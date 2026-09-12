"""Evidence analysis: determines SUPPORTED, NOT_FOUND, or CONTRADICTION state."""
import json
from typing import List
from openai import OpenAI
from backend.app.config import settings
from backend.app.models.schemas import (
    Chunk, EvidenceAnalysisResult, Evidence, Conflict, Citation,
)


class EvidenceAnalyzer:
    """Analyzes retrieved evidence to determine the answer state."""

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )
        self.model = settings.LLM_MODEL

    def analyze(self, question: str, chunks: List[Chunk]) -> EvidenceAnalysisResult:
        if not chunks:
            return EvidenceAnalysisResult(
                state="NOT_FOUND",
                relevant_evidence=[],
                reasoning="No evidence was retrieved from the corpus.",
                conflicts=None,
            )

        # Build evidence context for the LLM
        evidence_text = ""
        for i, chunk in enumerate(chunks):
            src = f"Document: {chunk.document}"
            if chunk.section:
                src += f" | Section: {chunk.section}"
            if chunk.page:
                src += f" | Page: {chunk.page}"
            evidence_text += (
                f"--- Evidence [{i+1}] (ID: {chunk.chunk_id}) ---\n"
                f"{src}\n"
                f"{chunk.text}\n\n"
            )

        system_prompt = (
            "You are an expert university-policy analyst. You must determine whether "
            "the provided evidence can answer the user's question.\n\n"
            "RULES:\n"
            "- Use ONLY the provided evidence. Never use general knowledge.\n"
            "- If the evidence clearly and consistently answers the question → state = SUPPORTED\n"
            "- If the evidence is irrelevant, insufficient, or doesn't address the question → state = NOT_FOUND\n"
            "- If two or more provisions give CONFLICTING guidance for the SAME situation → state = CONTRADICTION\n"
            "  (An explicit exception to a general rule is NOT a contradiction if they don't actually conflict.)\n"
            "  (A contradiction exists when one provision absolutely prohibits something that another provision permits.)\n\n"
            "Return ONLY valid JSON with this exact structure:\n"
            "{\n"
            '  "state": "SUPPORTED" | "NOT_FOUND" | "CONTRADICTION",\n'
            '  "relevant_evidence_indices": [1, 3],\n'
            '  "reasoning": "Explain your decision based on the evidence",\n'
            '  "conflicts": [\n'
            "    {\n"
            '      "evidence_a_index": 1,\n'
            '      "evidence_b_index": 3,\n'
            '      "reason": "Explain the specific conflict"\n'
            "    }\n"
            "  ]\n"
            "}\n"
            "Set conflicts to null if state is not CONTRADICTION.\n"
            "evidence indices are 1-based, matching the [N] labels above."
        )

        user_prompt = f"Question: {question}\n\nEvidence:\n{evidence_text}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )

            result = json.loads(response.choices[0].message.content)
            return self._parse_result(result, chunks)

        except Exception as e:
            return EvidenceAnalysisResult(
                state="NOT_FOUND",
                relevant_evidence=[],
                reasoning=f"Analysis error: {str(e)}",
                conflicts=None,
            )

    def _parse_result(
        self, result: dict, chunks: List[Chunk]
    ) -> EvidenceAnalysisResult:
        """Parse LLM JSON into structured result."""
        state = result.get("state", "NOT_FOUND")
        if state not in ("SUPPORTED", "NOT_FOUND", "CONTRADICTION"):
            state = "NOT_FOUND"

        # Map evidence indices to Evidence objects
        relevant_indices = result.get("relevant_evidence_indices", [])
        relevant_evidence: list[Evidence] = []
        for idx in relevant_indices:
            i = int(idx) - 1  # 1-based → 0-based
            if 0 <= i < len(chunks):
                c = chunks[i]
                relevant_evidence.append(Evidence(
                    document=c.document,
                    section=c.section,
                    page=c.page,
                    text=c.text,
                ))

        # Parse conflicts
        conflicts: list[Conflict] | None = None
        if state == "CONTRADICTION" and result.get("conflicts"):
            conflicts = []
            for conf in result["conflicts"]:
                idx_a = int(conf.get("evidence_a_index", 1)) - 1
                idx_b = int(conf.get("evidence_b_index", 2)) - 1

                if 0 <= idx_a < len(chunks) and 0 <= idx_b < len(chunks):
                    ca, cb = chunks[idx_a], chunks[idx_b]
                    conflicts.append(Conflict(
                        evidence_a=ca.text,
                        citation_a=Citation(
                            id=f"SRC-{idx_a+1:03d}",
                            document=ca.document,
                            section=ca.section,
                            page=ca.page,
                        ),
                        evidence_b=cb.text,
                        citation_b=Citation(
                            id=f"SRC-{idx_b+1:03d}",
                            document=cb.document,
                            section=cb.section,
                            page=cb.page,
                        ),
                        reason=conf.get("reason", "Conflicting provisions detected."),
                    ))
                    # Ensure both pieces are in relevant_evidence
                    for c in (ca, cb):
                        ev = Evidence(document=c.document, section=c.section,
                                      page=c.page, text=c.text)
                        if not any(e.document == ev.document and e.text == ev.text
                                   for e in relevant_evidence):
                            relevant_evidence.append(ev)

        # Safety: if SUPPORTED but no evidence, downgrade to NOT_FOUND
        if state == "SUPPORTED" and not relevant_evidence:
            state = "NOT_FOUND"

        return EvidenceAnalysisResult(
            state=state,
            relevant_evidence=relevant_evidence,
            conflicts=conflicts,
            reasoning=result.get("reasoning", ""),
        )

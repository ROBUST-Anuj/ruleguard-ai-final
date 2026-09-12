"""Grounded answer generation with citation markers."""
from typing import List
from openai import OpenAI
from backend.app.config import settings
from backend.app.models.schemas import (
    EvidenceAnalysisResult, QueryResponse, Evidence, Citation, Conflict,
)


class AnswerGenerator:
    """Generates grounded answers based on evidence analysis results."""

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            default_headers={"Accept-Encoding": "gzip, deflate"},
        )
        self.model = settings.LLM_MODEL

    def generate(self, question: str, analysis: EvidenceAnalysisResult) -> QueryResponse:
        if analysis.state == "NOT_FOUND":
            return self._not_found_response(question, analysis)
        elif analysis.state == "CONTRADICTION":
            return self._contradiction_response(question, analysis)
        else:
            return self._supported_response(question, analysis)

    # ── NOT FOUND ────────────────────────────────────────────

    def _not_found_response(
        self, question: str, analysis: EvidenceAnalysisResult
    ) -> QueryResponse:
        return QueryResponse(
            state="NOT_FOUND",
            answer=(
                "The supplied university regulations do not contain sufficient information "
                "to answer this question. The corpus was searched but no relevant provisions "
                "were found that directly address this topic."
            ),
            evidence=[],
            citations=[],
            conflicts=None,
            reasoning=analysis.reasoning,
        )

    # ── CONTRADICTION ────────────────────────────────────────

    def _contradiction_response(
        self, question: str, analysis: EvidenceAnalysisResult
    ) -> QueryResponse:
        # Build a structured contradiction answer
        parts = [
            "**CONTRADICTION DETECTED**\n\n"
            "Two or more applicable provisions in the university regulations conflict "
            "on this matter.\n"
        ]

        citations: list[Citation] = []
        if analysis.conflicts:
            for i, conflict in enumerate(analysis.conflicts):
                parts.append(f"\n**Provision A:**\n> {conflict.evidence_a[:500]}\n")
                parts.append(f"Source: `{conflict.citation_a.document}`")
                if conflict.citation_a.section:
                    parts.append(f" — {conflict.citation_a.section}")
                if conflict.citation_a.page:
                    parts.append(f" — Page {conflict.citation_a.page}")
                parts.append("\n")

                parts.append(f"\n**Provision B:**\n> {conflict.evidence_b[:500]}\n")
                parts.append(f"Source: `{conflict.citation_b.document}`")
                if conflict.citation_b.section:
                    parts.append(f" — {conflict.citation_b.section}")
                if conflict.citation_b.page:
                    parts.append(f" — Page {conflict.citation_b.page}")
                parts.append("\n")

                parts.append(f"\n**Why they conflict:** {conflict.reason}\n")

                citations.append(conflict.citation_a)
                citations.append(conflict.citation_b)

        parts.append(
            "\n**Conclusion:** The supplied regulations do not provide one unambiguous "
            "answer because these provisions overlap and conflict. You should consult "
            "the relevant administrative authority for clarification."
        )

        # Build evidence list
        evidence = analysis.relevant_evidence

        return QueryResponse(
            state="CONTRADICTION",
            answer="".join(parts),
            evidence=evidence,
            citations=citations,
            conflicts=analysis.conflicts,
            reasoning=analysis.reasoning,
        )

    # ── SUPPORTED ────────────────────────────────────────────

    def _supported_response(
        self, question: str, analysis: EvidenceAnalysisResult
    ) -> QueryResponse:
        # Build evidence context with citation IDs
        evidence_block = ""
        citations: list[Citation] = []
        for i, ev in enumerate(analysis.relevant_evidence):
            cite_id = f"SRC-{i+1:03d}"
            src = ev.document
            if ev.section:
                src += f" — {ev.section}"
            if ev.page:
                src += f" — Page {ev.page}"
            evidence_block += f"[{cite_id}] ({src}):\n{ev.text}\n\n"
            citations.append(Citation(
                id=cite_id,
                document=ev.document,
                section=ev.section,
                page=ev.page,
            ))

        # If analysis already produced a grounded answer, format citations directly
        if analysis.answer and analysis.answer.strip():
            import re
            answer = analysis.answer
            # Replace [1], 【1】, etc. with [SRC-001]
            def _cite_repl(m):
                idx = int(m.group(1))
                if 1 <= idx <= len(analysis.relevant_evidence):
                    return f"[SRC-{idx:03d}]"
                return m.group(0)
            answer = re.sub(r'[\[【](\d+)[\]】]', _cite_repl, answer)
            return QueryResponse(
                state="SUPPORTED",
                answer=answer,
                evidence=analysis.relevant_evidence,
                citations=citations,
                conflicts=None,
                reasoning=analysis.reasoning,
            )

        system_prompt = (
            "You are a university regulations assistant. Answer the user's question "
            "using ONLY the provided evidence. Include inline citation markers like "
            "[SRC-001] after each factual claim. Do not invent information. "
            "Be precise and professional."
        )

        user_prompt = (
            f"Question: {question}\n\n"
            f"Evidence:\n{evidence_block}\n"
            "Provide a clear, well-structured answer using only the evidence above. "
            "Cite sources with [SRC-NNN] markers."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error generating answer: {str(e)}"

        return QueryResponse(
            state="SUPPORTED",
            answer=answer,
            evidence=analysis.relevant_evidence,
            citations=citations,
            conflicts=None,
            reasoning=analysis.reasoning,
        )

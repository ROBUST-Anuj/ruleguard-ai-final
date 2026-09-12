# RuleGuard

**Ask your university rules. Get an answer you can verify.**

RuleGuard is an explainable university-regulations question-answering system that correctly distinguishes between three states: the rulebook **supports** an answer, the rulebook **does not contain** an answer, or the rulebook **contradicts itself**.

## Live Demo

> 🌐 **Public Live Demo:** **[https://ruleguard-ai-iota.vercel.app](https://ruleguard-ai-iota.vercel.app)**
>
> The live deployment runs the complete RuleGuard system on a single domain — serving the React single-page frontend and executing the FastAPI hybrid retrieval and reasoning pipeline via Vercel Python serverless functions.
>
> **GitHub Repository:** https://github.com/ROBUST-Anuj/ruleguard-ai-final

---

## Problem

Generic university chatbots retrieve text and let an LLM answer — but they can't tell you when the rules are silent or when two provisions conflict. Students get confident-sounding answers that may be invented from general knowledge, with no way to verify the source.

## Solution

RuleGuard implements a three-state evidence analysis pipeline:

| State | Meaning | Visual |
|-------|---------|--------|
| **SUPPORTED** | The corpus contains sufficient evidence to answer | 🟢 Green |
| **NOT_FOUND** | The corpus does not address this question | 🟡 Amber |
| **CONTRADICTION** | Two or more provisions conflict | 🔴 Red |

Every answer is grounded in the supplied corpus with precise citations. The system never invents policy from general knowledge.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     React Frontend                       │
│        (Vite + TypeScript + Tailwind CSS)                │
└───────────────────────┬──────────────────────────────────┘
                        │ POST /api/query
┌───────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend                        │
│                                                          │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  ┌─────────┐ │
│  │ Hybrid  │→ │ Evidence │→ │  Answer   │→ │Citation │ │
│  │Retrieval│  │ Analyzer │  │ Generator │  │Validator│ │
│  └────┬────┘  └──────────┘  └───────────┘  └─────────┘ │
│       │                                                  │
│  ┌────▼────┐  ┌──────────┐                               │
│  │Semantic │  │ Lexical  │                               │
│  │ (FAISS) │  │ (BM25)   │                               │
│  └────┬────┘  └────┬─────┘                               │
│       └─────┬──────┘                                     │
│        ┌────▼────┐                                       │
│        │  Index  │ ← Ingestion Pipeline                  │
│        └────┬────┘                                       │
│        ┌────▼────┐                                       │
│        │ Corpus  │  8 Markdown + 1 PDF                   │
│        └─────────┘                                       │
└──────────────────────────────────────────────────────────┘
```

### Pipeline

```
User Question
  → Hybrid Retrieval (semantic + lexical)
    → Evidence Analysis (LLM determines SUPPORTED / NOT_FOUND / CONTRADICTION)
      → Grounded Answer Generation (with citation markers)
        → Citation Validation (verify sources exist)
          → Structured API Response
```

---

## Features

- **Grounded answers** — every factual claim cites the source document and section
- **Three-state classification** — SUPPORTED, NOT_FOUND, or CONTRADICTION
- **Contradiction detection** — identifies conflicting provisions across documents
- **Hybrid retrieval** — combines FAISS semantic search with BM25 keyword matching
- **Structure-aware chunking** — splits by headings and sections, not arbitrary character counts
- **Citation validation** — verifies all cited documents and sections exist
- **Evaluation suite** — 50 questions across three categories with automated scoring
- **PDF support** — extracts text with page-level metadata from PDF documents

---

## Dataset

| Property | Value |
|----------|-------|
| Institution | Northbridge Institute of Technology (NIT) — fictional |
| Corpus size | ~10,000 words |
| Documents | 8 Markdown policies + 1 PDF handbook |
| Planted contradictions | 3 (documented in `data/contradictions.md`) |
| Evaluation questions | 50 total (15 answerable, 10 contradiction, 25 unanswerable) |

### Deliberate Contradictions

| ID | Topic | Documents |
|----|-------|-----------|
| CON-001 | Attendance threshold for medical exemption | `attendance_policy.md` §4.2 vs `medical_exemption_policy.md` §3.1 |
| CON-002 | Fee payment deadline and deregistration | `fee_regulations.md` §2.1 vs `academic_regulations.md` §6.3 |
| CON-003 | Number of supplementary exam attempts | `examination_policy.md` §7.1 vs `academic_regulations.md` §5.4 |

---

## Demo Scenarios

### 🟢 Scenario 1 — SUPPORTED

> **Q:** What is the minimum attendance required for semester examinations?
>
> **A:** Students must maintain a minimum attendance of 75% in each registered course. [SRC-001]

### 🟡 Scenario 2 — NOT FOUND

> **Q:** What happens if I miss the examination because of a family wedding?
>
> **A:** The supplied university regulations do not contain sufficient information to answer this question.

### 🔴 Scenario 3 — CONTRADICTION

> **Q:** Can I appear for the examination with 68% attendance if I have a medical exemption?
>
> **A:** CONTRADICTION DETECTED — The Attendance Policy (§4.2) states "No exceptions shall be granted below 75%" but the Medical Exemption Policy (§3.1) permits examinations with attendance as low as 60%.

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- An OpenAI API key (or compatible API)

### 1. Clone and install

```bash
git clone https://github.com/ROBUST-Anuj/ruleguard-ai-final.git
cd ruleguard-ai-final

# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your API key:
# LLM_API_KEY=sk-your-key-here
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_API_KEY` | — | OpenAI API key (required) |
| `LLM_MODEL` | `gpt-4o-mini` | LLM model for analysis and generation |
| `LLM_BASE_URL` | `https://api.openai.com/v1` | API base URL (change for compatible APIs) |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model for semantic search |
| `SEMANTIC_WEIGHT` | `0.65` | Weight for semantic retrieval in hybrid score |
| `LEXICAL_WEIGHT` | `0.35` | Weight for lexical retrieval in hybrid score |
| `TOP_K` | `10` | Number of chunks to retrieve |

### 3. Generate PDF and ingest corpus

```bash
python scripts/generate_pdf.py
python scripts/ingest.py
```

### 4. Run the application

```bash
# Terminal 1: Backend
uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

---

## Evaluation

```bash
# Make sure the backend is running first
python evaluate.py
```

Results are saved to `evaluation/results.json`.

---

## Tests

```bash
pytest backend/tests/ -v
```

---

## Project Structure

```
ruleguard-ai/
├── backend/
│   ├── app/
│   │   ├── api/routes.py            # FastAPI endpoints
│   │   ├── ingestion/
│   │   │   ├── document_loader.py   # MD/PDF loading
│   │   │   ├── chunker.py           # Structure-aware chunking
│   │   │   ├── embeddings.py        # OpenAI embeddings
│   │   │   └── indexer.py           # FAISS + BM25 indexes
│   │   ├── retrieval/
│   │   │   ├── semantic.py          # FAISS similarity search
│   │   │   ├── lexical.py           # BM25 keyword search
│   │   │   └── hybrid.py            # Combined scoring
│   │   ├── reasoning/
│   │   │   ├── evidence_analyzer.py # Three-state classification
│   │   │   ├── answer_generator.py  # Grounded answer generation
│   │   │   └── pipeline.py          # Full pipeline orchestration
│   │   ├── citations/validator.py   # Citation validation
│   │   ├── models/schemas.py        # Pydantic models
│   │   ├── config.py                # Settings
│   │   └── main.py                  # FastAPI app
│   └── tests/                       # pytest test suite
├── frontend/
│   └── src/
│       ├── components/              # React components
│       ├── pages/Home.tsx           # Main page
│       ├── api/client.ts            # API client
│       └── types/index.ts           # TypeScript types
├── data/
│   ├── corpus/                      # 8 Markdown policy documents
│   ├── pdf/                         # Generated PDF handbook
│   ├── evaluation/                  # Test datasets (50 questions)
│   └── contradictions.md            # Documented contradictions
├── scripts/
│   ├── ingest.py                    # Corpus ingestion pipeline
│   └── generate_pdf.py              # PDF generation
├── evaluate.py                      # Evaluation script
├── requirements.txt
├── .env.example
└── README.md
```

---

## API

### POST /api/query

```json
// Request
{ "question": "What is the minimum attendance required?" }

// Response
{
  "state": "SUPPORTED",
  "answer": "Students must maintain 75% attendance. [SRC-001]",
  "evidence": [
    {
      "document": "attendance_policy.md",
      "section": "4.2 Minimum Attendance Requirements",
      "page": null,
      "text": "Students must maintain a minimum attendance of 75%..."
    }
  ],
  "citations": [
    {
      "id": "SRC-001",
      "document": "attendance_policy.md",
      "section": "4.2 Minimum Attendance Requirements"
    }
  ]
}
```

### GET /api/health

Returns API status and index load state.

### GET /api/sources

Lists all indexed source documents.

---

## What Is Real vs Mocked

### Genuinely Implemented (Real)

| Component | Detail |
|-----------|--------|
| **Document corpus** | 8 Markdown policy documents (~10,000 words) written for a fictional university (Northbridge Institute of Technology). Content is original and authored for this project. |
| **PDF handbook** | Generated from corpus content using ReportLab. Contains headings, tables, and page numbers. Real PDF extraction via PyMuPDF. |
| **Document ingestion** | Real Markdown parser and PDF text extractor that preserves section headings, page numbers, and document metadata. |
| **Structure-aware chunking** | Real implementation that splits by Markdown headings, not arbitrary character counts. Produces deterministic chunk IDs. |
| **Semantic retrieval** | Real FAISS vector index with OpenAI `text-embedding-3-small` embeddings. Vectors are computed at ingestion time and stored locally. |
| **Lexical retrieval** | Real BM25 keyword index via `rank_bm25`. |
| **Hybrid retrieval** | Real score normalization and weighted combination of semantic + lexical results. |
| **Three-state classification** | Real LLM-based evidence analysis that determines SUPPORTED / NOT_FOUND / CONTRADICTION from retrieved evidence. Not hardcoded — the LLM evaluates evidence at runtime. |
| **Contradiction detection** | Real — the LLM identifies conflicting provisions from different corpus documents. Contradictions are not pattern-matched by question; the system analyses the retrieved evidence for conflicts. Three deliberate contradictions are planted in the corpus and documented in `data/contradictions.md`. |
| **Citation validation** | Real — verifies that every cited document exists in the corpus and that PDF citations include valid page numbers. Invalid citations are filtered out. |
| **Grounded answer generation** | Real — the LLM generates answers using only retrieved evidence, with inline `[SRC-NNN]` citation markers mapped to real source passages. |
| **FastAPI backend** | Real REST API with `/api/query`, `/api/health`, and `/api/sources` endpoints. |
| **React frontend** | Real single-page application built with Vite + TypeScript + Tailwind CSS. Three distinct UI states with color-coded badges. |
| **Evaluation system** | Real automated evaluation script that queries the live API with 50 test questions and computes per-category accuracy. No hardcoded scores. |
| **Test suite** | Real pytest tests (29 tests) covering chunking, retrieval, citation validation, schema validation, and API request validation. |

### External Dependencies (Not Mocked, but Require Configuration)

| Component | Detail |
|-----------|--------|
| **OpenAI API** | The system requires a valid OpenAI API key for: (1) generating embeddings during ingestion, and (2) evidence analysis and answer generation at query time. Without an API key, ingestion and querying will fail. The API key is never committed — it must be provided via `.env`. |

### What Is NOT Included

| Component | Detail |
|-----------|--------|
| **User authentication** | No login or session management. |
| **Database** | Indexes are stored as local files (FAISS index + pickled BM25). No PostgreSQL/Redis. |
| **Deployment** | No Docker, Kubernetes, or cloud deployment configuration. The project runs locally. |
| **Caching** | No query result caching. Each query calls the LLM. |

---

## Limitations

- Contradiction detection relies on LLM analysis, which may occasionally miss subtle conflicts or flag legitimate exceptions as contradictions
- The corpus is fictional and limited to ~10,000 words; real university regulations would be much larger
- Evaluation accuracy depends on the LLM model used; results may vary across providers
- No document versioning — the system assumes a single static corpus
- No user authentication or session persistence

## Future Improvements

- Stronger reranking with cross-encoder models
- Contradiction graphs for visualizing policy conflicts
- Document versioning and change tracking
- Multilingual support
- Human review workflows for flagged contradictions
- Caching layer for repeated queries
- Fine-tuned embedding model for policy language

---

## License

MIT

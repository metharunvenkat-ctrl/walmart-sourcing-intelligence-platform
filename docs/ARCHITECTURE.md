# 🏗️ System Architecture & Engineering Blueprint

This document details the architectural principles, component interactions, and data processing flows for the **Walmart Sourcing & Procurement Intelligence Platform**.

---

## 1. System Architecture Overview

```text
  +-----------------------------------------------------------------------+
  |                        React 18 Frontend UI                           |
  |  (Tier 1 Executive Scorecard | Tier 2 Battlecard | Tier 3 Accordion)  |
  +-----------------------------------+-----------------------------------+
                                      | HTTP REST (JSON)
                                      v
  +-----------------------------------------------------------------------+
  |                       FastAPI Backend Service                         |
  |   (/api/documents/upload | /api/gaps/analyze | /api/chat/query)      |
  +-----------------------------------+-----------------------------------+
                                      |
         +----------------------------+----------------------------+
         |                                                         |
         v                                                         v
+-----------------------------+                           +--------------------------------+
| IBM Docling Parser          |                           | Google Gemini 2.5 Flash LLM    |
| (DocumentConverter)         |                           | (Structured Gap Analysis JSON) |
+--------------+--------------+                           +---------------+----------------+
               |                                                          |
               v                                                          v
+-----------------------------+                           +--------------------------------+
| Layout Markdown Chunker     |                           | PostgreSQL 16 + pgvector       |
| (Story vs Criteria Chunks)  |                           | (768-dim Embeddings & Metadata)|
+-----------------------------+                           +--------------------------------+
```

---

## 2. Document Processing & Ingestion Workflow

1. **Document Conversion**: IBM Docling (`DocumentConverter`) ingests PDF, DOCX, or HTML contracts, parsing layout components into clean Markdown trees while maintaining section headings (`#`, `##`), tables, and page boundaries.
2. **Chunking Engine**:
   - `story` chunks: Narrative context blocks (1000–1500 tokens).
   - `criteria` chunks: Specific clause-level parameters (e.g. Payment terms, SLA metrics, Liability caps).
3. **Embedding Generation**: Text chunks pass through Google Gemini `text-embedding-004` to produce 768-dimensional dense vectors.
4. **pgvector Storage**: Vectors are stored in `document_chunks` table alongside JSONB metadata (`story_id`, `page_number`, `category_tag`) and indexed with IVFFlat cosine similarity.

---

## 3. Anti-Hallucination Guardrails

- **Low Temperature Decoding**: Gap analysis runs at $T=0.2$ to enforce deterministic, non-creative factual extraction.
- **Dual-Anchor Citations**: Prompts require explicit file names and section titles for all identified contract deviations.
- **Pydantic Validation**: LLM JSON outputs are parsed directly into Pydantic models. Any schema mismatch triggers an automated retry.

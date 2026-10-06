# 🔌 REST API Specification

The FastAPI backend exposes the following core REST endpoints:

## 1. Document Upload & Ingestion
- **POST** `/api/documents/upload`
  - Multipart form upload of vendor proposals or SLA baselines.
  - Returns `document_id`, `chunk_count`, and status.

## 2. Gap Analysis & Battlecard Generation
- **POST** `/api/gaps/analyze`
  - Input: `{ "proposal_document_id": "...", "baseline_document_id": "..." }`
  - Returns: Tier 1 Scorecard, Tier 2 Battlecard Items, Tier 3 Section Accordions.

## 3. Contextual Sourcing Chatbot
- **POST** `/api/chat/query`
  - Input: `{ "query": "What is the liability cap in the Apex Logistics proposal?", "session_id": "..." }`
  - Returns: Grounded answer text with source document citations and similarity scores.


---

## ⚠️ Disclaimer Notice
This document and all associated dataset examples are synthetic mock artifacts engineered exclusively for independent portfolio demonstration purposes. This project is not affiliated with or endorsed by Walmart Inc.
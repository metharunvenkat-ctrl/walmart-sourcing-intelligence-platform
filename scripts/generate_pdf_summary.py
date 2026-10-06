import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6B7280"))
        
        # Header (on pages after cover)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Walmart Sourcing Intelligence Platform — Executive Technical Summary")
            self.setStrokeColor(colors.HexColor("#E5E7EB"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL — FOR WALMART SOURCING & PROCUREMENT TEAM")
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    NAVY = colors.HexColor("#041E42")       # Walmart Deep Navy
    BLUE = colors.HexColor("#0071CE")       # Walmart Primary Blue
    YELLOW = colors.HexColor("#FFC220")     # Walmart Gold
    DARK = colors.HexColor("#1F2937")       # Body Text Dark Slate
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Callout Box Light Gray/Blue
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=NAVY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=BLUE,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=BLUE,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK,
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK,
        leftIndent=10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=DARK
    )

    story = []
    
    # ---------------------------------------------------------
    # COVER / HEADER
    # ---------------------------------------------------------
    story.append(Spacer(1, 5))
    story.append(Paragraph("Walmart Sourcing & Procurement Intelligence Platform", title_style))
    story.append(Paragraph("Comprehensive Technical Project Summary, RAG Architecture & System Blueprint", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceBefore=0, spaceAfter=12))
    
    # Metadata Block Table
    meta_data = [
        [Paragraph("<b>Project Scope:</b> Walmart Category Management RAG Engine", table_cell_style), Paragraph("<b>Parsing Engine:</b> IBM Docling (DocumentConverter)", table_cell_style)],
        [Paragraph("<b>Primary Vector Store:</b> PostgreSQL 16 + pgvector", table_cell_style), Paragraph("<b>LLM Backend:</b> Google Gemini 2.5 Flash / Flash Lite", table_cell_style)],
        [Paragraph("<b>Embedding Model:</b> text-embedding-004 (768d)", table_cell_style), Paragraph("<b>Deployment:</b> Docker Compose Multi-Container", table_cell_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # ---------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Core Business Objectives", h1_style))
    story.append(Paragraph(
        "The <b>Walmart Sourcing & Procurement Intelligence Platform</b> is an enterprise-grade Retrieval-Augmented Generation (RAG) system "
        "engineered specifically for Walmart category buyers, procurement managers, and legal reviewers. When evaluating complex vendor proposals, "
        "service level agreements (SLAs), and master supply agreements (MSAs), sourcing teams typically spend days manually comparing incoming "
        "bids against Walmart's master procurement baselines and historical category precedents.",
        body_style
    ))
    story.append(Paragraph(
        "This platform automates contract comparison, vendor proposal gap analysis, precedent benchmarking, and interactive negotiation battlecard "
        "generation—reducing review cycles from days to under 60 seconds while providing 100% grounded citations to raw contract clauses.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 2: SOURCING & PROCUREMENT USE CASES
    # ---------------------------------------------------------
    story.append(Paragraph("2. Primary Sourcing & Procurement Use Cases", h1_style))
    
    use_cases = [
        ("Vendor Proposal Evaluation & Gap Detection", "Automated side-by-side contract comparison highlighting explicit deviations, un-capped liabilities, payment term discrepancies (e.g. Net 90 vs Net 30), and omitted SLA metrics relative to Walmart baseline expectations."),
        ("Precedent Knowledgebase Benchmarking", "Indexing historical supplier agreements across product categories (Activewear, Footwear, Electronics, Logistics) to empower sourcing managers with past precedent benchmarks during negotiation."),
        ("Priority Negotiation Battlecard Generation", "Extracting high-risk contract deviations and ranking them by priority with precise clause citations, summary of variance, and exact contract source references."),
        ("Category-Aware Interactive AI Assistant", "Context-grounded chatbot allowing procurement officers to query vendor commitments, liability caps, audit rights, and termination clauses across indexed documents.")
    ]
    for title, desc in use_cases:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 3: HIGH-LEVEL ARCHITECTURE & COMPONENTS
    # ---------------------------------------------------------
    story.append(Paragraph("3. Platform Architecture & System Workflow", h1_style))
    story.append(Paragraph(
        "The system follows a modern microservice architecture structured into four decoupled layers: Document Parsing, Vector Indexing, "
        "LLM Synthesis, and Tiered Frontend Visualization.",
        body_style
    ))
    
    # Architecture Flow ASCII Table
    arch_flow = [
        [Paragraph("<b>Layer</b>", table_header_style), Paragraph("<b>Technology / Tool</b>", table_header_style), Paragraph("<b>Role & Operation</b>", table_header_style)],
        [Paragraph("1. Document Parsing", table_cell_style), Paragraph("<b>IBM Docling</b><br/>(DocumentConverter)", table_cell_style), Paragraph("Converts PDF, DOCX, HTML into layout-aware Markdown trees while maintaining headers, tables, and page boundaries.", table_cell_style)],
        [Paragraph("2. Chunking Engine", table_cell_style), Paragraph("<b>Layout-Aware Splitter</b>", table_cell_style), Paragraph("Splits text into <i>Story</i> (narrative context) and <i>Criteria</i> (clause-level granularity) chunks with rich JSON metadata.", table_cell_style)],
        [Paragraph("3. Embedding & Vector DB", table_cell_style), Paragraph("<b>Google Gemini Embedding</b><br/>+ PostgreSQL pgvector", table_cell_style), Paragraph("Generates 768-dim embeddings (`text-embedding-004`) stored with IVFFlat cosine similarity indexes.", table_cell_style)],
        [Paragraph("4. Gap Analysis LLM", table_cell_style), Paragraph("<b>Google Gemini 2.5 Flash</b><br/>(Temperature = 0.2)", table_cell_style), Paragraph("Executes grounded JSON gap analysis comparing incoming proposals against baseline SLAs with Pydantic validation.", table_cell_style)],
        [Paragraph("5. UI Dashboard", table_cell_style), Paragraph("<b>React + TypeScript</b><br/>+ Tailwind CSS", table_cell_style), Paragraph("Renders Tier 1 Sub-scores, Tier 2 Negotiation Battlecard, and Tier 3 Collapsible Section Accordions.", table_cell_style)]
    ]
    arch_table = Table(arch_flow, colWidths=[100, 140, 260])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 4: DETAILED FRONTEND UI DASHBOARD (TIER 1, 2, 3)
    # ---------------------------------------------------------
    story.append(Paragraph("4. Frontend UI Workflow & Tiered Battlecard Design", h1_style))
    story.append(Paragraph(
        "The frontend user interface is organized into three distinct analysis tiers to serve both executive overview needs and granular legal inspection:",
        body_style
    ))
    
    story.append(Paragraph("• <b>Tier 1: High-Level Executive Summary & Scorecard</b>", h2_style))
    story.append(Paragraph(
        "Displays an overall contract compatibility score (0-100%) calculated across weighted domain criteria. "
        "Includes visual status count pills highlighting <b>🟢 Compliant</b>, <b>🟡 Deviation</b>, and <b>🔴 Gap</b> metrics at a glance.",
        bullet_style
    ))
    
    story.append(Paragraph("• <b>Tier 2: Priority Negotiation Battlecard</b>", h2_style))
    story.append(Paragraph(
        "Streamlined for maximum clarity during vendor calls. Unnecessary leverage and counter-position boxes have been completely removed. "
        "Each battlecard item features: <b>Priority Tag (#1, #2...)</b>, <b>Clause Category Tag</b>, <b>Concise Deviation Summary</b>, and an interactive "
        "collapsible drawer: <i>📜 View Citation & Precedent Benchmark ▼</i>.",
        bullet_style
    ))
    
    story.append(Paragraph("• <b>Tier 3: Section-Wise Analysis (`📋 Tier 3 Section-Wise Analysis`)</b>", h2_style))
    story.append(Paragraph(
        "Groups contract clauses by section (e.g. Legal & Liability, Payment & Commercials, Logistics & Delivery). "
        "Section accordions default to collapsed (`open = false`) and expand upon click to reveal clause-by-clause baseline vs proposal comparisons.",
        bullet_style
    ))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 5: DATABASE SCHEMA & INSPECTION
    # ---------------------------------------------------------
    story.append(Paragraph("5. Database Schema & Inspection Commands", h1_style))
    story.append(Paragraph(
        "The system utilizes PostgreSQL 16 with the `pgvector` extension. The central relation is `document_chunks`:",
        body_style
    ))
    
    schema_rows = [
        [Paragraph("<b>Column Name</b>", table_header_style), Paragraph("<b>Data Type</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("`chunk_id`", table_cell_style), Paragraph("UUID (Primary Key)", table_cell_style), Paragraph("Unique identifier for each document chunk.", table_cell_style)],
        [Paragraph("`chunk_type`", table_cell_style), Paragraph("VARCHAR(20)", table_cell_style), Paragraph("Identifies chunk granularity (`story` or `criteria`).", table_cell_style)],
        [Paragraph("`content`", table_cell_style), Paragraph("TEXT", table_cell_style), Paragraph("Extracted clause or section text content.", table_cell_style)],
        [Paragraph("`embedding`", table_cell_style), Paragraph("vector(768)", table_cell_style), Paragraph("Gemini 768-dimensional dense vector with IVFFlat index.", table_cell_style)],
        [Paragraph("`story_id`", table_cell_style), Paragraph("UUID", table_cell_style), Paragraph("Parent document / story relation ID.", table_cell_style)],
        [Paragraph("`metadata`", table_cell_style), Paragraph("JSONB", table_cell_style), Paragraph("Contains page numbers, section headers, document title, category tag.", table_cell_style)],
        [Paragraph("`source_path`", table_cell_style), Paragraph("TEXT", table_cell_style), Paragraph("Original file path or upload filename.", table_cell_style)]
    ]
    schema_table = Table(schema_rows, colWidths=[100, 120, 280])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(schema_table)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("<b>Live Database Inspection Command:</b>", h2_style))
    db_cmd_text = "docker exec -it rag-db-1 psql -U postgres -d rag_db -c \"SELECT chunk_id, chunk_type, source_path FROM document_chunks LIMIT 5;\""
    story.append(Paragraph(f"<code>{db_cmd_text}</code>", code_style))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 6: TOOL SELECTION & TRADE-OFF MATRIX
    # ---------------------------------------------------------
    story.append(Paragraph("6. Tool Selection Trade-Off Analysis", h1_style))
    
    tradeoffs = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Selected Tool</b>", table_header_style), Paragraph("<b>Alternatives</b>", table_header_style), Paragraph("<b>Selection Rationale</b>", table_header_style)],
        [Paragraph("Document Parsing", table_cell_style), Paragraph("<b>IBM Docling</b>", table_cell_style), Paragraph("PyPDF, Unstructured", table_cell_style), Paragraph("Native layout awareness; preserves markdown table structures & section hierarchy perfectly for legal contracts.", table_cell_style)],
        [Paragraph("Vector Store", table_cell_style), Paragraph("<b>PostgreSQL + pgvector</b>", table_cell_style), Paragraph("Pinecone, ChromaDB", table_cell_style), Paragraph("Eliminates external SaaS dependency; unifies relational metadata (JSONB) with vector search in a single ACID DB.", table_cell_style)],
        [Paragraph("LLM Engine", table_cell_style), Paragraph("<b>Google Gemini 2.5 Flash</b>", table_cell_style), Paragraph("OpenAI GPT-4o, Ollama", table_cell_style), Paragraph("1M token context window allows full document pair injection; exceptional structured JSON enforcement speed.", table_cell_style)],
        [Paragraph("Deployment", table_cell_style), Paragraph("<b>Docker Compose</b>", table_cell_style), Paragraph("Bare-metal, Kubernetes", table_cell_style), Paragraph("Guarantees reproducible multi-container environment across developer laptops and production servers.", table_cell_style)]
    ]
    to_table = Table(tradeoffs, colWidths=[85, 95, 110, 210])
    to_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(to_table)
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 7: ANTI-HALLUCINATION GUARDRAILS
    # ---------------------------------------------------------
    story.append(Paragraph("7. Anti-Hallucination & Reliability Guardrails", h1_style))
    story.append(Paragraph("To ensure zero hallucination in high-stakes contract reviews, 6 strict safety mechanisms are enforced:", body_style))
    
    guardrails = [
        ("1. Layout Hierarchy Preservation", "Docling extracts exact section titles and paragraph boundaries, eliminating artificial text split errors."),
        ("2. Dual-Anchor Citation Mandate", "LLM system prompts explicitly require citing exact document names and section titles for every gap identified."),
        ("3. Direct Raw Context Window Injection", "Both incoming proposal text and baseline contract text are passed simultaneously in the context window."),
        ("4. Low Temperature Decoding", "Extraction and gap analysis run at T=0.2 to enforce deterministic, factual output generation."),
        ("5. Strict Pydantic JSON Schema Validation", "All LLM outputs are parsed into strict Pydantic data models with mandatory field checks."),
        ("6. Cosine Distance Traceability", "Vector search results include distance metrics (1.0 - distance) ensuring full traceability back to source DB chunks.")
    ]
    for title, desc in guardrails:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 8: SYSTEM PROMPTS SUMMARY
    # ---------------------------------------------------------
    story.append(Paragraph("8. Core System Prompts Overview", h1_style))
    story.append(Paragraph(
        "The platform relies on three specialized system prompts located in <code>src/rag_ingest/prompts/</code>:",
        body_style
    ))
    story.append(Paragraph("• <b>`GAP_ANALYSIS_PROMPT`</b>: Enforces side-by-side contract comparison against Walmart SLA baselines, returning Tier 1 score breakdown, Tier 2 priority battlecard items, and Tier 3 section accordions.", bullet_style))
    story.append(Paragraph("• <b>`INGESTION_PROMPT`</b>: Classifies incoming Markdown documents into structured story vs criteria chunks, assigning category metadata and clause tags.", bullet_style))
    story.append(Paragraph("• <b>`CHAT_PROMPT`</b>: Governs the sourcing chatbot, ensuring all answers are grounded strictly in retrieved pgvector context with explicit file citations.", bullet_style))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 9: DOCKER & ENVIRONMENT CONFIGURATION
    # ---------------------------------------------------------
    story.append(Paragraph("9. Docker Containerization & Environment Setup", h1_style))
    story.append(Paragraph(
        "The system is containerized into three primary services defined in <code>docker-compose.yml</code>:",
        body_style
    ))
    story.append(Paragraph("• <b>`rag-db-1`</b>: PostgreSQL 16 with `pgvector/pgvector:pg16` image listening on host port 5433 (container port 5432).", bullet_style))
    story.append(Paragraph("• <b>`rag-backend-1`</b>: FastAPI Python 3.11 service listening on port 8000.", bullet_style))
    story.append(Paragraph("• <b>`rag-frontend-1`</b>: React Vite application served via Nginx on port 3000.", bullet_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Key Environment Variables (`.env`):</b>", h2_style))
    env_sample = "GEMINI_API_KEY=AIzaSy...\nPOSTGRES_USER=postgres\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_DB=rag_db\nPOSTGRES_HOST=db\nPOSTGRES_PORT=5432\nLLM_MODEL=gemini-2.5-flash"
    story.append(Paragraph(f"<code>{env_sample.replace(chr(10), '<br/>')}</code>", code_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 10: FUTURE ROADMAP
    # ---------------------------------------------------------
    story.append(Paragraph("10. Future Platform Enhancements & Enterprise Roadmap", h1_style))
    future_items = [
        ("ERP / SAP Ariba Integration", "Direct API integration with SAP Ariba and Coupa for automated contract ingestion upon supplier upload."),
        ("Automated DOCX Redlining", "Exporting Tier 2 negotiation battlecards directly into tracked-changes Word documents (.docx) for vendor sharing."),
        ("Multi-Modal Proposal Parsing", "Utilizing Gemini Vision capabilities to extract complex tables, workflow diagrams, and price schedules embedded as images.")
    ]
    for title, desc in future_items:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete:", filename)

if __name__ == '__main__':
    desktop_pdf = os.path.join(os.path.dirname(__file__), "..", "docs", "reports", "Walmart_Project_Summary.pdf")
    desktop_pdf_alt = os.path.join(os.path.dirname(__file__), "..", "docs", "Walmart_Project_Summary.pdf")
    folder_pdf = r"C:\Users\metha\OneDrive\Desktop\walmart project summary.pdf"
    
    build_pdf(desktop_pdf)
    build_pdf(desktop_pdf_alt)
    build_pdf(folder_pdf)

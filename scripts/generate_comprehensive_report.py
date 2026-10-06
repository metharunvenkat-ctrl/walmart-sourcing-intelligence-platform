import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

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
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Walmart Sourcing Intelligence Platform — Comprehensive Engineering Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "INDEPENDENT TECHNICAL PORTFOLIO REPORT — MOCK SYNTHETIC DATA ONLY")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def get_scaled_image(path, target_width=480):
    if not os.path.exists(path):
        return None
    try:
        with PILImage.open(path) as img:
            w, h = img.size
            aspect = h / float(w)
            target_height = target_width * aspect
            return Image(path, width=target_width, height=target_height)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

def build_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    NAVY = colors.HexColor("#041E42")       # Walmart Deep Navy
    BLUE = colors.HexColor("#0071CE")       # Primary Blue
    GOLD = colors.HexColor("#D97706")       # Accent Amber/Gold
    DARK = colors.HexColor("#1F2937")       # Body Text
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Table / Callout Background
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    GREEN = colors.HexColor("#166534")
    
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=BLUE,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=15,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=BLUE,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK,
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK,
        leftIndent=10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    
    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )
    
    table_cell_style = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=DARK
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4B5563"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=8
    )

    story = []
    
    # ---------------------------------------------------------
    # HEADER & METADATA
    # ---------------------------------------------------------
    story.append(Spacer(1, 4))
    story.append(Paragraph("Walmart Sourcing & Procurement Intelligence Platform", title_style))
    story.append(Paragraph("Comprehensive Architectural Report, Tool Rationale, Backend Execution & UI Insights", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceBefore=0, spaceAfter=10))
    
    meta_table_data = [
        [Paragraph("<b>Author / Engineer:</b> Metharun Venkat", table_cell_style), Paragraph("<b>Parsing Engine:</b> IBM Docling (`DocumentConverter`)", table_cell_style)],
        [Paragraph("<b>Vector Database:</b> PostgreSQL 16 + pgvector", table_cell_style), Paragraph("<b>LLM Backend:</b> Google Gemini 2.5 Flash ($T=0.2$)", table_cell_style)],
        [Paragraph("<b>Embedding Model:</b> text-embedding-004 (768d)", table_cell_style), Paragraph("<b>Repository:</b> `metharunvenkat-ctrl/walmart-sourcing...`", table_cell_style)]
    ]
    t_meta = Table(meta_table_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))
    
    # ---------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "In global retail category management, evaluating complex vendor proposals against master procurement baselines and historical category "
        "precedents is a labor-intensive, error-prone process. Sourcing officers typically review 50+ page vendor submissions containing subtle commercial "
        "variances (e.g., Net 60 vs Net 90 payment terms, reduced Defective Merchandise Allowances, uncapped liability limits, or omitted SLA guarantees). "
        "Manual evaluation cycles take several days per RFP response, risking missed risk exposure or unoptimized negotiation leverage.",
        body_style
    ))
    story.append(Paragraph(
        "The <b>Walmart Sourcing & Procurement Intelligence Platform</b> solves this by combining layout-aware document conversion with Retrieval-Augmented "
        "Generation (RAG) and tiered structured evaluation. The system automatically ingests vendor proposals, executes clause-by-clause gap analysis "
        "against Walmart baseline MSAs, retrieves historical category precedent benchmarks, and renders interactive negotiation battlecards in under <b>60 seconds</b>.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # ---------------------------------------------------------
    # SECTION 2: TOOL SELECTION & ARCHITECTURAL TRADE-OFF ANALYSIS
    # ---------------------------------------------------------
    story.append(Paragraph("2. Tool Selection & Comparative Trade-off Analysis", h1_style))
    story.append(Paragraph(
        "Every technology component was selected following rigorous comparative evaluation against industry alternatives to maximize layout precision, "
        "data privacy, execution speed, and cost efficiency:",
        body_style
    ))
    
    tool_rows = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Selected Tool</b>", table_header_style), Paragraph("<b>Alternatives Considered</b>", table_header_style), Paragraph("<b>Detailed Selection Rationale & Advantages</b>", table_header_style)],
        [
            Paragraph("Document Parser", table_cell_style),
            Paragraph("<b>IBM Docling</b><br/>(`DocumentConverter`)", table_cell_style),
            Paragraph("PyPDF, Unstructured,<br/>LlamaIndex, PDFMiner", table_cell_style),
            Paragraph("Docling natively preserves document layout trees, multi-page table structures, section headings, and header/footer metadata. Standard PDF parsers strip layout context, causing broken tables and misaligned clause boundaries.", table_cell_style)
        ],
        [
            Paragraph("Vector Store", table_cell_style),
            Paragraph("<b>PostgreSQL 16</b><br/>+ `pgvector`", table_cell_style),
            Paragraph("Pinecone, ChromaDB,<br/>Milvus, Qdrant", table_cell_style),
            Paragraph("Eliminates external SaaS API costs and vendor lock-in. Unifies dense vector similarity search (`vector(768)` with IVFFlat cosine index) and relational metadata (`JSONB`) in a single ACID-compliant database.", table_cell_style)
        ],
        [
            Paragraph("LLM Engine", table_cell_style),
            Paragraph("<b>Google Gemini 2.5 Flash</b><br/>($T=0.2$)", table_cell_style),
            Paragraph("OpenAI GPT-4o,<br/>Local Ollama Llama-3", table_cell_style),
            Paragraph("1M token context window allows full document pair injection (baseline + vendor proposal + precedent context simultaneously). Superior speed for structured JSON schema enforcement via Pydantic validation.", table_cell_style)
        ],
        [
            Paragraph("Embedding Model", table_cell_style),
            Paragraph("<b>Google Gemini</b><br/>`text-embedding-004`", table_cell_style),
            Paragraph("OpenAI text-embedding-3,<br/>HuggingFace BGE-large", table_cell_style),
            Paragraph("Generates 768-dimensional dense vector embeddings optimized for semantic retrieval across legal, financial, and logistics terminology.", table_cell_style)
        ],
        [
            Paragraph("Frontend UI", table_cell_style),
            Paragraph("<b>React 18 + TypeScript</b><br/>+ Tailwind CSS", table_cell_style),
            Paragraph("Streamlit, Gradio,<br/>Next.js", table_cell_style),
            Paragraph("Enables a custom 3-tier enterprise dashboard featuring interactive accordions, count pills, collapsible precedent drawers, and a dark-mode supplier counter-offer generator.", table_cell_style)
        ],
        [
            Paragraph("Deployment", table_cell_style),
            Paragraph("<b>Docker Compose</b>", table_cell_style),
            Paragraph("Bare-metal Python,<br/>Kubernetes (k8s)", table_cell_style),
            Paragraph("Guarantees reproducible multi-container deployment across developer environments and enterprise cloud servers with integrated health checks.", table_cell_style)
        ]
    ]
    t_tools = Table(tool_rows, colWidths=[70, 85, 95, 250])
    t_tools.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_tools)
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 3: STEP-BY-STEP BACKEND PIPELINE & EXECUTION LIFECYCLE
    # ---------------------------------------------------------
    story.append(Paragraph("3. Step-by-Step Backend Pipeline & Execution Lifecycle", h1_style))
    story.append(Paragraph(
        "The ingestion and evaluation engine executes through a rigorous multi-stage pipeline:",
        body_style
    ))
    
    steps = [
        ("Step 1: Layout-Aware Document Conversion (Docling)", "When a vendor proposal or baseline MSA is uploaded, `docling.document_converter.DocumentConverter` converts PDF/DOCX files into layout-preserved Markdown trees, keeping section headers (`#`, `##`), nested tables, and page metadata intact."),
        ("Step 2: Dual-Granularity Markdown Chunking", "The text is split into two distinct chunk types: `story` chunks (1000–1500 tokens providing narrative section context) and `criteria` chunks (granular clause parameters such as Payment Terms, Unit Pricing, and Warranty SLAs)."),
        ("Step 3: Dense Vector Embedding & pgvector Storage", "Text chunks pass through `text-embedding-004` generating 768-dimensional dense vectors stored in `document_chunks` table alongside JSONB metadata (`story_id`, `page_number`, `category_tag`) and IVFFlat cosine similarity indexes."),
        ("Step 4: Contextual Vector Retrieval & Precedent Search", "When analyzing a vendor proposal, vector search queries `document_chunks` to retrieve relevant baseline clauses and past vendor precedent benchmarks matching the category (e.g. Activewear, Footwear)."),
        ("Step 5: Grounded Gap Analysis & LLM Extraction", "Retrieved context (`incoming_bid`, `vendor_precedent`, `category_best`) is injected into Gemini 2.5 Flash ($T=0.2$). The LLM extracts explicit deviations and formats output into a strict Pydantic JSON schema."),
        ("Step 6: Multi-Tier UI Rendering & Counter-Offer Generation", "The frontend renders Tier 1 Executive Scorecard, Tier 2 Priority Battlecards, Tier 3 Section Accordions, and auto-synthesizes a Tier 4 Supplier Counter-Offer Letter.")
    ]
    for title, desc in steps:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 4: ANTI-HALLUCINATION GUARDRAILS
    # ---------------------------------------------------------
    story.append(Paragraph("4. Anti-Hallucination & Quality Control Framework", h1_style))
    story.append(Paragraph("To ensure 100% factual reliability in contract reviews, 6 strict safety mechanisms are enforced:", body_style))
    
    guardrails = [
        ("1. Layout Hierarchy Preservation", "IBM Docling extracts exact section titles and paragraph boundaries, preventing split-context errors."),
        ("2. Dual-Anchor Citation Mandate", "LLM system prompts explicitly require citing exact document names and section titles for every gap identified."),
        ("3. Direct Raw Context Window Injection", "Both incoming proposal text and baseline contract text are passed simultaneously in the context window."),
        ("4. Low Temperature Decoding ($T=0.2$)", "Extraction and gap analysis run at deterministic low temperature to eliminate creative hallucinations."),
        ("5. Strict Pydantic JSON Schema Validation", "All LLM outputs are validated against Pydantic models; invalid schema formatting triggers auto-retries."),
        ("6. Cosine Distance Traceability", "Vector search results report exact distance scores (`1.0 - distance`), guaranteeing full audit traceability back to source DB chunks.")
    ]
    for title, desc in guardrails:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 5: VISUALIZATIONS & SOURCING INSIGHTS DELIVERED
    # ---------------------------------------------------------
    story.append(Paragraph("5. Visualizations & Sourcing Insights Delivered", h1_style))
    story.append(Paragraph(
        "The platform UI transforms complex contract analysis into actionable sourcing intelligence across four structured tiers:",
        body_style
    ))
    
    assets_dir = r"C:\Users\metha\OneDrive\Desktop\walmart project\docs\assets"
    img1_path = os.path.join(assets_dir, "dashboard_tier1_tier2.png")
    img2_path = os.path.join(assets_dir, "dashboard_tier3_sections.png")
    img3_path = os.path.join(assets_dir, "dashboard_tier3_expanded_clause.png")
    img4_path = os.path.join(assets_dir, "counter_offer_letter.png")

    # Tier 1 & 2
    story.append(Paragraph("• <b>Tier 1 Executive Scorecard & Tier 2 Priority Negotiation Battlecard</b>", h2_style))
    story.append(Paragraph(
        "Tier 1 displays overall award status (e.g., <i>TARGETED RENEGOTIATION — 81.5 / 100 PTS</i>), weighted sub-scores across domain sections "
        "(SEC-A through SEC-F), and risk callout pills (Working Capital Exposure, Unit Cost Variance vs Best, Lead Time Overage). "
        "Tier 2 lists high-leverage deviations ranked by priority (#1, #2...) with category tags, variance summaries, and collapsible citation drawers "
        "(<i>📜 View Citation & Precedent Benchmark ▼</i>).",
        bullet_style
    ))
    
    img1 = get_scaled_image(img1_path, target_width=470)
    if img1:
        story.append(img1)
        story.append(Paragraph("Figure 1: Tier 1 Executive Scorecard & Tier 2 Priority Negotiation Battlecard UI", caption_style))
    story.append(Spacer(1, 6))

    # Tier 3 Accordions
    story.append(Paragraph("• <b>Tier 3 Section-Wise Analysis Accordions</b>", h2_style))
    story.append(Paragraph(
        "Section accordions default to collapsed (`open = false`), summarizing clause counts across status pills: <b>🟢 Compliant</b>, <b>🟡 Deviation</b>, and <b>🔴 Gap</b>. "
        "Allows category buyers to scan compliance across all contract sections at a glance.",
        bullet_style
    ))
    img2 = get_scaled_image(img2_path, target_width=470)
    if img2:
        story.append(img2)
        story.append(Paragraph("Figure 2: Tier 3 Section-Wise Analysis Accordions View", caption_style))
    story.append(Spacer(1, 6))

    # Tier 3 Expanded
    story.append(Paragraph("• <b>Tier 3 Expanded Clause-Level Detail View</b>", h2_style))
    story.append(Paragraph(
        "Expanding any section accordion reveals granular clause evaluation cards (e.g. `SEC-A.1`, `SEC-A.2`). "
        "Each card delivers: <b>Statement-First Sourcing Insights</b>, <b>Quantitative Variance Deltas vs. Vendor Precedent & Category Best-in-Class</b>, "
        "and interactive <b>Dual-Anchor Evidence Drawer</b> buttons.",
        bullet_style
    ))
    img3 = get_scaled_image(img3_path, target_width=470)
    if img3:
        story.append(img3)
        story.append(Paragraph("Figure 3: Tier 3 Expanded Clause Evaluation Cards & Benchmark Deltas", caption_style))
    story.append(Spacer(1, 6))

    # Tier 4 Counter Letter
    story.append(Paragraph("• <b>Tier 4 Supplier Counter-Offer Letter Generation</b>", h2_style))
    story.append(Paragraph(
        "Generates a formal, executive-ready supplier counter-offer letter ready to copy and send to vendor representatives. "
        "Synthesizes payment term revert mandates, FOB unit cost realignments, commodity price trigger caps, and QA specifications into a polished letter.",
        bullet_style
    ))
    img4 = get_scaled_image(img4_path, target_width=470)
    if img4:
        story.append(img4)
        story.append(Paragraph("Figure 4: Tier 4 Automated Supplier Counter-Offer Letter Generator", caption_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 6: DATABASE SCHEMA & INSPECTION
    # ---------------------------------------------------------
    story.append(Paragraph("6. Database Schema & Inspection Commands", h1_style))
    story.append(Paragraph(
        "The system utilizes PostgreSQL 16 with the `pgvector` extension. Core schema definition for `document_chunks`:",
        body_style
    ))
    
    schema_rows = [
        [Paragraph("<b>Column Name</b>", table_header_style), Paragraph("<b>Data Type</b>", table_header_style), Paragraph("<b>Description & Constraints</b>", table_header_style)],
        [Paragraph("`chunk_id`", table_cell_style), Paragraph("UUID (Primary Key)", table_cell_style), Paragraph("Unique identifier for each document chunk.", table_cell_style)],
        [Paragraph("`chunk_type`", table_cell_style), Paragraph("VARCHAR(20)", table_cell_style), Paragraph("Chunk classification (`story` or `criteria`).", table_cell_style)],
        [Paragraph("`content`", table_cell_style), Paragraph("TEXT", table_cell_style), Paragraph("Extracted section or clause markdown text.", table_cell_style)],
        [Paragraph("`embedding`", table_cell_style), Paragraph("vector(768)", table_cell_style), Paragraph("Gemini 768-dimensional vector with IVFFlat index.", table_cell_style)],
        [Paragraph("`story_id`", table_cell_style), Paragraph("UUID", table_cell_style), Paragraph("Parent document relation ID.", table_cell_style)],
        [Paragraph("`metadata`", table_cell_style), Paragraph("JSONB", table_cell_style), Paragraph("Page numbers, section headings, document title, category tag.", table_cell_style)],
        [Paragraph("`source_path`", table_cell_style), Paragraph("TEXT", table_cell_style), Paragraph("Original file path or upload filename.", table_cell_style)]
    ]
    t_schema = Table(schema_rows, colWidths=[100, 120, 260])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("<b>Live Database Inspection Command:</b>", h2_style))
    db_cmd_text = "docker exec -it rag-db-1 psql -U postgres -d rag_db -c \"SELECT chunk_id, chunk_type, source_path FROM document_chunks LIMIT 5;\""
    story.append(Paragraph(f"<code>{db_cmd_text}</code>", code_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 7: DISCLAIMER & CONFIDENTIALITY NOTICE
    # ---------------------------------------------------------
    story.append(Paragraph("7. Disclaimer & Confidentiality Notice", h1_style))
    
    disc_box_data = [[
        Paragraph(
            "<b>⚠️ INDEPENDENT PORTFOLIO PROJECT DISCLAIMER</b><br/>"
            "This document and repository represent an independent technical portfolio demonstration project. It is <b>not</b> an officially "
            "sponsored, endorsed, or affiliated product of Walmart Inc., its subsidiaries, or any named vendor.<br/><br/>"
            "<b>100% SYNTHETIC MOCK DATA:</b> All contract documents, vendor proposals (e.g. Apex Sportswear Global Ltd.), Service Level Agreements (SLAs), "
            "pricing sheets, and evaluation outputs contained within this report are <b>entirely synthetic mock data</b> engineered solely for portfolio "
            "demonstration purposes.<br/><br/>"
            "<b>ZERO PROPRIETARY DATA:</b> This project contains <b>no proprietary Walmart Master Sourcing Agreements (MSAs)</b>, actual supplier pricing, "
            "trade secrets, confidential business data, or non-public internal information of any kind.",
            table_cell_style
        )
    ]]
    t_disc = Table(disc_box_data, colWidths=[480])
    t_disc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")), # Amber tint
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D97706")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_disc)
    story.append(Spacer(1, 10))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete:", output_filename)

if __name__ == '__main__':
    desktop_pdf = r"C:\Users\metha\OneDrive\Desktop\Walmart_Sourcing_Intelligence_Platform_Comprehensive_Report.pdf"
    repo_pdf = r"C:\Users\metha\OneDrive\Desktop\walmart project\docs\reports\Walmart_Sourcing_Intelligence_Platform_Comprehensive_Report.pdf"
    
    build_pdf(desktop_pdf)
    build_pdf(repo_pdf)

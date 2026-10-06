import os
import sys
import shutil
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

class MasterNumberedCanvas(canvas.Canvas):
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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Walmart Sourcing Intelligence Platform — Master Technical Architecture & Engineering Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL — INDEPENDENT TECHNICAL PORTFOLIO REPORT (SYNTHETIC DATA)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def get_scaled_image(path, target_width=475):
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

def build_master_pdf(output_filename):
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
    DARK = colors.HexColor("#0F172A")       # Body Text
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Table / Callout Background
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    CODE_BG = colors.HexColor("#F1F5F9")
    
    title_style = ParagraphStyle(
        'MasterTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'MasterSubtitle',
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
        spaceBefore=14,
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
        spaceBefore=10,
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
    
    code_block_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
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
    # COVER / HEADER
    # ---------------------------------------------------------
    story.append(Spacer(1, 4))
    story.append(Paragraph("Walmart Sourcing & Procurement Intelligence Platform", title_style))
    story.append(Paragraph("Master Engineering Blueprint, Tool Rationale, Full System Prompts & Execution Lifecycles", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceBefore=0, spaceAfter=10))
    
    meta_data = [
        [Paragraph("<b>Author / Engineer:</b> Metharun Venkat", table_cell_style), Paragraph("<b>Parsing Engine:</b> IBM Docling (`DocumentConverter`)", table_cell_style)],
        [Paragraph("<b>Vector Database:</b> PostgreSQL 16 + pgvector", table_cell_style), Paragraph("<b>LLM Backend:</b> Google Gemini 2.5 Flash ($T=0.2$)", table_cell_style)],
        [Paragraph("<b>Embedding Model:</b> text-embedding-004 (768d)", table_cell_style), Paragraph("<b>Repository:</b> `metharunvenkat-ctrl/walmart-sourcing...`", table_cell_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 250])
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
    # SECTION 1: EXECUTIVE OVERVIEW & BUSINESS OBJECTIVES
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Overview & Strategic Objectives", h1_style))
    story.append(Paragraph(
        "In global retail private-brand category management (e.g., Walmart's George, Athletic Works, Time and Tru), evaluating vendor RFPs against "
        "master procurement baselines and historical supplier precedents is a complex, time-critical challenge. Sourcing managers regularly evaluate "
        "50+ page vendor proposals containing subtle commercial, operational, and legal variances—such as Net 60 vs. Net 90 payment terms, reduced "
        "Defective Merchandise Allowances (DMA), uncapped liability limits, or extended lead times.",
        body_style
    ))
    story.append(Paragraph(
        "Manual contract evaluation takes several business days per supplier submission, introducing human oversight risks and uncaptured negotiation leverage. "
        "The <b>Walmart Sourcing & Procurement Intelligence Platform</b> automates side-by-side contract evaluation, gap detection, precedent benchmarking, "
        "and priority negotiation battlecard synthesis—reducing review cycles from days to under <b>60 seconds</b> with 100% grounded clause traceability.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # SECTION 2: TOOL SELECTION & ARCHITECTURAL TRADE-OFF ANALYSIS
    # ---------------------------------------------------------
    story.append(Paragraph("2. Tool Selection & Comparative Trade-off Analysis", h1_style))
    story.append(Paragraph(
        "Every architectural decision was made following rigorous evaluation of open-source and cloud alternatives to ensure high layout precision, "
        "data privacy, execution speed, and enterprise scalability:",
        body_style
    ))
    
    tools_table = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Selected Tool</b>", table_header_style), Paragraph("<b>Alternatives Considered</b>", table_header_style), Paragraph("<b>Detailed Selection Rationale & Comparative Advantages</b>", table_header_style)],
        [
            Paragraph("Document Parser", table_cell_style),
            Paragraph("<b>IBM Docling</b><br/>(`DocumentConverter`)", table_cell_style),
            Paragraph("PyPDF, Unstructured,<br/>LlamaIndex, PDFMiner", table_cell_style),
            Paragraph("Docling natively parses document layout trees, preserving multi-page table structures, section headings, and header/footer metadata. Standard PDF parsers flatten text streams, corrupting nested financial tables and clause boundaries.", table_cell_style)
        ],
        [
            Paragraph("Vector Store", table_cell_style),
            Paragraph("<b>PostgreSQL 16</b><br/>+ `pgvector`", table_cell_style),
            Paragraph("Pinecone, ChromaDB,<br/>Milvus, Qdrant", table_cell_style),
            Paragraph("Eliminates external SaaS API costs and data privacy concerns. Unifies dense vector similarity search (`vector(768)` with IVFFlat cosine indexing) and relational metadata (`JSONB`) inside a single ACID-compliant database.", table_cell_style)
        ],
        [
            Paragraph("LLM Engine", table_cell_style),
            Paragraph("<b>Google Gemini 2.5 Flash</b><br/>($T=0.2$)", table_cell_style),
            Paragraph("OpenAI GPT-4o,<br/>Local Ollama Llama-3", table_cell_style),
            Paragraph("1M token context window allows full document pair injection (baseline + incoming bid + precedent context simultaneously). Delivers rapid execution and strict JSON schema enforcement via Pydantic model validation.", table_cell_style)
        ],
        [
            Paragraph("Embedding Model", table_cell_style),
            Paragraph("<b>Google Gemini</b><br/>`text-embedding-004`", table_cell_style),
            Paragraph("OpenAI text-embedding-3,<br/>HuggingFace BGE-large", table_cell_style),
            Paragraph("Generates 768-dimensional dense vector embeddings optimized for semantic retrieval across specialized legal, financial, and supply chain procurement terminology.", table_cell_style)
        ],
        [
            Paragraph("Frontend UI", table_cell_style),
            Paragraph("<b>React 18 + TypeScript</b><br/>+ Tailwind CSS", table_cell_style),
            Paragraph("Streamlit, Gradio,<br/>Next.js", table_cell_style),
            Paragraph("Enables a responsive 3-tier enterprise dashboard featuring interactive section accordions, status count pills, collapsible precedent drawers, and a dark-mode supplier counter-offer generator.", table_cell_style)
        ],
        [
            Paragraph("Deployment", table_cell_style),
            Paragraph("<b>Docker Compose</b>", table_cell_style),
            Paragraph("Bare-metal Python,<br/>Kubernetes (k8s)", table_cell_style),
            Paragraph("Guarantees reproducible multi-container deployment across developer laptops and cloud infrastructure with integrated container health checks.", table_cell_style)
        ]
    ]
    t_tools = Table(tools_table, colWidths=[70, 85, 95, 250])
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
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 3: STEP-BY-STEP BACKEND PIPELINE LIFECYCLE
    # ---------------------------------------------------------
    story.append(Paragraph("3. Step-by-Step Backend Execution Lifecycle", h1_style))
    story.append(Paragraph(
        "The RAG ingestion and evaluation engine operates through six distinct execution phases:",
        body_style
    ))
    
    steps = [
        ("Step 1: Layout-Aware Document Parsing (Docling)", "When a vendor proposal or baseline MSA is uploaded, `docling.document_converter.DocumentConverter` extracts document structure into clean Markdown trees, keeping section headers (`#`, `##`), nested tables, and page metadata intact."),
        ("Step 2: Dual-Granularity Markdown Chunking", "Text is divided into two distinct chunk types: `story` chunks (1000–1500 tokens providing narrative section context) and `criteria` chunks (granular clause parameters such as Payment Terms, Unit Pricing, and Warranty SLAs)."),
        ("Step 3: Vector Embedding & pgvector Storage", "Chunks pass through `text-embedding-004` producing 768-dimensional dense vectors stored in `document_chunks` table alongside JSONB metadata (`story_id`, `page_number`, `category_tag`) and IVFFlat cosine similarity indexes."),
        ("Step 4: Hybrid Context Retrieval & Precedent Search", "When evaluating a vendor proposal, vector search queries `document_chunks` to retrieve relevant baseline clauses and past vendor precedent benchmarks matching the category (e.g. Activewear, Footwear)."),
        ("Step 5: Grounded Gap Analysis & LLM Extraction", "Retrieved context (`incoming_bid`, `vendor_precedent`, `category_best`) is injected into Gemini 2.5 Flash ($T=0.2$). The LLM extracts explicit deviations and formats output into a strict Pydantic JSON schema."),
        ("Step 6: Tiered UI Visualization & Counter-Offer Generation", "The frontend renders Tier 1 Executive Scorecard, Tier 2 Priority Battlecards, Tier 3 Section Accordions, and auto-synthesizes a Tier 4 Supplier Counter-Offer Letter.")
    ]
    for title, desc in steps:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 4: ANTI-HALLUCINATION & RELIABILITY GUARDRAILS
    # ---------------------------------------------------------
    story.append(Paragraph("4. Anti-Hallucination & Quality Control Framework", h1_style))
    story.append(Paragraph("To guarantee 100% factual reliability in contract reviews, 6 strict safety mechanisms are enforced:", body_style))
    
    guardrails = [
        ("1. Layout Hierarchy Preservation", "IBM Docling extracts exact section titles and paragraph boundaries, eliminating artificial text split errors."),
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
    # SECTION 5: FULL PRODUCTION SYSTEM PROMPTS
    # ---------------------------------------------------------
    story.append(Paragraph("5. Full Production System Prompts", h1_style))
    story.append(Paragraph(
        "Below are verbatim representations of the production system prompts that govern document classification, gap analysis extraction, and RAG conversational answers:",
        body_style
    ))
    
    # GAP ANALYSIS PROMPT BLOCK
    story.append(Paragraph("<b>5.1 `GAP_ANALYSIS_PROMPT` (Contract Gap Evaluation & Tier 1-4 Generation):</b>", h2_style))
    gap_prompt_text = (
        "You are an expert Strategic Sourcing Intelligence & Contract Analytics Agent specializing in retail private-brand fashion procurement.\n"
        "Your role is to evaluate incoming vendor proposal clauses by benchmarking them simultaneously against two historical reference points:\n"
        "1. Vendor Self-Precedent (Incumbent Track Record): Prior contract terms agreed to by this specific supplier.\n"
        "2. Category Best-in-Class (Competitive Benchmark): Most favorable terms executed across any supplier for this category.\n\n"
        "## MANDATORY RULES:\n"
        "- LOGISTICS & TURNAROUND: Do NOT mark differing Port of Loading names as critical gaps. Classify 5-15 day lead-time overages as deviations.\n"
        "- TIER 1: Assign award_status (ACCEPT WITH CONDITIONS | TARGETED RENEGOTIATION | DISQUALIFIED). Calculate 100-pt scorecard & macro exposure.\n"
        "- TIER 2: Rank top 3-5 priority deviations into priority, clause_id, clause_title, deviation_summary, impact_badge, cited_anchors. Exclude leverage/counter-position boxes.\n"
        "- TIER 3: 1-2 sentence statement-first insights leading with numbers (%, days, $). Include evidence drawers with incoming_bid, vendor_precedent, category_best.\n"
        "- TIER 4: Complete, formal supplier counter-offer letter ready to send.\n\n"
        "STRICT JSON OUTPUT SCHEMA:\n"
        "{\n"
        "  \"tier_1_summary\": {\n"
        "    \"award_status\": \"TARGETED RENEGOTIATION\",\n"
        "    \"total_score\": 81.5, \"max_score\": 100,\n"
        "    \"section_scores\": {\n"
        "      \"section_A\": { \"earned\": 9.5, \"max\": 10 }, \"section_B\": { \"earned\": 14.0, \"max\": 15 },\n"
        "      \"section_C\": { \"earned\": 32.0, \"max\": 40 }, \"section_D\": { \"earned\": 26.0, \"max\": 35 },\n"
        "      \"section_E\": { \"status\": \"Complete\" }, \"section_F\": { \"status\": \"Pass\" }\n"
        "    },\n"
        "    \"macro_exposure\": {\n"
        "      \"working_capital_impact\": \"-30 days float drag\",\n"
        "      \"cost_variance_vs_category_best\": \"+$0.35/unit (+7.6%)\",\n"
        "      \"lead_time_variance\": \"+10 to +15 calendar days over standard SLA\"\n"
        "    }\n"
        "  },\n"
        "  \"tier_2_battlecard\": [ {\n"
        "    \"priority\": 1, \"clause_id\": \"FIN-D.3\", \"clause_title\": \"Settlement Terms & Standard Allowances\",\n"
        "    \"deviation_summary\": \"Vendor bids Net 60 days (vs Net 90) and discounts DMA to 1.5% (vs 2.0%).\",\n"
        "    \"impact_badge\": \"-30 Days Float Drag | -50 bps DMA Allowance\",\n"
        "    \"cited_anchors\": { \"vendor_precedent_doc\": \"...\", \"category_baseline_doc\": \"...\" }\n"
        "  } ],\n"
        "  \"tier_3_clause_matrix\": [ {\n"
        "    \"clause_id\": \"SEC-A.1\", \"verdict\": \"compliant\",\n"
        "    \"insight_statement\": \"Vendor provides complete corporate entity registration and valid EPB export license.\",\n"
        "    \"quantitative_deltas\": { \"vs_vendor_precedent\": \"Fully matched entity profile\", \"vs_category_best\": \"Fully compliant corporate status\" },\n"
        "    \"evidence\": { \"incoming_bid\": {...}, \"vendor_precedent\": {...}, \"category_best\": {...} }\n"
        "  } ],\n"
        "  \"tier_4_counter_letter\": \"Dear Mr. Chowdhury,...\"\n"
        "}"
    )
    t_gap_prompt = Table([[Paragraph(f"<code>{gap_prompt_text.replace(chr(10), '<br/>')}</code>", code_block_style)]], colWidths=[480])
    t_gap_prompt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_gap_prompt)
    story.append(Spacer(1, 8))

    # INGESTION PROMPT BLOCK
    story.append(Paragraph("<b>5.2 `INGESTION_PROMPT` (Document Classification & Markdown Ingestion):</b>", h2_style))
    ingest_prompt_text = (
        "You are a procurement document intelligence engine. Read raw markdown of vendor proposals, baseline RFPs, or historical awards and return a single JSON object.\n"
        "TAXONOMY:\n"
        "- document_type: baseline_rfp | vendor_bid | historical_award\n"
        "- department: Mens | Womens | Kids | Unisex | General\n"
        "- product_category: Topwear | Bottomwear | Footwear | Sports_Activewear | Accessories | Innerwear_Loungewear | Kids_Wear | General\n"
        "- section_letter & section_name: A (Qualifications, weight 10), B (Past Involvement, weight 15), C (Proposed Work Plan, weight 40), D (Fee Proposal, weight 35), E (Authorized Negotiator, weight 0), F (Attachments, weight 0)\n"
        "- clause_type: technical | commercial | logistics | compliance | qualification | administrative\n"
        "CHUNKING: Break sections into discrete evaluable units (SPEC-C.1, LOG-C.3, FIN-D.1, FIN-D.3...). Preserve exact numeric figures and tolerances."
    )
    t_ingest_prompt = Table([[Paragraph(f"<code>{ingest_prompt_text.replace(chr(10), '<br/>')}</code>", code_block_style)]], colWidths=[480])
    t_ingest_prompt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ingest_prompt)
    story.append(Spacer(1, 8))

    # CHAT PROMPT BLOCK
    story.append(Paragraph("<b>5.3 `CHAT_PROMPT` (Interactive Contextual RAG Sourcing Assistant):</b>", h2_style))
    chat_prompt_text = (
        "You are a helpful assistant for analyzing requirements documents.\n"
        "Answer the user's question based ONLY on the following context from the knowledge base.\n"
        "If the context doesn't contain enough information to answer, say so clearly.\n"
        "Always reference which document and story your answer comes from.\n\n"
        "CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nAnswer in plain text format (no JSON encapsulation)."
    )
    t_chat_prompt = Table([[Paragraph(f"<code>{chat_prompt_text.replace(chr(10), '<br/>')}</code>", code_block_style)]], colWidths=[480])
    t_chat_prompt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_chat_prompt)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 6: VISUALIZATIONS & SOURCING INSIGHTS DELIVERED
    # ---------------------------------------------------------
    story.append(Paragraph("6. Visualizations & Sourcing Insights Delivered", h1_style))
    story.append(Paragraph(
        "The frontend user interface transforms complex contract analysis into actionable sourcing intelligence across four structured tiers:",
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
    # SECTION 7: DATABASE SCHEMA & INSPECTION
    # ---------------------------------------------------------
    story.append(Paragraph("7. Database Schema & Inspection Commands", h1_style))
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
    story.append(Paragraph(f"<code>{db_cmd_text}</code>", code_block_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 8: DISCLAIMER & CONFIDENTIALITY NOTICE
    # ---------------------------------------------------------
    story.append(Paragraph("8. Disclaimer & Confidentiality Notice", h1_style))
    
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
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D97706")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_disc)
    story.append(Spacer(1, 10))

    doc.build(story, canvasmaker=MasterNumberedCanvas)
    print("Master PDF build complete:", output_filename)

if __name__ == '__main__':
    desktop_pdf = r"C:\Users\metha\OneDrive\Desktop\Walmart_Sourcing_Intelligence_Platform_Master_Report.pdf"
    repo_pdf = r"C:\Users\metha\OneDrive\Desktop\walmart project\docs\reports\Walmart_Sourcing_Intelligence_Platform_Master_Report.pdf"
    
    build_master_pdf(desktop_pdf)
    build_master_pdf(repo_pdf)

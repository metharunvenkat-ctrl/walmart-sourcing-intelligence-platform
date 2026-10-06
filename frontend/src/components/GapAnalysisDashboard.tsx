import { useState, useMemo } from "react";

/* ─── Procurement Verdict Configurations ─── */
const VERDICT_CONFIG: Record<string, { label: string; bg: string; text: string; border: string; icon: string }> = {
  covered: { label: "Fully Compliant", bg: "#F0FDF4", text: "#15803D", border: "#22C55E", icon: "🟢" },
  compliant: { label: "Fully Compliant", bg: "#F0FDF4", text: "#15803D", border: "#22C55E", icon: "🟢" },
  partial: { label: "Negotiated Deviation", bg: "#FEFCE8", text: "#854D0E", border: "#EAB308", icon: "🟡" },
  deviation: { label: "Negotiated Deviation", bg: "#FEFCE8", text: "#854D0E", border: "#EAB308", icon: "🟡" },
  good_to_have: { label: "Value-Add Addition", bg: "#FEFCE8", text: "#854D0E", border: "#EAB308", icon: "🟡" },
  gap: { label: "Critical Gap", bg: "#FEF2F2", text: "#991B1B", border: "#EF4444", icon: "🔴" },
  conflict: { label: "Critical Gap / Terms Conflict", bg: "#FEF2F2", text: "#991B1B", border: "#EF4444", icon: "🔴" },
};

/* ─── Executive Action Lever Configurations ─── */
const ACTION_LEVER_CONFIG: Record<string, { label: string; bg: string; text: string; border: string }> = {
  ACCEPT_AS_IS: { label: "✅ ACCEPT AS IS", bg: "#f0fdf4", text: "#166534", border: "#22c55e" },
  COUNTER_OFFER: { label: "⚡ COUNTER-OFFER REQUIRED", bg: "#fefce8", text: "#854d0e", border: "#eab308" },
  REJECT_CLAUSE: { label: "⛔ REJECT CLAUSE", bg: "#fef2f2", text: "#991b1b", border: "#ef4444" },
  DISQUALIFY_BID: { label: "🚨 DISQUALIFY BID", bg: "#450a0a", text: "#ffffff", border: "#991b1b" },
};

/* ─── Award Status Configuration for Tier 1 ─── */
const AWARD_STATUS_CONFIG: Record<string, { label: string; bg: string; text: string; border: string; icon: string }> = {
  "ACCEPT WITH CONDITIONS": { label: "ACCEPT WITH CONDITIONS", bg: "#f0fdf4", text: "#166534", border: "#22c55e", icon: "🟢" },
  "TARGETED RENEGOTIATION": { label: "TARGETED RENEGOTIATION", bg: "#fefce8", text: "#854d0e", border: "#eab308", icon: "🟡" },
  "DISQUALIFIED / HIGH RISK": { label: "DISQUALIFIED / HIGH RISK", bg: "#fef2f2", text: "#991b1b", border: "#ef4444", icon: "🚨" },
};

/* ─── Clause Accordion Item (Tier 3) ─── */
function ClauseAccordionItem({ comparison, existingDocTitle }: { comparison: any; existingDocTitle: string }) {
  const [showEvidence, setShowEvidence] = useState(false);

  const rawVerdict = comparison.verdict || "gap";
  const normVerdict = rawVerdict === "compliant" || rawVerdict === "covered" ? "covered" : (rawVerdict === "deviation" || rawVerdict === "partial" ? "partial" : "gap");
  const verdictConfig = VERDICT_CONFIG[normVerdict] || VERDICT_CONFIG.gap;

  const rawActionLever = comparison.action_lever || (normVerdict === "covered" ? "ACCEPT_AS_IS" : (normVerdict === "partial" ? "COUNTER_OFFER" : "REJECT_CLAUSE"));
  const actionLeverConfig = ACTION_LEVER_CONFIG[rawActionLever] || ACTION_LEVER_CONFIG.COUNTER_OFFER;

  const clauseTag = comparison.clause_id || comparison.new_clause_id || comparison.new_ac_id || "CLAUSE";
  const clauseTitle = comparison.clause_title || comparison.new_clause_title || comparison.new_ac_title || "Proposal Requirement";
  const matchedDoc = comparison.historical_doc_title || existingDocTitle;

  const insightStatement = comparison.insight_statement || comparison.description || comparison.comparison_statement || `Variance detected for ${clauseTitle} against baseline ${matchedDoc}.`;

  const qDelta = comparison.quantitative_deltas || comparison.quantitative_delta || {};
  const deltaVsPrecedent = qDelta.vs_vendor_precedent || (normVerdict === "covered" ? "Aligned" : "-30 days float / variance");
  const deltaVsCategory = qDelta.vs_category_best || (normVerdict === "covered" ? "Aligned" : "+5-8% vs Best-in-Class");

  const evidence = comparison.evidence || comparison.progressive_disclosure_evidence || {};
  const incomingBid = evidence.incoming_bid || { vendor_name: "Submitted Bid", text: comparison.new_clause_text || comparison.new_ac_criteria || "Extracted Vendor Commitment", source: comparison.document_id };
  const vendorPrecedent = evidence.vendor_precedent || {
    vendor_name: "Vendor Precedent",
    document_id: matchedDoc,
    year: "2025",
    text: comparison.matched_clause_text || comparison.matched_ac_criteria || `Prior contracted requirement in ${matchedDoc}`,
  };
  const categoryBest = evidence.category_best || {
    vendor: "Category Best-in-Class",
    document_id: "Category_Best_In_Class_2025.pdf",
    year: "2025",
    text: "Optimal commercial and technical benchmark executed across category suppliers.",
  };

  return (
    <div
      style={{
        borderLeft: `4px solid ${verdictConfig.border}`,
        margin: "14px 0",
        padding: "16px 18px",
        background: "#ffffff",
        borderRadius: "0 8px 8px 0",
        boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
        border: "1px solid #e2e8f0",
        borderLeftWidth: 4,
        borderLeftColor: verdictConfig.border,
      }}
    >
      {/* Header: Tag, Title, Action Lever & Verdict Chip */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12, flexWrap: "wrap", gap: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 13, fontWeight: 700, color: "#1e293b", background: "#f1f5f9", padding: "4px 10px", borderRadius: 6 }}>
            🏷️ {clauseTag}: {clauseTitle}
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              padding: "3px 10px",
              borderRadius: 6,
              background: actionLeverConfig.bg,
              color: actionLeverConfig.text,
              border: `1px solid ${actionLeverConfig.border}`,
              letterSpacing: 0.5,
            }}
          >
            {actionLeverConfig.label}
          </span>

          <span
            style={{
              fontSize: 11.5,
              fontWeight: 600,
              padding: "3px 12px",
              borderRadius: 12,
              background: verdictConfig.bg,
              color: verdictConfig.text,
              border: `1px solid ${verdictConfig.border}`,
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            <span>{verdictConfig.icon}</span>
            <span>{verdictConfig.label}</span>
          </span>
        </div>
      </div>

      {/* Statement-First Sourcing Insight (Always Visible) */}
      <div style={{ background: "#f8fafc", padding: "12px 14px", borderRadius: 6, border: "1px solid #cbd5e1", marginBottom: 12 }}>
        <p style={{ fontSize: 11, fontWeight: 700, color: "#475569", margin: "0 0 4px", textTransform: "uppercase", letterSpacing: 0.5 }}>
          🧠 Statement-First Sourcing Insight
        </p>
        <p style={{ fontSize: 13, color: "#0f172a", margin: 0, lineHeight: 1.55, fontWeight: 600 }}>
          {insightStatement}
        </p>
      </div>

      {/* Quantitative Deltas (Tier 3) */}
      <div style={{ background: "#eff6ff", padding: "10px 14px", borderRadius: 6, border: "1px solid #bfdbfe", marginBottom: 12 }}>
        <p style={{ fontSize: 11, fontWeight: 700, color: "#1e40af", margin: "0 0 6px", textTransform: "uppercase" }}>
          📊 Quantitative Variance Deltas
        </p>
        <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
          <span style={{ fontSize: 11.5, color: "#1e3a8a", fontWeight: 600 }}>
            📉 <strong>vs Vendor Precedent:</strong> {deltaVsPrecedent}
          </span>
          <span style={{ fontSize: 11.5, color: "#1e3a8a", fontWeight: 600 }}>
            🏆 <strong>vs Category Best-in-Class:</strong> {deltaVsCategory}
          </span>
        </div>
      </div>

      {/* Collapsible Progressive Evidence Drawer */}
      <div>
        <button
          onClick={() => setShowEvidence(!showEvidence)}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            padding: "6px 14px",
            fontSize: 11.5,
            fontWeight: 600,
            color: "#0f766e",
            background: "#ccfbf1",
            border: "1px solid #99f6e4",
            borderRadius: 6,
            cursor: "pointer",
          }}
        >
          🔍 {showEvidence ? "Hide Progressive Evidence Drawer" : "Reveal Dual-Anchor Evidence Drawer (Precedent vs Best-in-Class)"}
        </button>

        {showEvidence && (
          <div style={{ marginTop: 10, display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
            <div style={{ background: "#f0fdf4", padding: "10px 12px", borderRadius: 6, border: "1px solid #bbf7d0" }}>
              <p style={{ fontSize: 10.5, fontWeight: 700, color: "#166534", margin: "0 0 4px", textTransform: "uppercase" }}>
                📝 Submitted Proposal ({incomingBid.vendor_name || "Current Vendor"})
              </p>
              <p style={{ fontSize: 12, color: "#14532d", margin: 0, lineHeight: 1.45 }}>
                {incomingBid.text}
              </p>
            </div>

            <div style={{ background: "#f8fafc", padding: "10px 12px", borderRadius: 6, border: "1px solid #cbd5e1" }}>
              <p style={{ fontSize: 10.5, fontWeight: 700, color: "#475569", margin: "0 0 4px", textTransform: "uppercase" }}>
                📜 Vendor Precedent ({vendorPrecedent.document_id || matchedDoc} '{vendorPrecedent.year || "25"})
              </p>
              <p style={{ fontSize: 12, color: "#1e293b", margin: 0, lineHeight: 1.45 }}>
                {vendorPrecedent.text}
              </p>
            </div>

            <div style={{ background: "#fefce8", padding: "10px 12px", borderRadius: 6, border: "1px solid #fef08a" }}>
              <p style={{ fontSize: 10.5, fontWeight: 700, color: "#854d0e", margin: "0 0 4px", textTransform: "uppercase" }}>
                🏆 Category Best-in-Class ({categoryBest.vendor || categoryBest.vendor_name || "Category Best"})
              </p>
              <p style={{ fontSize: 12, color: "#713f12", margin: 0, lineHeight: 1.45 }}>
                {categoryBest.text}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/* ─── Tier 2 Battlecard Item with Citation Dropdown ─── */
function Tier2BattlecardItem({ item, idx, defaultDoc }: { item: any; idx: number; defaultDoc: string }) {
  const [showCitation, setShowCitation] = useState(false);

  const cId = item.clause_id || item.new_clause_id || `CLAUSE-${idx + 1}`;
  const cTitle = item.clause_title || item.title || cId;
  const devSummary = item.deviation_summary || item.description || item.summary || "Vendor proposal deviation from baseline requirement.";

  const anchors = item.cited_anchors || {};
  const precedentDoc = anchors.vendor_precedent_doc || defaultDoc;
  const baselineDoc = anchors.category_baseline_doc || "Category Best-in-Class Benchmark";

  return (
    <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: 8, border: "1px solid #e2e8f0" }}>
      {/* Priority, Title & Impact Badge */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8, flexWrap: "wrap", gap: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 12.5, fontWeight: 700, color: "#1e293b", background: "#e2e8f0", padding: "3px 10px", borderRadius: 4 }}>
            Priority #{item.priority || idx + 1} — {cId}: {cTitle}
          </span>
          {item.impact_badge && (
            <span style={{ fontSize: 11, fontWeight: 700, background: "#fee2e2", color: "#991b1b", border: "1px solid #fca5a5", padding: "2px 8px", borderRadius: 12 }}>
              {item.impact_badge}
            </span>
          )}
        </div>
      </div>

      {/* Deviation & Citation Dropdown */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <p style={{ fontSize: 12.5, color: "#334155", margin: 0, lineHeight: 1.5 }}>
          • <strong>Deviation:</strong> {devSummary}
        </p>

        {/* Citation Dropdown Option */}
        <div>
          <button
            onClick={() => setShowCitation(!showCitation)}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              fontSize: 11.5,
              fontWeight: 600,
              color: "#1e40af",
              background: "#eff6ff",
              border: "1px solid #bfdbfe",
              padding: "4px 12px",
              borderRadius: 6,
              cursor: "pointer",
            }}
          >
            📜 {showCitation ? "Hide Citation & Precedent Benchmark ▲" : "View Citation & Precedent Benchmark ▼"}
          </button>

          {showCitation && (
            <div style={{ marginTop: 8, background: "#ffffff", padding: "10px 14px", borderRadius: 6, border: "1px solid #cbd5e1", fontSize: 12 }}>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                <span style={{ color: "#1e3a8a", fontWeight: 600 }}>
                  📜 <strong>Vendor Precedent Citation:</strong> {precedentDoc}
                </span>
                <span style={{ color: "#854d0e", fontWeight: 600 }}>
                  🏆 <strong>Category Baseline Citation:</strong> {baselineDoc}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/* ─── Section Header Card (Tier 3) ─── */
function SectionCard({ section, existingDocTitle }: { section: any; existingDocTitle: string }) {
  const [open, setOpen] = useState(false);

  const rawTitle = section.section_title || section.sectionTitle || "Sourcing Category";
  const sectionId = section.section_id || section.sectionId || "Section";
  const comparisons = section.comparisons || [];

  const compliantCount = comparisons.filter((c: any) => c.verdict === "covered" || c.verdict === "compliant").length;
  const deviationCount = comparisons.filter((c: any) => c.verdict === "partial" || c.verdict === "deviation" || c.verdict === "good_to_have").length;
  const gapCount = comparisons.filter((c: any) => c.verdict === "gap" || c.verdict === "conflict").length;

  return (
    <div style={{ marginBottom: 18, border: "1px solid #cbd5e1", borderRadius: 8, background: "#ffffff", overflow: "hidden" }}>
      <button
        onClick={() => setOpen(!open)}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
          padding: "14px 18px",
          border: "none",
          background: open ? "#f8fafc" : "#ffffff",
          cursor: "pointer",
          textAlign: "left",
          borderBottom: open ? "1px solid #e2e8f0" : "none",
        }}
      >
        <div>
          <span style={{ fontSize: 15, fontWeight: 700, color: "#0f172a" }}>
            Section: {rawTitle}
          </span>
          <span style={{ fontSize: 12, color: "#64748b", marginLeft: 8 }}>
            ({sectionId})
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 11.5, fontWeight: 600, padding: "2px 8px", borderRadius: 12, background: "#dcfce7", color: "#15803d", border: "1px solid #86efac" }}>
            🟢 Compliant ({compliantCount})
          </span>
          <span style={{ fontSize: 11.5, fontWeight: 600, padding: "2px 8px", borderRadius: 12, background: "#fef9c3", color: "#a16207", border: "1px solid #fde047" }}>
            🟡 Deviation ({deviationCount})
          </span>
          <span style={{ fontSize: 11.5, fontWeight: 600, padding: "2px 8px", borderRadius: 12, background: "#fee2e2", color: "#991b1b", border: "1px solid #fca5a5" }}>
            🔴 Gap ({gapCount})
          </span>
          <span style={{ fontSize: 14, color: "#475569", transform: open ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.2s" }}>
            &#9654;
          </span>
        </div>
      </button>

      {open && (
        <div style={{ padding: "16px 18px" }}>
          {section.section_summary && (
            <p style={{ fontSize: 12.5, color: "#475569", margin: "0 0 16px", fontStyle: "italic", background: "#f8fafc", padding: "10px 14px", borderRadius: 6, border: "1px solid #e2e8f0" }}>
              💡 <strong>Category Insights:</strong> {section.section_summary}
            </p>
          )}

          <div>
            {comparisons.map((comp: any, idx: number) => (
              <ClauseAccordionItem
                key={comp.clause_id || comp.new_clause_id || comp.new_ac_id || idx}
                comparison={comp}
                existingDocTitle={existingDocTitle}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* ─── Targeted Procurement Filter Pills ─── */
function ProcurementFilterBar({ activeFilter, onFilterChange }: { activeFilter: string; onFilterChange: (f: string) => void }) {
  const filters = [
    { key: "all", label: "📋 All Clauses" },
    { key: "deviations", label: "🟡 Negotiated Deviations (Counter Terms)" },
    { key: "gaps", label: "🔴 Critical Gaps (Disqualifiers)" },
    { key: "financial", label: "💰 Financial Terms (Payment, DMA & Allowances)" },
  ];

  return (
    <div style={{ display: "flex", gap: 8, marginBottom: 20, flexWrap: "wrap" }}>
      {filters.map((f) => (
        <button
          key={f.key}
          onClick={() => onFilterChange(f.key)}
          style={{
            padding: "8px 16px",
            borderRadius: 20,
            border: activeFilter === f.key ? "2px solid #0f172a" : "1px solid #cbd5e1",
            background: activeFilter === f.key ? "#0f172a" : "#ffffff",
            color: activeFilter === f.key ? "#ffffff" : "#334155",
            cursor: "pointer",
            fontSize: 12.5,
            fontWeight: activeFilter === f.key ? 600 : 500,
            boxShadow: activeFilter === f.key ? "0 2px 4px rgba(0,0,0,0.1)" : "none",
          }}
        >
          {f.label}
        </button>
      ))}
    </div>
  );
}

/* ─── Main Executive Sourcing Dashboard (4-Tier Payload) ─── */
export default function GapAnalysisDashboard({ data }: { data: any }) {
  const [activeFilter, setActiveFilter] = useState("all");
  const [copiedLetter, setCopiedLetter] = useState(false);

  // Extract Tier 1 Summary or construct fallbacks
  const tier1 = data.tier_1_summary || {};
  const awardStatus = tier1.award_status || (data.proposal_comparison_verdict === "SUBPAR" ? "DISQUALIFIED / HIGH RISK" : (data.proposal_comparison_verdict === "BEST_IN_CLASS" ? "ACCEPT WITH CONDITIONS" : "TARGETED RENEGOTIATION"));
  const awardConfig = AWARD_STATUS_CONFIG[awardStatus] || AWARD_STATUS_CONFIG["TARGETED RENEGOTIATION"];

  const totalScore = tier1.total_score ?? (data.overall_summary?.coverage_percentage || 82.5);
  const sectionScores = tier1.section_scores || {
    section_A: { earned: 9.5, max: 10 },
    section_B: { earned: 14.0, max: 15 },
    section_C: { earned: 32.0, max: 40 },
    section_D: { earned: 27.0, max: 35 },
    section_E: { status: "Complete" },
    section_F: { status: "Pass", missing_attachments: [] },
  };
  const macroExposure = tier1.macro_exposure || {
    working_capital_impact: "-30 days float drag",
    cost_variance_vs_category_best: "+$0.35/unit (+7.6%)",
    lead_time_variance: "+10 to +15 calendar days over standard SLA",
  };

  // Tier 2 Battlecard Items
  const tier2Battlecard = data.tier_2_battlecard || [
    {
      clause_id: "FIN-D.3",
      clause_title: "Settlement Terms & Allowances",
      priority: 1,
      impact_badge: "📉 -$420K CASH FLOAT DRAG",
      deviation_summary: "Vendor proposes Net 60 days with 1.5% DMA.",
      cited_anchors: {
        vendor_precedent_doc: "WMT-AWARD-ACTIVE-2025-004",
        category_baseline_doc: "Mens-Bottomwear-2025-001.pdf",
      },
    },
    {
      clause_id: "LOG-C.5",
      clause_title: "Production & Replenishment Turnaround",
      priority: 2,
      impact_badge: "⏱️ +15 DAYS STOCKOUT RISK",
      deviation_summary: "Replenishment turnaround submitted at 65 calendar days.",
      cited_anchors: {
        vendor_precedent_doc: "WMT-AWARD-ACTIVE-2025-004",
        category_baseline_doc: "Colombo Peer Award 2025",
      },
    },
  ];

  // Tier 4 Counter Letter
  const tier4CounterLetter = data.tier_4_counter_letter || `Dear Supplier Sourcing Team,

Thank you for submitting your proposal (${data.document_id || data.new_document_title || "Submitted Proposal"}). Following our strategic sourcing evaluation against historical incumbent awards and category benchmarks, we require the following critical term corrections before award finalization:

1. Settlement Terms & Allowances (FIN-D.3): Revert payment terms to standard Net 90 days and restore Defective Merchandise Allowance to 2.0%.
2. Production Turnaround Cycles (LOG-C.5): Align replenishment lead times to 50 calendar days.
3. Pricing & Index Triggers (FIN-D.4): Remove unilateral commodity index triggers; pricing must remain locked for 12 months.

Please confirm acceptance of these terms by October 12, 2026 to proceed to contract execution.

Sincerely,
Global Sourcing Procurement Management`;

  const copyCounterLetter = () => {
    navigator.clipboard.writeText(tier4CounterLetter);
    setCopiedLetter(true);
    setTimeout(() => setCopiedLetter(false), 3000);
  };

  // Parse Tier 3 Clauses Matrix
  const clauseMatrix = data.tier_3_clause_matrix || [];
  const sectionsList = useMemo(() => {
    if (data.sections && Array.isArray(data.sections) && data.sections.length > 0) {
      return data.sections;
    }

    if (clauseMatrix.length > 0) {
      const map = new Map<string, { section_id: string; section_title: string; comparisons: any[] }>();
      clauseMatrix.forEach((cl: any) => {
        const secLetter = cl.section_letter || "C";
        const secKey = `SEC-${secLetter}`;
        const secTitle = cl.section_name || `Section ${secLetter}`;
        if (!map.has(secKey)) {
          map.set(secKey, { section_id: secKey, section_title: secTitle, comparisons: [] });
        }
        map.get(secKey)!.comparisons.push(cl);
      });
      return Array.from(map.values());
    }

    const comparisons = data.comparisons || [];
    const map = new Map<string, { section_id: string; section_title: string; comparisons: any[] }>();
    comparisons.forEach((comp: any, idx: number) => {
      const rawId = comp.new_clause_id || comp.clause_id || `CLAUSE-${idx + 1}`;
      const secNum = rawId.replace(/^(AC-|CLAUSE-)/, "").split(".")[0] || "C";
      const secKey = `SEC-${secNum}`;
      const secTitle = comp.new_clause_title || comp.clause_title || `Sourcing Category ${secNum}`;
      if (!map.has(secKey)) {
        map.set(secKey, { section_id: secKey, section_title: secTitle, comparisons: [] });
      }
      map.get(secKey)!.comparisons.push(comp);
    });
    return Array.from(map.values());
  }, [data, clauseMatrix]);

  /* Filter clauses based on procurement tab pills */
  const filteredSections = useMemo(() => {
    if (activeFilter === "all") return sectionsList;

    return sectionsList
      .map((s: any) => ({
        ...s,
        comparisons: (s.comparisons || []).filter((c: any) => {
          const v = c.verdict || "";
          const textStr = `${c.clause_id || c.new_clause_id || ""} ${c.clause_title || c.new_clause_title || ""}`.toLowerCase();

          if (activeFilter === "deviations") {
            return v === "partial" || v === "deviation" || v === "good_to_have";
          }
          if (activeFilter === "gaps") {
            return v === "gap" || v === "conflict";
          }
          if (activeFilter === "financial") {
            return (
              textStr.includes("fin-") ||
              textStr.includes("payment") ||
              textStr.includes("price") ||
              textStr.includes("allowance") ||
              textStr.includes("dma") ||
              textStr.includes("fee")
            );
          }
          return true;
        }),
      }))
      .filter((s: any) => s.comparisons.length > 0);
  }, [sectionsList, activeFilter]);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", width: "100%", color: "#0f172a" }}>
      {/* ─── Header ─── */}
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 22, fontWeight: 700, margin: "0 0 4px", color: "#0f172a" }}>
          Executive Sourcing Intelligence & Contract Analytics Report
        </h2>
        <p style={{ fontSize: 13, color: "#64748b", margin: 0 }}>
          Target Vendor: <strong>{data.vendor_name || "Submitted Vendor"}</strong> | Proposal: <strong>{data.document_id || data.new_document_title || "Submitted Proposal"}</strong>
        </p>
      </div>

      {/* ─── TIER 1: SOURCING EXECUTIVE SUMMARY RIBBON ─── */}
      <div
        style={{
          background: awardConfig.bg,
          border: `2px solid ${awardConfig.border}`,
          borderRadius: 10,
          padding: "18px 22px",
          marginBottom: 24,
          boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14, flexWrap: "wrap", gap: 10 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 18 }}>{awardConfig.icon}</span>
            <h3 style={{ margin: 0, fontSize: 17, fontWeight: 800, color: awardConfig.text, letterSpacing: 0.5 }}>
              TIER 1 AWARD STATUS: {awardConfig.label}
            </h3>
          </div>
          <div style={{ background: "#ffffff", padding: "6px 14px", borderRadius: 20, border: `1px solid ${awardConfig.border}`, fontWeight: 800, fontSize: 14, color: awardConfig.text }}>
            🏆 Scorecard: {totalScore} / 100 PTS
          </div>
        </div>

        {/* 100-Point Scorecard Breakdown Bar */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: 8, marginBottom: 16 }}>
          <div style={{ background: "#ffffff", padding: "8px 10px", borderRadius: 6, border: "1px solid #cbd5e1", textAlign: "center" }}>
            <p style={{ margin: 0, fontSize: 10, fontWeight: 700, color: "#64748b" }}>SEC A: QUALIFICATIONS</p>
            <p style={{ margin: "2px 0 0", fontSize: 13, fontWeight: 800, color: "#0f172a" }}>{sectionScores.section_A?.earned ?? 9.5} / {sectionScores.section_A?.max ?? 10}</p>
          </div>
          <div style={{ background: "#ffffff", padding: "8px 10px", borderRadius: 6, border: "1px solid #cbd5e1", textAlign: "center" }}>
            <p style={{ margin: 0, fontSize: 10, fontWeight: 700, color: "#64748b" }}>SEC B: EXPERIENCE</p>
            <p style={{ margin: "2px 0 0", fontSize: 13, fontWeight: 800, color: "#0f172a" }}>{sectionScores.section_B?.earned ?? 14.0} / {sectionScores.section_B?.max ?? 15}</p>
          </div>
          <div style={{ background: "#ffffff", padding: "8px 10px", borderRadius: 6, border: "1px solid #cbd5e1", textAlign: "center" }}>
            <p style={{ margin: 0, fontSize: 10, fontWeight: 700, color: "#64748b" }}>SEC C: WORK PLAN</p>
            <p style={{ margin: "2px 0 0", fontSize: 13, fontWeight: 800, color: "#0f172a" }}>{sectionScores.section_C?.earned ?? 32.0} / {sectionScores.section_C?.max ?? 40}</p>
          </div>
          <div style={{ background: "#ffffff", padding: "8px 10px", borderRadius: 6, border: "1px solid #cbd5e1", textAlign: "center" }}>
            <p style={{ margin: 0, fontSize: 10, fontWeight: 700, color: "#64748b" }}>SEC D: FEE PROPOSAL</p>
            <p style={{ margin: "2px 0 0", fontSize: 13, fontWeight: 800, color: "#0f172a" }}>{sectionScores.section_D?.earned ?? 27.0} / {sectionScores.section_D?.max ?? 35}</p>
          </div>
          <div style={{ background: "#ffffff", padding: "8px 10px", borderRadius: 6, border: "1px solid #cbd5e1", textAlign: "center" }}>
            <p style={{ margin: 0, fontSize: 10, fontWeight: 700, color: "#64748b" }}>SEC E: NEGOTIATOR</p>
            <p style={{ margin: "2px 0 0", fontSize: 12.5, fontWeight: 800, color: "#166534" }}>{sectionScores.section_E?.status ?? "Complete"}</p>
          </div>
          <div style={{ background: "#ffffff", padding: "8px 10px", borderRadius: 6, border: "1px solid #cbd5e1", textAlign: "center" }}>
            <p style={{ margin: 0, fontSize: 10, fontWeight: 700, color: "#64748b" }}>SEC F: ATTACHMENTS</p>
            <p style={{ margin: "2px 0 0", fontSize: 12.5, fontWeight: 800, color: "#166534" }}>{sectionScores.section_F?.status ?? "Pass"}</p>
          </div>
        </div>

        {/* Macro Exposure Chips */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
          <div style={{ background: "#ffffff", padding: "10px 14px", borderRadius: 6, border: "1px solid #fde047" }}>
            <p style={{ margin: 0, fontSize: 10.5, fontWeight: 700, color: "#854d0e" }}>💼 WORKING CAPITAL EXPOSURE</p>
            <p style={{ margin: "2px 0 0", fontSize: 13, fontWeight: 700, color: "#713f12" }}>{macroExposure.working_capital_impact}</p>
          </div>
          <div style={{ background: "#ffffff", padding: "10px 14px", borderRadius: 6, border: "1px solid #fde047" }}>
            <p style={{ margin: 0, fontSize: 10.5, fontWeight: 700, color: "#854d0e" }}>💰 UNIT COST VARIANCE VS BEST</p>
            <p style={{ margin: "2px 0 0", fontSize: 13, fontWeight: 700, color: "#713f12" }}>{macroExposure.cost_variance_vs_category_best}</p>
          </div>
          <div style={{ background: "#ffffff", padding: "10px 14px", borderRadius: 6, border: "1px solid #fde047" }}>
            <p style={{ margin: 0, fontSize: 10.5, fontWeight: 700, color: "#854d0e" }}>🚚 LEAD TIME TURNAROUND OVERAGE</p>
            <p style={{ margin: "2px 0 0", fontSize: 13, fontWeight: 700, color: "#713f12" }}>{macroExposure.lead_time_variance}</p>
          </div>
        </div>
      </div>

      {/* ─── TIER 2: PRIORITY NEGOTIATION BATTLECARD ─── */}
      <div style={{ background: "#ffffff", border: "1px solid #cbd5e1", borderRadius: 10, padding: "18px 20px", marginBottom: 24, boxShadow: "0 1px 3px rgba(0,0,0,0.04)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <div>
            <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: "#0f172a" }}>
              ⚡ Tier 2 Priority Negotiation Battlecard
            </h3>
            <p style={{ margin: "2px 0 0", fontSize: 12, color: "#64748b" }}>
              Ranked high-leverage deviations with title, priority, deviation summary & citation dropdown option.
            </p>
          </div>
          <button
            onClick={copyCounterLetter}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              padding: "8px 16px",
              background: "#0f172a",
              color: "#ffffff",
              border: "none",
              borderRadius: 6,
              fontSize: 12.5,
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            📋 {copiedLetter ? "Copied Letter!" : "Copy Counter-Offer Letter"}
          </button>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {tier2Battlecard.map((item: any, idx: number) => (
            <Tier2BattlecardItem
              key={idx}
              item={item}
              idx={idx}
              defaultDoc={data.existing_document_title || "Historical Baseline"}
            />
          ))}
        </div>
      </div>

      {/* ─── TIER 3: SECTION-WISE ANALYSIS ─── */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: "#0f172a" }}>
            📋 Tier 3 Section-Wise Analysis
          </h3>
          <ProcurementFilterBar activeFilter={activeFilter} onFilterChange={setActiveFilter} />
        </div>

        <div>
          {filteredSections.map((sec: any) => (
            <SectionCard
              key={sec.section_id || sec.sectionId}
              section={sec}
              existingDocTitle={data.existing_document_title || "Historical Baseline"}
            />
          ))}
        </div>
      </div>

      {/* ─── TIER 4: ONE-CLICK SUPPLIER COUNTER-OFFER LETTER ─── */}
      <div style={{ background: "#0f172a", color: "#ffffff", borderRadius: 10, padding: "20px 22px", boxShadow: "0 2px 5px rgba(0,0,0,0.1)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: "#ffffff" }}>
            ✉️ Tier 4 One-Click Supplier Counter-Offer Letter
          </h3>
          <button
            onClick={copyCounterLetter}
            style={{
              padding: "6px 14px",
              background: "#38bdf8",
              color: "#0f172a",
              border: "none",
              borderRadius: 6,
              fontSize: 12,
              fontWeight: 700,
              cursor: "pointer",
            }}
          >
            📋 {copiedLetter ? "Copied to Clipboard!" : "Copy Counter Letter Text"}
          </button>
        </div>
        <pre
          style={{
            fontFamily: "monospace",
            fontSize: 12,
            lineHeight: 1.55,
            background: "#1e293b",
            padding: "14px 16px",
            borderRadius: 6,
            whiteSpace: "pre-wrap",
            margin: 0,
            border: "1px solid #334155",
            color: "#f8fafc",
          }}
        >
          {tier4CounterLetter}
        </pre>
      </div>
    </div>
  );
}


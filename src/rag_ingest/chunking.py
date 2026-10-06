"""
Updated Chunking — Story-Level Search
=======================================
"""

import hashlib
import logging

logger = logging.getLogger(__name__)


def generate_story_id(doc_title: str, story_title: str) -> str:
    """Generate a deterministic unique ID for a story across documents."""
    raw = f"{doc_title}::{story_title}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def safe_get(data, key, default="NA"):
    if not isinstance(data, dict):
        return default
    value = data.get(key)
    return value if value is not None else default


def chunk_for_storage(extracted_json: dict) -> dict[str, list[dict]]:
    """
    Takes extracted JSON and produces two separate chunk lists:
    
    1. story_chunks  — for semantic search (finding matching stories/sections)
    2. ac_chunks     — for gap analysis (comparing clauses)
    
    The link between them is story_id in metadata.
    """
    if not isinstance(extracted_json, dict):
        extracted_json = {}
        
    doc_title = extracted_json.get("document_id") or extracted_json.get("document_title") or "Untitled Document"
    doc_summary = extracted_json.get("document_summary") or ""
    doc_type = extracted_json.get("document_type") or "baseline_rfp"
    department = extracted_json.get("department") or "General"
    product_category = extracted_json.get("product_category") or "General"
    material_family = extracted_json.get("material_family") or "General"
    doc_metadata = extracted_json.get("metadata") or {}
    
    story_chunks = []
    ac_chunks = []
    
    # Process clauses from new taxonomy schema
    clauses = extracted_json.get("clauses") or []
    if clauses and isinstance(clauses, list):
        by_section: dict[str, list[dict]] = {}
        for cl in clauses:
            if not isinstance(cl, dict):
                continue
            s_letter = safe_get(cl, "section_letter", "C")
            s_name = safe_get(cl, "section_name", safe_get(cl, "clause_type", "general").capitalize())
            key = f"Section {s_letter}: {s_name}"
            by_section.setdefault(key, []).append(cl)

        for sec_key, cl_list in by_section.items():
            first_cl = cl_list[0]
            s_letter = safe_get(first_cl, "section_letter", "C")
            s_name = safe_get(first_cl, "section_name", "Section")
            s_weight = first_cl.get("section_weight", 0)
            e_type = safe_get(first_cl, "eval_type", "scored")

            story_id = generate_story_id(doc_title, sec_key)
            story_text = f"{sec_key} (Weight: {s_weight}%, Eval: {e_type}) — Extracted {len(cl_list)} clauses"
            
            story_chunks.append({
                "id": story_id,
                "text": story_text,
                "metadata": {
                    "story_id": story_id,
                    "story_title": sec_key,
                    "section_letter": s_letter,
                    "section_name": s_name,
                    "section_weight": s_weight,
                    "eval_type": e_type,
                    "document_type": doc_type,
                    "document_title": doc_title,
                    "department": department,
                    "product_category": product_category,
                    "material_family": material_family,
                    "ac_count": len(cl_list),
                }
            })

            for cl in cl_list:
                cid = safe_get(cl, "clause_id", safe_get(cl, "id", "CLAUSE-0.0"))
                ctitle = safe_get(cl, "clause_title", safe_get(cl, "title", "Clause"))
                ctext = safe_get(cl, "clause_text", safe_get(cl, "criteria", safe_get(cl, "text", "")))
                ctype_item = safe_get(cl, "clause_type", "general")
                cl_s_letter = safe_get(cl, "section_letter", s_letter)
                cl_s_name = safe_get(cl, "section_name", s_name)
                cl_s_weight = cl.get("section_weight", s_weight)
                cl_e_type = safe_get(cl, "eval_type", e_type)

                ac_chunks.append({
                    "id": f"{story_id}_{cid}",
                    "text": f"[{cid}] Section {cl_s_letter} ({cl_s_name}): {ctitle} — {ctext}",
                    "metadata": {
                        "ac_id": cid,
                        "ac_title": ctitle,
                        "clause_type": ctype_item,
                        "section_letter": cl_s_letter,
                        "section_name": cl_s_name,
                        "section_weight": cl_s_weight,
                        "eval_type": cl_e_type,
                        "story_id": story_id,
                        "document_type": doc_type,
                        "department": department,
                        "product_category": product_category,
                        "material_family": material_family,
                    }
                })

    # Process legacy stories & acceptance_criteria schema if present
    for story in extracted_json.get("stories", []) or []:
        if not isinstance(story, dict):
            continue
        story_metadata = story.get("metadata") or {}
        story_id = generate_story_id(doc_title, safe_get(story, "title", ""))
        story_text = f"{safe_get(story, 'title', '')} — {safe_get(story, 'description', '')}"
        
        story_chunks.append({
            "id": story_id,
            "text": story_text,
            "metadata": {
                "story_id": story_id,
                "role": safe_get(story_metadata, "role"),
                "group": safe_get(story_metadata, "group"),
                "doc_epic": safe_get(doc_metadata, "doc_epic"),
                "ac_count": len(story.get("acceptance_criteria", [])),
                "story_title": safe_get(story, "title"),
                "document_type": doc_type,
                "document_title": doc_title,
                "document_summary": doc_summary,
                "department": department,
                "product_category": product_category,
                "material_family": material_family,
                "story_description": safe_get(story, "description"),
                "story_id_original": safe_get(story, "id"),
            },
        })
        
        for ac in story.get("acceptance_criteria", []) or []:
            if not isinstance(ac, dict):
                continue
            ac_chunks.append({
                "id": f"{story_id}_{safe_get(ac, 'id', '')}",
                "text": f"{safe_get(ac, 'title', '')} — {safe_get(ac, 'criteria', '')}",
                "metadata": {
                    "ac_id": safe_get(ac, "id"),
                    "ac_title": safe_get(ac, "title"),
                    "story_id": story_id,
                    "story_id_original": safe_get(story, "id"),
                    "department": department,
                    "product_category": product_category,
                    "material_family": material_family,
                },
            })
    
    return {
        "story_chunks": story_chunks,
        "ac_chunks": ac_chunks,
    }

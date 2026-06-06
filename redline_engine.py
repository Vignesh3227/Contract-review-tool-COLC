import fitz 

def create_dummy_pdf(text: str) -> bytes:
    """
    Generates a basic PDF in memory for Demo Mode so the redliner has a canvas.
    Uses insert_textbox to safely wrap text inside a bounding box.
    """
    doc = fitz.open()
    page = doc.new_page()
    
    rect = fitz.Rect(50, 50, 550, 800)

    page.insert_textbox(rect, text, fontsize=11)
    
    return doc.write()

def generate_redlined_pdf(pdf_bytes: bytes, audit_json: dict) -> bytes:
    """
    Applies red strikeouts for violations and green highlights for approved clauses.
    Includes explicit content metadata for robust hover-tooltips.
    """
    if not pdf_bytes or not audit_json:
        return b""
        
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        issues = audit_json.get("issues", [])
        safe_clauses = audit_json.get("safe_clauses", [])
        
       
        for issue in issues:
            snippet = issue.get("original_text_snippet", "")
            replacement = issue.get("recommended_redline", "")
            
            if not snippet or snippet == "N/A": continue
                
            for page in doc:
                text_instances = page.search_for(snippet, quads=True)
                if text_instances:
                    
                    strike = page.add_strikeout_annot(text_instances)
                    strike.set_colors(stroke=(1, 0, 0))  # Red
                    strike.set_info(title="NyayaRedline AI", content=f"REVISED CLAUSE:\n{replacement}")
                    strike.update()
                    
                    
                    last_quad = text_instances[-1]
                    annot = page.add_text_annot(last_quad.lr, f"REVISED CLAUSE:\n\n{replacement}")
                    annot.set_colors(stroke=(0, 0.5, 0))
                    annot.set_info(title="NyayaRedline AI", content=f"REVISED CLAUSE:\n{replacement}")
                    
                    popup_rect = fitz.Rect(last_quad.lr.x, last_quad.lr.y, last_quad.lr.x + 300, last_quad.lr.y + 200)
                    annot.set_popup(popup_rect)
                    annot.update()

        
        for safe in safe_clauses:
            snippet = safe.get("original_text_snippet", "")
            reasoning = safe.get("reasoning", "")
            
            if not snippet or snippet == "N/A": continue
                
            for page in doc:
                text_instances = page.search_for(snippet, quads=True)
                if text_instances:
                   
                    highlight = page.add_highlight_annot(text_instances)
                    highlight.set_colors(stroke=(0.85, 1.0, 0.85)) # Light Green
                    highlight.set_info(title="NyayaRedline AI", content=f"APPROVED CLAUSE:\n{reasoning}")
                    highlight.update()
                    
                  
                    first_quad = text_instances[0]
                    annot = page.add_text_annot(first_quad.ul, f"[APPROVED CLAUSE]\n\n{reasoning}")
                    annot.set_colors(stroke=(0, 0.4, 0)) 
                    annot.set_info(title="NyayaRedline AI", content=f"APPROVED CLAUSE:\n{reasoning}")
                    
                    popup_rect = fitz.Rect(first_quad.ul.x, first_quad.ul.y, first_quad.ul.x + 250, first_quad.ul.y + 150)
                    annot.set_popup(popup_rect)
                    annot.update()
                    
        return doc.write()
    except Exception as e:
        print(f"Redlining Engine Error: {e}")
        return b""
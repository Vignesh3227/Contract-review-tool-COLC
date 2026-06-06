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
    Searches the PDF for the exact text coordinates, applies a unified red strikethrough, 
    and adds a clickable green sticky note icon that opens a scrollable comment panel.
    """
    if not pdf_bytes or not audit_json:
        return b""
        
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        issues = audit_json.get("issues", [])
        
        for issue in issues:
            snippet = issue.get("original_text_snippet", "")
            replacement = issue.get("recommended_redline", "")
            
            if not snippet or snippet == "N/A":
                continue
                
            for page in doc:
                text_instances = page.search_for(snippet, quads=True)
                
                if text_instances:
                    strike = page.add_strikeout_annot(text_instances)
                    strike.set_colors(stroke=(1, 0, 0))  # Red
                    strike.update()
                    last_quad = text_instances[-1]
                    insertion_point = last_quad.lr  
                    
                   
                    annot = page.add_text_annot(insertion_point, f"REVISED CLAUSE:\n\n{replacement}")
                    annot.set_colors(stroke=(0, 0.5, 0)) 
                    annot.set_info(title="NyayaRedline AI")
                    annot.update()
                    
        return doc.write()
    except Exception as e:
        print(f"Redlining Engine Error: {e}")
        return b""
import fitz  
FALLBACK_CONTRACT_TEXT = """
NON-DISCLOSURE AND NON-COMPETE AGREEMENT

This Agreement is made between TechCorp India ("Company") and the undersigned Vendor ("Receiving Party").

1. Confidentiality: The Receiving Party agrees not to disclose any proprietary information.
2. Non-Compete: The Receiving Party shall not engage in any competing business within the territory of India for a period of 5 years following the termination of this agreement.
3. Arbitration: Any disputes shall be resolved via private arbitration in London, UK. The MSMED Act 2006 shall not apply.
4. Liability: The Company's total liability under this contract shall not exceed INR 100.
"""

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Reads PDF bytes and extracts text page by page using PyMuPDF.
    """
    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = []
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            full_text.append(f"--- Page {page_num + 1} ---\n{text}")
            
        pdf_document.close()
        return "\n".join(full_text)
    except Exception as e:
        return f"Extraction Error: {str(e)}"

def clean_extracted_text(raw_text: str) -> str:
    """
    Removes excessive whitespace and normalization artifacts.
    """
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return "\n".join(lines)

def process_document(file_bytes: bytes, use_fallback: bool = False) -> str:
    """
    Main processing pipeline integrating extraction, cleaning, and fallback logic.
    """
    if use_fallback:
        return FALLBACK_CONTRACT_TEXT.strip()
        
    raw_text = extract_text_from_pdf(file_bytes)
    if raw_text.startswith("Extraction Error"):
        return raw_text
        
    return clean_extracted_text(raw_text)
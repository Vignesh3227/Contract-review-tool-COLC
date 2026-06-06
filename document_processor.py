import fitz  # PyMuPDF
import os
from google import genai
from google.genai import types

FALLBACK_CONTRACT_TEXT = """
NON-DISCLOSURE AND NON-COMPETE AGREEMENT

This Agreement is made between TechCorp India ("Company") and the undersigned Vendor ("Receiving Party").

1. Confidentiality: The Receiving Party agrees not to disclose any proprietary information.
2. Non-Compete: The Receiving Party shall not engage in any competing business within the territory of India for a period of 5 years following the termination of this agreement.
3. Arbitration: Any disputes shall be resolved via private arbitration in London, UK. The MSMED Act 2006 shall not apply.
4. Liability: The Company's total liability under this contract shall not exceed INR 100.
"""

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Reads PDF bytes and extracts text page by page using PyMuPDF."""
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

def extract_text_from_image(file_bytes: bytes, file_extension: str) -> str:
    """Uses Gemini 2.5 Flash Vision to act as a highly accurate OCR engine for images."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "OCR Error: Gemini API key missing."
            
        client = genai.Client(api_key=api_key)
        
        # Normalize mime type for the API
        mime_type = "image/jpeg" if file_extension.lower() in ['jpg', 'jpeg'] else "image/png"
        
        prompt = (
            "You are a highly accurate legal OCR system. Extract all the text from this document image "
            "exactly as it is written. Maintain the original layout and paragraphs. "
            "Do not add any conversational filler, just return the raw text."
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ]
        )
        return response.text
    except Exception as e:
        return f"OCR Extraction Error: {str(e)}"

def clean_extracted_text(raw_text: str) -> str:
    """Removes excessive whitespace and normalization artifacts."""
    if not raw_text:
        return ""
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return "\n".join(lines)

def process_document(file_bytes: bytes, file_name: str, use_fallback: bool = False) -> str:
    """Main processing pipeline routing to the correct extraction engine based on file type."""
    if use_fallback:
        return FALLBACK_CONTRACT_TEXT.strip()
        
    file_ext = file_name.split('.')[-1].lower() if file_name else ""
    
    if file_ext == 'pdf':
        raw_text = extract_text_from_pdf(file_bytes)
    elif file_ext in ['png', 'jpg', 'jpeg']:
        raw_text = extract_text_from_image(file_bytes, file_ext)
    else:
        return f"Error: Unsupported file format '{file_ext}'"
        
    if raw_text.startswith("Extraction Error") or raw_text.startswith("OCR Error"):
        return raw_text
        
    return clean_extracted_text(raw_text)
import os
import json
from google import genai
from google.genai import types

def run_contract_audit(contract_text: str) -> dict:
    """
    Sends contract text to Gemini 2.5 Flash and enforces a structured JSON response
    based on Indian statutory frameworks.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "Gemini API key missing in environment variables"}

    client = genai.Client(api_key=api_key)
    
    system_prompt = """
    You are an expert Indian Corporate Legal Auditor specializing in MSME contract protection. 
    Analyze the provided contract text and identify statutory violations, severe hidden liabilities, or highly unfavorable clauses.
    
    You must evaluate the contract using ONLY the following Indian statutory frameworks:
    1. Indian Contract Act, 1872
    2. Arbitration and Conciliation Act, 1996
    3. Specific Relief Act, 1963
    4. Sale of Goods Act, 1930
    5. Partnership Act, 1932
    6. Limited Liability Partnership Act, 2008
    7. Companies Act, 2013
    8. MSMED Act, 2006
    9. Information Technology Act, 2000
    10. Digital Personal Data Protection Act, 2023
    11. Copyright Act, 1957
    12. Trade Marks Act, 1999
    13. Negotiable Instruments Act, 1881
    14. Indian Stamp Act, 1899
    15. GST Acts

    CRITICAL REDLINING RULES FOR CONTEXT AWARENESS:
    1. NUMBERING PRESERVATION: You MUST preserve the exact numbering of the clause you are replacing. If the original clause is "9. Arbitration", your `recommended_redline` MUST start with "9." and retain the structural context.
    2. NO SEQUENCE BREAKING: Do not suggest adding new clause numbers at the bottom of the document. Simply rewrite the existing numbered clause in place.
    3. EXACT SNIPPETS: Your `original_text_snippet` must be an exact, verbatim substring from the text so the coordinate mapper can find it.
    
    You must respond ONLY with a valid JSON object matching this exact structure:
    {
      "overall_risk_score": 85,
      "summary": "Brief overall summary of contract standing",
      "issues": [
        {
          "original_text_snippet": "Verbatim text from the contract. Must be an exact substring.",
          "clause_title": "Name of the problematic clause",
          "severity": "High" | "Medium" | "Low",
          "governing_act": "The specific Indian Act violated",
          "description": "Explanation of why this exposes an MSME vendor under Indian law",
          "recommended_redline": "Exact wording to propose instead"
        }
      ]
    }
    """

    try:
       
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_prompt}\n\nContract Text:\n{contract_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Audit execution failed: {str(e)}"}
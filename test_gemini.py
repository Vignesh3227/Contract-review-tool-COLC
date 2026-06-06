import os
from dotenv import load_dotenv
from google import genai

def test_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    print("Initializing modern google-genai client...")
    
    try:
       
        client = genai.Client(api_key=api_key)
        
   
        model_name = 'gemini-2.5-flash'
        
        print(f"Attempting to connect to {model_name}...")
        
        response = client.models.generate_content(
            model=model_name,
            contents="Respond strictly with: 'Gemini API connection established.'"
        )
        
        print("\nSuccess:", response.text.strip())
        
    except Exception as e:
        print(f"\nConnection failed with error: {e}")

if __name__ == "__main__":
    test_gemini()
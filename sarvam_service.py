import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def translate_text(text: str, target_lang: str = "hi-IN", source_lang: str = "auto") -> str:
    """
    Translates text into a target Indian language using Sarvam's REST API.
    """
    if not SARVAM_API_KEY:
        return "Error: SARVAM_API_KEY not configured."
        
    url = "https://api.sarvam.ai/translate"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "input": text,
        "source_language_code": source_lang,
        "target_language_code": target_lang
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("translated_text", text)
        print(f"Sarvam Translation Error [{response.status_code}]: {response.text}")
        return text
    except Exception as e:
        print(f"Network error during translation: {e}")
        return text

def text_to_speech(text: str, target_lang: str = "hi-IN", speaker: str = "anushka") -> bytes:
    """
    Converts text to speech using Sarvam's REST API.
    Extracts the base64 string from the JSON response and returns raw audio bytes.
    """
    if not SARVAM_API_KEY:
        print("Error: SARVAM_API_KEY not configured.")
        return b""
        
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "target_language_code": target_lang,
        "speaker": speaker
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            
            data = response.json()
            if "audios" in data and len(data["audios"]) > 0:
                base64_string = data["audios"][0]
                return base64.b64decode(base64_string)
            print(f"TTS structure mismatch. Keys found: {data.keys()}")
            return b""
        else:
            print(f"Sarvam TTS Error [{response.status_code}]: {response.text}")
            return b""
    except Exception as e:
        print(f"Network error during TTS generation: {e}")
        return b""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def translate_text(text: str, target_lang: str = "hi-IN", source_lang: str = "auto") -> str:
    """
    Translates text into a target Indian language using Sarvam's REST API.
    Common targets: 'hi-IN' (Hindi), 'gu-IN' (Gujarati), 'bn-IN' (Bengali), 'ta-IN' (Tamil)
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
        else:
            print(f"Sarvam Translation Error [{response.status_code}]: {response.text}")
            return text
    except Exception as e:
        print(f"Network error during translation: {e}")
        return text

def text_to_speech(text: str, target_lang: str = "hi-IN", speaker: str = "anushka") -> bytes:
    """
    Converts text to speech audio bytes using Sarvam's REST API.
    Returns raw audio bytes (typically WAV/MP3 format depending on service defaults).
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
            # Return the raw audio binary stream
            return response.content
        else:
            print(f"Sarvam TTS Error [{response.status_code}]: {response.text}")
            return b""
    except Exception as e:
        print(f"Network error during TTS generation: {e}")
        return b""
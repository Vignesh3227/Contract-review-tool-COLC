import base64
import json  # Import the JSON library
from sarvam_service import translate_text, text_to_speech

print("Testing Translation REST Endpoint...")
translation = translate_text("The contract review is complete. No critical violations found.", target_lang="hi-IN")
print(f"Hindi Translation: {translation}\n")

print("Testing Text-to-Speech REST Endpoint...")
\
raw_audio_data = text_to_speech("नमस्ते, आपका स्वागत है।", target_lang="hi-IN")

if raw_audio_data:
    audio_data = json.loads(raw_audio_data)
    if "audios" in audio_data:
        base64_string = audio_data["audios"][0]
        audio_bytes = base64.b64decode(base64_string)
        
        print(f"Success! Received {len(audio_bytes)} bytes of audio data.")
        
        with open("test_output.wav", "wb") as f:
            f.write(audio_bytes)
            
        print("Saved audio file to 'test_output.wav'")
    else:
        print(f"TTS failed. Response didn't contain 'audios'. Got: {audio_data}")
else:
    print("TTS failed. No data received.")
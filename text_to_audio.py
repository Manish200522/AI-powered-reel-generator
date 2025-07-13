from gtts import gTTS
import os

def text_to_speech_file(text, folder):
    tts = gTTS(text=text, lang='en')
    path = os.path.join("user_uploads", folder)
    os.makedirs(path, exist_ok=True)
    save_path = os.path.join(path, "audio.mp3")
    tts.save(save_path)
    print(f"Saved to {save_path}")
    return save_path

#text_to_speech_file("hey I am a good boy", "db58bae8-5d96-11f0-9afb-4c496c99281a")

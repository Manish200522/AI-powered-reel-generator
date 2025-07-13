import os
import time
import subprocess
from text_to_audio import text_to_speech_file

# Helper function to print status with symbols
def log(msg, level="info"):
    symbols = {
        "info": "ℹ️",
        "success": "✅",
        "warn": "⚠️",
        "error": "❌"
    }
    print(f"{symbols.get(level, '')} {msg}")

def text_to_audio(folder):
    desc_path = f"user_uploads/{folder}/desc.txt"
    if not os.path.exists(desc_path):
        log(f"Missing description file: {desc_path}", "warn")
        return False

    try:
        with open(desc_path, "r", encoding="utf-8") as f:
            text = f.read()
        log(f"Generating TTS for folder: {folder}")
        text_to_speech_file(text, folder)
        return True
    except Exception as e:
        log(f"Error generating TTS for {folder}: {e}", "error")
        return False

def create_reel(folder):
    input_txt = f"user_uploads/{folder}/input.txt"
    audio_file = f"user_uploads/{folder}/audio.mp3"
    output_file = f"static/reels/{folder}.mp4"

    if not os.path.exists(input_txt):
        log(f"Missing input.txt: {input_txt}", "warn")
        return False
    if not os.path.exists(audio_file):
        log(f"Missing audio file: {audio_file}", "warn")
        return False

    command = (
        f'ffmpeg -f concat -safe 0 -i "{input_txt}" -i "{audio_file}" '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=decrease,'
        f'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
        f'-c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 192k '
        f'-shortest -r 30 -pix_fmt yuv420p "{output_file}"'
    )

    try:
        log(f"Creating reel for folder: {folder}")
        subprocess.run(command, shell=True, check=True)
        log(f"Reel created successfully: {output_file}", "success")
        return True
    except subprocess.CalledProcessError as e:
        log(f"FFmpeg failed for {folder}:\n{e}", "error")
        return False

if __name__ == "__main__":
    os.makedirs("static/reels", exist_ok=True)

    if not os.path.exists("done.txt"):
        open("done.txt", "w").close()

    while True:
        with open("done.txt", "r") as f:
            done_folders = set(f.read().splitlines())

        folders = os.listdir("user_uploads")
        for folder in folders:
            if folder in done_folders:
                continue

            log(f"Processing folder: {folder}")
            success = text_to_audio(folder) and create_reel(folder)

            if success:
                with open("done.txt", "a") as done_file:
                    done_file.write(folder + "\n")
            else:
                log(f"Processing failed for {folder}", "warn")

        time.sleep(4)

# ~/shoonya/whisper_ingest.py

import os
import json
import datetime
import subprocess
import shutil

AUDIO_INPUT = os.path.expanduser("~/shoonya/data/audio")
LTM_DIR = os.path.expanduser("~/shoonya/memory/ltm")

os.makedirs(AUDIO_INPUT, exist_ok=True)
os.makedirs(LTM_DIR, exist_ok=True)

MODEL = "base"  # Change to 'small', 'medium', 'large' if needed

def transcribe(file_path):
    print(f" Transcribing {file_path}...")
    cmd = [
        "whisper", file_path,
        "--model", MODEL,
        "--output_format", "txt",
        "--output_dir", AUDIO_INPUT
    ]
    subprocess.run(cmd)

def ingest_transcripts():
    for fname in os.listdir(AUDIO_INPUT):
        if fname.endswith(".txt") and not fname.startswith("transcribed_"):
            path = os.path.join(AUDIO_INPUT, fname)
            with open(path) as f:
                text = f.read()

            # Save as LTM memory
            memory_id = fname.replace(".txt", "")
            mem_file = os.path.join(LTM_DIR, f"{memory_id}.json")
            if not os.path.exists(mem_file):
                with open(mem_file, 'w') as mf:
                    mf.write('{\n')
                    mf.write(f'  "id": "{memory_id}",\n')
                    mf.write(f'  "source": "audio/{fname}",\n')
                    mf.write(f'  "text": {json.dumps(text)}\n')
                    mf.write('}\n')
                print(f" Stored: {mem_file}")
            
            # Rename transcript so it's not reprocessed
            shutil.move(path, os.path.join(AUDIO_INPUT, f"transcribed_{fname}"))

if __name__ == "__main__":
    print(" Drop your audio (.mp3/.wav) files in:", AUDIO_INPUT)
    input("Press Enter after placing files...")

    audio_files = [f for f in os.listdir(AUDIO_INPUT) if f.endswith(('.mp3', '.wav'))]
    for f in audio_files:
        transcribe(os.path.join(AUDIO_INPUT, f))

    ingest_transcripts()
    print(" Whisper ingest complete.")


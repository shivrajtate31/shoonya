import os
import hashlib
import json

WEB_DIR = os.path.expanduser("~/shoonya/data/web")
LTM_DIR = os.path.expanduser("~/shoonya/memory/ltm")
QUESTIONS_FILE = os.path.expanduser("~/shoonya/curiosity/questions_to_explore.md")

os.makedirs(LTM_DIR, exist_ok=True)
os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)

def generate_id(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def split_text(text, max_len=1000):
    words = text.split()
    chunks, chunk = [], []
    for word in words:
        chunk.append(word)
        if len(' '.join(chunk)) >= max_len:
            chunks.append(' '.join(chunk))
            chunk = []
    if chunk:
        chunks.append(' '.join(chunk))
    return chunks

def ingest_file(path):
    with open(path, 'r') as f:
        text = f.read()
    chunks = split_text(text)
    for chunk in chunks:
        memory_id = generate_id(chunk)
        memory_file = os.path.join(LTM_DIR, f"{memory_id}.json")
        if not os.path.exists(memory_file):
            entry = {
                "id": memory_id,
                "source": os.path.basename(path),
                "text": chunk
            }
            with open(memory_file, 'w') as mf:
                json.dump(entry, mf, indent=2)

            print(f"🧠 Stored memory: {memory_file}")

            # Suggest a question
            with open(QUESTIONS_FILE, 'a') as qf:
                qf.write(f"- What does this mean? → {chunk[:80]}\n")

if __name__ == "__main__":
    files = [f for f in os.listdir(WEB_DIR) if f.endswith(".txt")]
    for f in files:
        path = os.path.join(WEB_DIR, f)
        print(f"📥 Ingesting: {f}")
        ingest_file(path)
    print("✅ Ingestion complete.")


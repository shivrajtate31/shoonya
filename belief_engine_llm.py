import os
import json
import yaml
import hashlib
from pathlib import Path
from core.llm_api import query_ollama_api as query_llm

#  Paths
LTM_DIR = os.path.expanduser("~/shoonya/memory/ltm")
BELIEFS_FILE = os.path.expanduser("~/shoonya/beliefs/core_beliefs.yaml")
os.makedirs(os.path.dirname(BELIEFS_FILE), exist_ok=True)

#  Load existing beliefs
if os.path.exists(BELIEFS_FILE):
    with open(BELIEFS_FILE, "r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)
        if isinstance(loaded, list):
            beliefs = {
                hashlib.md5(entry['belief'].encode()).hexdigest()[:12]: entry
                for entry in loaded
            }
        else:
            beliefs = loaded or {}
else:
    beliefs = {}

#  Belief ID generator
def belief_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:12]

#  Process LTM files
files = [f for f in os.listdir(LTM_DIR) if f.endswith(".json")]
seen_sources = set()
total_beliefs = 0

for f in files:
    filepath = os.path.join(LTM_DIR, f)
    try:
        with open(filepath, "r", encoding="utf-8") as jf:
            data = json.load(jf)

        chunks = data if isinstance(data, list) else [data]

        for chunk in chunks:
            text = chunk.get("text", "").strip()
            source = chunk.get("source", f)

            #  Skip if already seen
            if source in seen_sources:
                continue
            seen_sources.add(source)

            if not text or len(text.split()) < 8:
                continue

            print(f"Extracting from: {source}")


            prompt = f"Extract 3 short factual beliefs from this text:\n{text}\nReturn only numbered belief sentences."
            response = query_llm(prompt)

            lines = [line.strip() for line in response.split('\n') if line.strip()]

            for line in lines:
                belief_text = line.lstrip("1234567890.- ").strip()
                if len(belief_text.split()) < 5:
                    continue
                key = belief_id(belief_text)
                if key not in beliefs:
                    beliefs[key] = {
                        "belief": belief_text,
                        "source": source
                    }
                    total_beliefs += 1

    except Exception as e:
        print(f"[!] Error extracting from {f}: {e}")

#  Save updated beliefs
with open(BELIEFS_FILE, "w", encoding="utf-8") as f:
    yaml.dump(beliefs, f, sort_keys=False, allow_unicode=True)

print(f"\n Extracted {total_beliefs} new beliefs → {BELIEFS_FILE}")

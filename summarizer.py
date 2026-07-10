# ~/shoonya/summarizer.py

import os
import json
from datetime import datetime

LTM_DIR = os.path.expanduser("~/shoonya/memory/ltm")
SUMMARY_FILE = os.path.expanduser(f"~/shoonya/reflection/summary_{datetime.now().date()}.md")

os.makedirs(os.path.dirname(SUMMARY_FILE), exist_ok=True)

# Naive keyword frequency-based summarizer
def score_chunk(text):
    keywords = ["life", "energy", "consciousness", "process", "biology", "quantum", "system", "cell"]
    return sum(text.lower().count(k) for k in keywords)

def summarize():
    summaries = []
    for fname in os.listdir(LTM_DIR):
        if fname.endswith(".json"):
            path = os.path.join(LTM_DIR, fname)
            with open(path) as f:
                entry = json.load(f)
                score = score_chunk(entry["text"])
                summaries.append((score, entry["text"]))

    summaries.sort(reverse=True)
    top_chunks = [text for score, text in summaries[:5]]

    with open(SUMMARY_FILE, 'w') as f:
        f.write(f"# Summary for {datetime.now().date()}\n\n")
        for i, chunk in enumerate(top_chunks, 1):
            f.write(f"### Insight {i}\n{chunk}\n\n")

    print(f"🧠 Summary written to {SUMMARY_FILE}")

if __name__ == "__main__":
    summarize()


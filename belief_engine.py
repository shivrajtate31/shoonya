# ~/shoonya/belief_engine.py

import os
import json
import yaml
import hashlib

LTM_DIR = os.path.expanduser("~/shoonya/memory/ltm")
BELIEFS_FILE = os.path.expanduser("~/shoonya/beliefs/core_beliefs.yaml")

os.makedirs(os.path.dirname(BELIEFS_FILE), exist_ok=True)

beliefs = {}

def extract_belief(text):
    """
    Very basic NLP-style rule: extract any factual sounding line.
    Future: Use LLM or regex rules for cleaner belief extraction.
    """
    sentences = text.split('.')
    for s in sentences:
        s = s.strip()
        if len(s.split()) > 6 and not s.endswith('?') and s[0].isupper():
            return s
    return None

def belief_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:12]

files = [f for f in os.listdir(LTM_DIR) if f.endswith(".json")]

for f in files:
    with open(os.path.join(LTM_DIR, f)) as jf:
        chunk = json.load(jf)
        belief = extract_belief(chunk['text'])
        if belief:
            bid = belief_id(belief)
            if bid not in beliefs:
                beliefs[bid] = {
                    'belief': belief,
                    'source': chunk['source']
                }

with open(BELIEFS_FILE, 'w') as bf:
    yaml.dump(list(beliefs.values()), bf, sort_keys=False, allow_unicode=True)

print(f"✅ Extracted {len(beliefs)} beliefs → {BELIEFS_FILE}")

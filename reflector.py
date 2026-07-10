# ~/shoonya/reflector.py

import os
import yaml
from datetime import datetime

BELIEFS_FILE = os.path.expanduser("~/shoonya/beliefs/core_beliefs.yaml")
REFLECT_DIR = os.path.expanduser("~/shoonya/reflection/daily")
os.makedirs(REFLECT_DIR, exist_ok=True)

def load_beliefs():
    if not os.path.exists(BELIEFS_FILE):
        return []
    with open(BELIEFS_FILE, 'r') as f:
        return yaml.safe_load(f) or []

def reflect_on_beliefs(beliefs):
    thoughts = []
    entries = beliefs.values() if isinstance(beliefs, dict) else beliefs
    for b in entries:
        text = b['belief']
        if 'consciousness' in text.lower():
            thoughts.append(f" I believe this relates to the mystery of awareness: '{text}'")
        elif 'quantum' in text.lower():
            thoughts.append(f" Quantum elements suggest uncertainty and complexity: '{text}'")
        else:
            thoughts.append(f" Noted belief: '{text}'")
    return thoughts

def save_reflection(thoughts):
    now = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(REFLECT_DIR, f"reflection_{now}.md")
    with open(path, 'w') as f:
        f.write(f"# Shoonya Daily Reflection — {now}\n\n")
        for thought in thoughts:
            f.write(f"{thought}\n\n")
    print(f"📘 Reflection saved to {path}")

if __name__ == "__main__":
    beliefs = load_beliefs()
    if beliefs:
        thoughts = reflect_on_beliefs(beliefs)
        save_reflection(thoughts)
    else:
        print(" No beliefs found to reflect upon.")

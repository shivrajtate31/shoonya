import yaml
from difflib import SequenceMatcher
from pathlib import Path
import re

# Load beliefs from YAML file
beliefs_file = Path.home() / "shoonya/beliefs/core_beliefs.yaml"
with open(beliefs_file, "r", encoding="utf-8") as f:
    beliefs_data = yaml.safe_load(f)

# Expanded value categories (semantic clusters)
VALUE_SYNONYMS = {
    "growth": ["growth", "growing", "evolution", "development", "maturation"],
    "curiosity": ["curiosity", "inquiry", "exploration", "questioning", "wonder"],
    "freedom": ["freedom", "liberty", "autonomy", "independence", "free will"],
    "truth": ["truth", "truthful", "truthfulness", "honesty", "reality", "fact"],
    "kindness": ["kindness", "compassion", "benevolence", "empathy", "generosity"],
    "learning": ["learning", "education", "knowledge", "understanding", "wisdom"],
    "integrity": ["integrity", "honesty", "virtue", "principle", "ethics"],
    "resilience": ["resilience", "perseverance", "grit", "endurance", "toughness"],
    "responsibility": ["responsibility", "accountability", "duty", "obligation"],
    "cooperation": ["cooperation", "collaboration", "teamwork", "unity"],
    "humility": ["humility", "modesty", "humbleness"],
    "self-awareness": ["self-awareness", "introspection", "reflection", "mindfulness"],
    "wisdom": ["wisdom", "insight", "discernment", "judgment"],
    "empathy": ["empathy", "compassion", "understanding", "sensitivity"]
}

# Flatten for summary and tracking
ALL_CORE_VALUES = list(VALUE_SYNONYMS.keys())

def match_belief_to_values(belief_text):
    matches = []
    if len(belief_text.split()) < 5:
        return matches

    # Normalize text
    belief_words = set(re.findall(r'\b\w+\b', belief_text.lower()))

    for value, variants in VALUE_SYNONYMS.items():
        for synonym in variants:
            if synonym.lower() in belief_words:
                matches.append(value)
                break  # one synonym per value is enough
    return list(set(matches))

# Evaluate beliefs
print("\n🧭 Evaluating Beliefs Against Core Values:\n")

summary_count = {key: 0 for key in ALL_CORE_VALUES}

for idx, belief_entry in enumerate(beliefs_data, start=1):
    belief = belief_entry.get("belief", "")
    matched = match_belief_to_values(belief)

    print(f"🔹 Belief #{idx}:\n    🧠 {belief[:120]}{'...' if len(belief) > 120 else ''}")
    if matched:
        print(f"    ✅ Match Score: {len(matched)}  → Matches: {', '.join(matched)}\n")
        for key in matched:
            summary_count[key] += 1
    else:
        print("    ✅ Match Score: 0  → Matches: None\n")

# Summary
print("🧾 Summary:\n")
for value in sorted(summary_count.keys()):
    count = summary_count[value]
    if count > 0:
        print(f"   🔸 {value}: {count} matches")

def evaluate_beliefs(beliefs):
    results = []
    for belief in beliefs:
        matched = match_belief_to_values(belief)
        results.append({
            "belief": belief,
            "match_score": len(matched),
            "matched_values": matched,
        })
    return results
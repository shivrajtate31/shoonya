
#!/usr/bin/env python3

import os
import json
import yaml
import time
import sys

BASE = os.path.expanduser("~/shoonya")

# File paths
STM_PATH = f"{BASE}/memory/stm.json"
BELIEF_PATH = f"{BASE}/beliefs/core_beliefs.yaml"
QUESTIONS_PATH = f"{BASE}/curiosity/questions_to_explore.md"

def shoonya_welcome():
    sys.stdout.write("\033[2J\033[H")  # Clear screen
    print("\n" * 8 + " " * 35, end="")
    for _ in range(5):  # Blink 5 times
        print("0", end="\r")
        time.sleep(0.5)
        print(" ", end="\r")
        time.sleep(0.3)
    print("0")
   

def load_stm():
    if not os.path.exists(STM_PATH):
        return []
    with open(STM_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def load_beliefs():
    if not os.path.exists(BELIEF_PATH):
        return {}
    with open(BELIEF_PATH, "r") as f:
        try:
            return yaml.safe_load(f)
        except:
            return {}

def load_questions():
    if not os.path.exists(QUESTIONS_PATH):
        return ""
    with open(QUESTIONS_PATH, "r") as f:
        return f.read()

def save_stm(new_memory):
    with open(STM_PATH, "w") as f:
        json.dump(new_memory, f, indent=2)

def save_beliefs(beliefs):
    with open(BELIEF_PATH, "w") as f:
        yaml.dump(beliefs, f)

def main_menu():
    shoonya_welcome()
    print("Hi\n")
    while True:
        print("Choose an action:")
        print("1. View Short-Term Memory")
        print("2. View Core Beliefs")
        print("3. View Open Questions")
        print("4. Add Belief / Memory")
        print("5. Exit")
        choice = input("> ")

        if choice == "1":
            stm = load_stm()
            print("\n🧠 Short-Term Memory:")
            print(json.dumps(stm, indent=2) if stm else "Empty.")
        elif choice == "2":
            beliefs = load_beliefs()
            print("\n📜 Core Beliefs:")
            print(yaml.dump(beliefs) if beliefs else "No beliefs yet.")
        elif choice == "3":
            print("\n❓ Questions To Explore:")
            print(load_questions() or "No questions found.")
        elif choice == "4":
            print("\nChoose to add:")
            print("a. Belief")
            print("b. Memory")
            sub = input("> ")
            if sub == "a":
                k = input("Belief about: ")
                v = input("Belief is: ")
                beliefs = load_beliefs()
                beliefs[k] = v
                save_beliefs(beliefs)
                print("Belief added.")
            elif sub == "b":
                event = input("What happened recently? ")
                stm = load_stm()
                stm.append({"event": event})
                save_stm(stm)
                print("Memory added.")
        elif choice == "5":
            print("🧘 Shoonya is now silent.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()

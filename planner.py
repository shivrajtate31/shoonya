# ~/shoonya/planner.py

import os
import json
from datetime import datetime

TODO_PATH = os.path.expanduser("~/shoonya/planner/todo.md")
TASKS_PATH = os.path.expanduser("~/shoonya/planner/tasks.json")

os.makedirs(os.path.dirname(TODO_PATH), exist_ok=True)

# Load existing tasks if present
def load_tasks():
    if os.path.exists(TASKS_PATH):
        try:
            with open(TASKS_PATH) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Warning: tasks.json is empty or invalid. Resetting...")
            return []
    return []

def save_tasks(tasks):
    with open(TASKS_PATH, 'w') as f:
        json.dump(tasks, f, indent=2)

def display_menu():
    print("\n📋 Planner Options:")
    print("1. View tasks")
    print("2. Add task")
    print("3. Mark task as done")
    print("4. Save as markdown")
    print("5. Exit")

def display_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
    for i, task in enumerate(tasks):
        status = "✅" if task['done'] else "❌"
        print(f"{i+1}. {status} {task['desc']}")

def save_markdown(tasks):
    with open(TODO_PATH, 'w') as f:
        f.write(f"# 📅 Tasks for {datetime.now().date()}\n\n")
        for task in tasks:
            status = "[x]" if task['done'] else "[ ]"
            f.write(f"- {status} {task['desc']}\n")
    print(f"✅ Saved markdown → {TODO_PATH}")

def main():
    tasks = load_tasks()

    while True:
        display_menu()
        choice = input("Select: ")

        if choice == "1":
            display_tasks(tasks)

        elif choice == "2":
            desc = input("Task description: ")
            tasks.append({"desc": desc, "done": False})

        elif choice == "3":
            display_tasks(tasks)
            idx = int(input("Mark which task as done (number)?: ")) - 1
            if 0 <= idx < len(tasks):
                tasks[idx]['done'] = True
            else:
                print("Invalid task number.")

        elif choice == "4":
            save_markdown(tasks)

        elif choice == "5":
            save_tasks(tasks)
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

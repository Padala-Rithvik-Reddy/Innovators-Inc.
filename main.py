import json
import os
import sys
from keystroke_module import execute_command

# File paths
DB_FILE = "knowledge_base.json"
IGNORED_FILE = "ignored_words.json"
MISTAKE_FILE = "mistake_map.json"

# Helper function to check file existence using os.stat()
def file_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

def ensure_file_exists(filename, default_data):
    """Creates a file with default data if it does not exist."""
    try:
        if not file_exists(filename):
            with open(filename, "w") as f:
                json.dump(default_data, f, indent=4)
    except Exception as e:
        print(f"Error ensuring file {filename} exists: {e}", file=sys.stderr)

# Create files if missing
ensure_file_exists(DB_FILE, {})
ensure_file_exists(IGNORED_FILE, [])
ensure_file_exists(MISTAKE_FILE, {})

def load_data():
    """Loads data from JSON files and returns the knowledge base, ignored words, and mistake map."""
    try:
        with open(DB_FILE, "r") as f:
            knowledge_base = json.load(f)
    except Exception as e:
        print(f"Error loading {DB_FILE}: {e}", file=sys.stderr)
        knowledge_base = {}
    try:
        with open(IGNORED_FILE, "r") as f:
            ignored_words = set(json.load(f))
    except Exception as e:
        print(f"Error loading {IGNORED_FILE}: {e}", file=sys.stderr)
        ignored_words = set()
    try:
        with open(MISTAKE_FILE, "r") as f:
            mistake_map = json.load(f)
    except Exception as e:
        print(f"Error loading {MISTAKE_FILE}: {e}", file=sys.stderr)
        mistake_map = {}
    return knowledge_base, ignored_words, mistake_map

def save_data():
    """Saves the knowledge base, ignored words, and mistake map to JSON files."""
    global knowledge_base, ignored_words, mistake_map
    try:
        with open(DB_FILE, "w") as f:
            json.dump(knowledge_base, f, indent=4)
    except Exception as e:
        print(f"Error saving {DB_FILE}: {e}", file=sys.stderr)
    try:
        with open(IGNORED_FILE, "w") as f:
            json.dump(list(ignored_words), f, indent=4)
    except Exception as e:
        print(f"Error saving {IGNORED_FILE}: {e}", file=sys.stderr)
    try:
        with open(MISTAKE_FILE, "w") as f:
            json.dump(mistake_map, f, indent=4)
    except Exception as e:
        print(f"Error saving {MISTAKE_FILE}: {e}", file=sys.stderr)

def process_command(command):
    """Processes user input, learns from corrections, and triggers keystroke actions."""
    global ignored_words

    command_words = command.lower().split()
    # Filter out ignored words
    filtered_command = [word for word in command_words if word not in ignored_words]
    if not filtered_command:
        print("⚠️ This command contains only ignored words. No prediction.")
        return
    command_key = " ".join(filtered_command)
    if command_key in knowledge_base:
        predicted_output = knowledge_base[command_key]
    else:
        predicted_output = filtered_command

    print("\n🤖 Predicted output:", predicted_output)
    user_response = input("Is this correct? (yes/no): ").strip().lower()
    if user_response == "no":
        correct_response = input("Enter the correct response (as space-separated words): ").strip().lower().split()
        if correct_response:
            knowledge_base[command_key] = correct_response
            mistake_map[command_key] = correct_response
            mistaken_words = set(filtered_command) - set(correct_response)
            ignored_words.update(mistaken_words)
            save_data()
            print("\n✅ Updated knowledge base & mistake map!")
    else:
        print("✅ Command executed as predicted.")
        execute_command(predicted_output)

# Load stored data
knowledge_base, ignored_words, mistake_map = load_data()

# Main loop
while True:
    command = input("\nEnter command (type 'exit' to quit): ").strip()
    if command.lower() == "exit":
        save_data()
        break
    process_command(command)

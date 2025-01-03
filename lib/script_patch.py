#!/usr/bin/env python3
# ID 3 - data_PATCH.py

import os
import glob
import re
from datetime import datetime, timezone

# Get environment variables
DATA_DIR = os.environ.get('DATA_DIR')
DATA_EXT = os.environ.get('DATA_EXT')
DATA_PATH = os.environ.get('DATA_PATH')
DATA_FILE_YML = os.environ.get('DATA_FILE_YML')

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

def print_red(text):
    print(f"{Colors.RED}{text}{Colors.RESET}")

def print_green(text):
    print(f"{Colors.GREEN}{text}{Colors.RESET}")

# Step 1: Find the file with the unique extension in the DATA_DIR
# def find_unique_file(DATA_DIR, DATA_EXT):
#     files = glob.glob(os.path.join(DATA_DIR, DATA_EXT))
#     if len(files) != 1:
#         print(f"Error: Expected one file, but found {len(files)}.")
#         exit(1)
#     return files[0]

# Step 2: Print the number of lines and characters in the file
def print_file_stats(DATA_PATH):
    with open(DATA_PATH, 'r') as file:
        lines = file.readlines()
        num_lines = len(lines)
        num_chars = sum(len(line) for line in lines)
        print(f"The file {DATA_FILE_YML}' contains {num_lines} lines and {num_chars} characters.")
        return lines

# Step 3: Append metadata at the beginning of the document
def append_metadata(DATA_PATH, lines):
    last_update = datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M:%S (UTC%z)').replace('+0000', '+00:00')
    last_activity = None
    for line in lines:
        if 'user_profile_activity_1_date_diff' in line:
            last_activity = line.split(":")[-1].strip()
            break
    if not last_activity:
        print("Error: 'user_profile_activity_1_date_diff' not found in the file.")
        exit(1)

    found_last_update, found_last_activity = False, False
    for idx, line in enumerate(lines):
        if line.startswith("last_update:"):
            lines[idx] = f"last_update: {last_update}\n"
            found_last_update = True
        elif line.startswith("last_activity:"):
            lines[idx] = f"last_activity: {last_activity}\n"
            found_last_activity = True

    metadata = []
    if not found_last_update:
        metadata.append(f"last_update: {last_update}\n")
    if not found_last_activity:
        metadata.append(f"last_activity: {last_activity}\n")
    
    if metadata:
        lines = metadata + lines
    return lines

# Step 4: Cleaning function
def clean_file(lines, commands):
    changes = []
    
    for command in commands:
        silent = False
        
        # Check if the command is marked as silent
        if command.startswith("silent "):
            command = command.replace("silent ", "", 1)
            silent = True
        
        # Handle "-r" to remove a specific text from a line
        if command.startswith('-r '):
            match = re.match(r'-r "(.*)"', command)
            if match:
                text = match.group(1)
                for idx, line in enumerate(lines):
                    if text in line:
                        old_value = line.strip()
                        new_value = line.replace(text, "")
                        lines[idx] = new_value
                        if not silent:
                            changes.append((idx + 1, old_value, new_value.strip(), "deletion"))
        
        # Handle "-rF" to remove an entire line containing a key
        elif command.startswith('-rF '):
            match = re.match(r'-rF "(.*)"', command)
            if match:
                key = match.group(1)
                for idx, line in enumerate(lines):
                    if key in line.split(':', 1)[0]:  # Match key before the colon
                        old_value = line.strip()
                        lines[idx] = ""  # Remove the line
                        if not silent:
                            changes.append((idx + 1, old_value, "", "deletion (entire line)"))
        
        # Handle "-c" to replace old text with new text
        elif command.startswith('-c '):
            match = re.match(r'-c "(.*)" "(.*)"', command)
            if match:
                old_text, new_text = match.groups()
                for idx, line in enumerate(lines):
                    if old_text in line:
                        old_value = line.strip()
                        lines[idx] = line.replace(old_text, new_text)
                        if not silent:
                            changes.append((idx + 1, old_value, lines[idx].strip(), "replacement"))

        # Handle "+k" to insert new text before the key (text)
        elif command.startswith('+k '):
            match = re.match(r'\+k "(.*)" "(.*)"', command)
            if match:
                text, new_data = match.groups()
                for idx, line in enumerate(lines):
                    if text in line and ':' in line.split(text)[0]:  # Key domain check
                        old_value = line.strip()
                        lines[idx] = new_data + " " + line
                        changes.append((idx + 1, old_value, lines[idx].strip(), "insertion before key"))

        # Handle "k+" to insert new text after the key (text)
        elif command.startswith('k+ '):
            match = re.match(r'k\+ "(.*)" "(.*)"', command)
            if match:
                text, new_data = match.groups()
                for idx, line in enumerate(lines):
                    if text in line and ':' in line.split(text)[0]:  # Key domain check
                        old_value = line.strip()
                        lines[idx] = line.strip() + " " + new_data + "\n"
                        changes.append((idx + 1, old_value, lines[idx].strip(), "insertion after key"))

        # Handle "+v" to insert new text before the value (text)
        elif command.startswith('+v '):
            match = re.match(r'\+v "(.*)" "(.*)"', command)
            if match:
                text, new_data = match.groups()
                for idx, line in enumerate(lines):
                    if ':' in line and text in line.split(':', 1)[1]:  # Value domain check
                        old_value = line.strip()
                        key, value = line.split(':', 1)  # Split key and value at the first colon
                        new_value = key + ": " + new_data + "" + value.strip()
                        lines[idx] = new_value + "\n"
                        changes.append((idx + 1, old_value, lines[idx].strip(), "insertion before value"))

        # Handle "v+" to insert new text after the value (text)
        elif command.startswith('v+ '):
            match = re.match(r'v\+ "(.*)" "(.*)"', command)
            if match:
                text, new_data = match.groups()
                for idx, line in enumerate(lines):
                    if ':' in line and text in line.split(':', 1)[1]:  # Value domain check
                        old_value = line.strip()
                        key, value = line.split(':', 1)  # Split key and value at the first colon
                        new_value = key + ": " + value.strip() + " " + new_data
                        lines[idx] = new_value
                        changes.append((idx + 1, old_value, lines[idx].strip(), "insertion after value"))

    return lines, changes

# Step 5: Output the changes made
def report_changes(changes, initial_lines, initial_chars, final_lines, final_chars):
    if not changes:
        print("No changes were made.")
    else:
        print(f"\nCleaning dataset..")
        for change in changes:
            line_num, old_value, new_value, action = change
            # print(f"Line {line_num}: {action} performed")
            # print_red(f"    OLD LINE: {old_value}")
            # print_green(f"    NEW LINE: {new_value}")
    
    # # Print initial file stats
    # print(f"\nInitial file statistics: {initial_lines} lines, {initial_chars} characters")
    # # Print final file stats
    # print(f"Final file statistics: {final_lines} lines, {final_chars} characters")
    # Print the difference
    # print(f"Difference: {final_lines - initial_lines} lines, {final_chars - initial_chars} characters")

    # print(f"\nCleanning summary: {initial_lines}/{final_lines} lines (-{final_lines - initial_lines} lines of code), {initial_chars}/{final_chars} characters ({final_chars - initial_chars} characters)")
    print(f"\n {len(changes)} changes made. {final_chars - initial_chars} characters and {final_lines - initial_lines} lines of code were removed.")
    # print(f"\nDifference: {final_lines - initial_lines} lines of code less, {final_chars - initial_chars} characters.")

# Main function to execute the steps
def main():
    # DATA_PATH = find_unique_file(DATA_DIR, DATA_EXT)
    
    # Capture initial file stats
    lines = print_file_stats(DATA_PATH)
    initial_lines = len(lines)
    initial_chars = sum(len(line) for line in lines)
    
    # Apply metadata update (append or update values)
    lines = append_metadata(DATA_PATH, lines)  # Capture updated lines
    
    # Apply cleaning commands using the new format
    commands = [
        # 'silent -r "_thumb"',                             # Silent: remove "_thumb"
        # '-rF "user_profile_sso_id"',                      # Remove entire line with "user_profile_sso_id"
        # '-c "user_profile_" "user_"',                     # Replace "user_profile_" with "user_"
        # '+k "some_key" "new_key"',                        # Insert"new_key" before "some_key"
        # 'k+ "some_key" "more_value"',                     # Insert "more_value" after "some_key"
        # '+v "some_value" "new_prefix"',                   # Insert "new_prefix" before "some_value"
        # '+v " /storage/" "https://labs.hackthebox.com"'   # Insert URL before "/storage/"
        # 
        
        '-r "_thumb"',
        '-rF "user_profile_sso_id"',
        '-c "_attack_paths_" "ap_"',
        '-c "user_profile_user_" "user_profile_"',
        '-c "user_profile_" "user_"',
        '-c "operating_systems" "os"',
        '-c "challenge_categories" "challenge_cat"',
        '-c "Window\'s Infinity" "Windows Infinity"',
        '+v " /storage/" "https://labs.hackthebox.com"'
        
    ]
    lines, changes = clean_file(lines, commands)

    # Capture final file stats
    final_lines = len(lines)
    final_chars = sum(len(line) for line in lines)
    
    # Output the changes
    report_changes(changes, initial_lines, initial_chars, final_lines, final_chars)

    # Write the cleaned file back to disk
    with open(DATA_PATH, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    main()

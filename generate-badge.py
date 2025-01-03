#!/usr/bin/env python3

import os
import sys
import re
import ast
import json
import yaml
import glob
import shutil
import imgkit
import requests

from PIL import Image
from dotenv import dotenv_values
from colorama import Fore, Style
from datetime import datetime, timezone

#################################################################
########################  VARIABLES
#################################################################

# Define the root directory for your project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants
API_URL = "https://labs.hackthebox.com/api/v4"
BASE_URL = "https://labs.hackthebox.com"

# User Config
USER_ID = 780424 # 6-digit user ID (linked to ID1) - 780424 - 000000

BADGE_TEMPLATE_NAME = 'badge-default.html'

# Fixed values
DIR_DATA = 'data'
DIR_USER = f'{DIR_DATA}/user'
BADGE_OUTPUT_DIR = f'{DIR_DATA}'
DIR_ASSETS = 'assets'
YAML_FILE_NAME = 'dataset.yml'
DIR_CSS = f'{DIR_ASSETS}/css'
DIR_JS = f'{DIR_ASSETS}/js'
DIR_TEMPLATES = f'{DIR_ASSETS}/templates'

# Dynamically generated values
YAML_FILE_PATH = f'{DIR_USER}/{YAML_FILE_NAME}'
BADGE_TEMPLATE_PATH = f'{DIR_TEMPLATES}/{BADGE_TEMPLATE_NAME}'
BADGE_OUTPUT_NAME = os.path.splitext(BADGE_TEMPLATE_NAME)[0]
BADGE_OUTPUT_HTML = f'{BADGE_OUTPUT_DIR}/{BADGE_OUTPUT_NAME}.html' 
BADGE_OUTPUT_PNG = f'{BADGE_OUTPUT_DIR}/{BADGE_OUTPUT_NAME}.png'


#################################################################
# print(f"{Fore.GREEN}Executing script_init{Style.RESET_ALL}")
#################################################################

print(Fore.BLUE + "\n Initializing Script.. \n" + Style.RESET_ALL)

print(f"    🔹 User ID set to    => {Style.BRIGHT}{Fore.BLUE}{USER_ID}{Style.RESET_ALL}")
print(f"    🔹 Badge output name => {Style.BRIGHT}{Fore.BLUE}{BADGE_OUTPUT_NAME}{Style.RESET_ALL}")
print(f"    🔹 Badge output dir  => {Style.BRIGHT}{Fore.BLUE}{BADGE_OUTPUT_DIR}{Style.RESET_ALL}")
print(f"    🔹 Selected template => {Style.BRIGHT}{Fore.BLUE}{BADGE_TEMPLATE_NAME}{Style.RESET_ALL}")

# Request Headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Python-Script/1.0'
}

# Create directories if they don't exist
os.makedirs(DIR_DATA, exist_ok=True)
os.makedirs(DIR_USER, exist_ok=True)
os.makedirs(BADGE_OUTPUT_DIR, exist_ok=True)

# Counter to append number to filename
fileid_counter = 1

# URLs to dynamically fetch data from
user_endpoints = {
        "user": f"{API_URL}/profile/{USER_ID}",
        "user_machines": f"{API_URL}/profile/chart/machines/attack/{USER_ID}",
        "user_os": f"{API_URL}/profile/progress/machines/os/{USER_ID}",
        "user_challenges": f"{API_URL}/profile/progress/challenges/{USER_ID}",
        "user_fortresses": f"{API_URL}/profile/progress/fortress/{USER_ID}",
        "user_sherlocks": f"{API_URL}/profile/progress/sherlocks/{USER_ID}",
        "user_endgames": f"{API_URL}/profile/progress/endgame/{USER_ID}",
        "user_prolabs": f"{API_URL}/profile/progress/prolab/{USER_ID}",
        "user_activity": f"{API_URL}/profile/activity/{USER_ID}",
    }

def user_fetch_data(url):
    """Fetch data from a given URL and return JSON response if successful."""
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code} - The profile is private.")
        sys.exit(1)  # Graceful exit with a status code indicating an error

# Variable to track if any save operation fails
user_save_failed = False

# print(f"\n{Fore.GREEN} Initializing Data Fetch.. {Style.RESET_ALL}")
print(Style.BRIGHT + Fore.YELLOW + "\n Generating user data files.. \n" + Style.RESET_ALL)
# print(Fore.CYAN + "\n    🔷 User ID " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + f"{USER_ID}\n" + Style.RESET_ALL)

def user_save_to_json(data, filename):
    """Save the fetched data to a JSON file."""
    global user_save_failed
    try:
        with open(os.path.join(DIR_USER, filename), 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"    🔹 {Fore.MAGENTA}{filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")
        user_save_failed = True  # Mark as failed

if user_save_failed:
    print("Error: One or more files failed to save.")
    sys.exit(1)

def user_process_and_save(endpoint_name, url):
    """Fetch, process, and save the data for a specific endpoint."""
    global fileid_counter
    data = user_fetch_data(url)
    if data:
        user_save_to_json(data, f"UD{fileid_counter}-{endpoint_name}.json")
        fileid_counter += 1  # Increment the counter for the next file

# Loop through all user endpoints and process each
for name, url in user_endpoints.items():
    user_process_and_save(name, url)

print(f"\n    User data files created successfully.")

# Function to check if 'team' key exists in profile_data.json
def check_team_in_profile():
    global TEAM_ID
    profile_file = os.path.join(DIR_USER, next((f for f in os.listdir(DIR_USER) if f.startswith('UD1')), ''))

    TEAM_ID = None
    
    # Check if the file exists
    if os.path.exists(profile_file):
        # Open and read the profile_data.json file
        with open(profile_file, 'r') as file:
            profile_data = json.load(file)
        
        # Navigate through the data and check if the team id is present
        team_info = profile_data.get("profile", {}).get("team", None)

        # Safely handle the case where 'team' is not found
        if team_info and isinstance(team_info, dict):
            TEAM_ID = team_info.get('id', None)
            if TEAM_ID:
                # print(f"{Fore.GREEN} Generating team data files.. {Style.RESET_ALL}\n")
                print(Style.BRIGHT + Fore.YELLOW + "\n Generating team data files.. " + Style.RESET_ALL)
                print(Style.BRIGHT + Fore.CYAN + "\n    🔷 Team ID found => " + Style.RESET_ALL + Style.BRIGHT + Fore.GREEN + f"{TEAM_ID}\n" + Style.RESET_ALL)
            else:
                print(f"\n{Fore.RED} Team ID not found in the team information.{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.RED} Team information not found in the profile data.{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.RED} {profile_file} not found.{Style.RESET_ALL}\n")


# At the end of the script, call the function to check team info in profile_data.json
check_team_in_profile()

if TEAM_ID:
    # URLs to dynamically fetch data from
    team_endpoints = {
        "team": f"{API_URL}/public/team/info/{TEAM_ID}",
        "team_bracket": f"{API_URL}/public/rankings/team/ranking_bracket/{TEAM_ID}",
        "team_rank_best": f"{API_URL}/public/rankings/team/best/{TEAM_ID}?period=1Y",
        "team_machines": f"{API_URL}/public/team/chart/machines/attack/{TEAM_ID}",
        "team_challenges": f"{API_URL}/public/team/chart/challenge/categories/{TEAM_ID}",
    }

    def team_fetch_data(url):
        """Fetch data from a given URL and return JSON response if successful."""
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            return None

    # Variable to track if any save operation fails
    team_save_failed = False

    def team_save_to_json(data, filename):
        """Save the fetched data to a JSON file."""
        global team_save_failed
        try:
            with open(os.path.join(DIR_USER, filename), 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"    🔹 {Fore.MAGENTA}{filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"Failed to save data to {filename}: {e}")
            team_save_failed = True  # Mark as failed

    if team_save_failed:
        print("Error: One or more files failed to save.")
        sys.exit(1)

    def team_process_and_save(endpoint_name, url):
        """Fetch, process, and save the data for a specific endpoint."""
        global fileid_counter
        data = team_fetch_data(url)
        if data:
            team_save_to_json(data, f"UT{fileid_counter}-{endpoint_name}.json")
            fileid_counter += 1  # Increment the counter for the next file

    # Loop through all team endpoints and process each
    for name, url in team_endpoints.items():
        team_process_and_save(name, url)

    print(f"\n    Team data files created successfully.")
else:
    print(f"\n{Fore.MAGENTA} No valid TEAM_ID found. Skipping team data fetch.{Style.RESET_ALL}")
    sys.exit(0)

    # print(f"\nData files created successfully.")


#################################################################
# print(f"{Fore.GREEN}Executing script_make{Style.RESET_ALL}")
#################################################################

# print(f"\n{Fore.GREEN} Generating Dataset.. {Style.RESET_ALL}")
print(Style.BRIGHT + Fore.YELLOW + "\n Generating Dataset.. " + Style.RESET_ALL)

def flatten_json(data, parent_key='', sep='_'):
    """
    Recursively flatten the JSON structure.
    Concatenate nested keys with a separator to make them unique.
    """
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Handle lists of dictionaries (e.g., prolabs or challenge categories)
                for i, item in enumerate(v):
                    items.extend(flatten_json(item, f"{new_key}_{i}", sep=sep).items())
            else:
                items.append((new_key, v))
    elif isinstance(data, list):
        # Handle list case at root level if needed
        for i, item in enumerate(data):
            items.extend(flatten_json(item, f"{parent_key}_{i}", sep=sep).items())
    else:
        # Base case where the value is not a dict or list
        items.append((parent_key, data))
    return dict(items)

def read_json_files(directory):
    """
    Read all JSON files from the given directory, sorted by numerical prefixes.
    If no number is found, those files will be sorted alphabetically.
    """
    def extract_fileid(filename):
        # Extracts the first number from the filename, or returns a default large number for sorting if none found
        match = re.findall(r'\d+', filename)
        return int(match[0]) if match else float('inf')  # Default to a large number if no number is found

    json_files = sorted(
        [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')],
        key=lambda x: extract_fileid(os.path.basename(x))
    )
    return json_files

def json_to_flat_yaml(YAML_FILE_NAME):
    # Directories to read JSON files from
    directories = [f'{DIR_USER}']
    
    # Clean (truncate) the output YAML file at the start
    open(YAML_FILE_NAME, 'w').close()

    # Dictionary to store the combined data
    combined_data = {}

    # Read and append all JSON files' content from both directories in order
    for directory in directories:
        json_files = read_json_files(directory)
        
        for json_file in json_files:
            with open(json_file, 'r') as f:
                json_objects = []
                current_json = ''
                for line in f:
                    line = line.strip()
                    if line:
                        current_json += line
                    if line.endswith('}'):  # When we reach the end of a JSON object
                        try:
                            json_objects.append(json.loads(current_json))
                            current_json = ''  # Reset to capture next JSON object
                        except json.JSONDecodeError:
                            pass  # Silently skip invalid JSON objects

                # Flatten each JSON object and add to the combined data
                for json_obj in json_objects:
                    try:
                        flattened = flatten_json(json_obj)
                        
                        # Check the first two characters of the file name and append the appropriate prefix
                        file_name = os.path.basename(json_file)
                        if file_name.startswith('UD'):
                            flattened = {f"user_{k}": v for k, v in flattened.items()}
                        elif file_name.startswith('UT'):
                            flattened = {f"team_{k}": v for k, v in flattened.items()}

                        combined_data.update(flattened)
                        
                    except AttributeError as e:
                        print(f"Error processing JSON object in file {json_file}: {e}")

    # Convert the combined data to YAML format and write to the output file
    with open(YAML_FILE_PATH, 'a') as f:  # Use 'a' to append in the correct order
        yaml.dump(combined_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

if __name__ == "__main__":

    # Call the conversion function for all JSON files in the specified directories
    json_to_flat_yaml(YAML_FILE_PATH)

    print(f"\n    A dataset with a flattened structure has been successfully generated.")

#################################################################
# print(f"{Fore.GREEN}Executing script_patch{Style.RESET_ALL}")
#################################################################

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

def print_red(text):
    print(f"{Colors.RED}{text}{Colors.RESET}")

def print_green(text):
    print(f"{Colors.GREEN}{text}{Colors.RESET}")

# Step 1: Find the file with the unique extension in the DIR_USER
# def find_unique_file(DIR_USER, DATA_FILE_EXTENSION):
#     files = glob.glob(os.path.join(DIR_USER, DATA_FILE_EXTENSION))
#     if len(files) != 1:
#         print(f"Error: Expected one file, but found {len(files)}.")
#         exit(1)
#     return files[0]

# Step 2: Print the number of lines and characters in the file
def print_file_stats(YAML_FILE_PATH):
    with open(YAML_FILE_PATH, 'r') as file:
        lines = file.readlines()
        num_lines = len(lines)
        num_chars = sum(len(line) for line in lines)
        print(f"\n    🔹 File name: {YAML_FILE_NAME}")
        print(f"    🔹 File details: {num_lines} lines, {num_chars} characters.")
        return lines

# Step 3: Append metadata at the beginning of the document
def append_metadata(YAML_FILE_PATH, lines):
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
        print(f"\n{Fore.YELLOW} Starting dataset clean-up and formatting.. {Style.RESET_ALL}")
        # print(Style.BRIGHT + Fore.YELLOW + "\n Generating Dataset.. \n" + Style.RESET_ALL)
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
    print(f"\n    🔹 Changes made: {len(changes)} ({final_chars - initial_chars} characters and {final_lines - initial_lines} lines of code removed.)")
    # print(f"\nDifference: {final_lines - initial_lines} lines of code less, {final_chars - initial_chars} characters.")

# Main function to execute the steps
def main():
    # YAML_FILE_PATH = find_unique_file(DIR_USER, DATA_FILE_EXTENSION)
    
    # Capture initial file stats
    lines = print_file_stats(YAML_FILE_PATH)
    initial_lines = len(lines)
    initial_chars = sum(len(line) for line in lines)
    
    # Apply metadata update (append or update values)
    lines = append_metadata(YAML_FILE_PATH, lines)  # Capture updated lines
    
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
    with open(YAML_FILE_PATH, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    main()

#################################################################
# print(f"{Fore.GREEN}Executing template_select{Style.RESET_ALL}")
#################################################################

# Load the YAML file and extract all required values
def get_user_data_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        # Extract values or default to None if they don't exist
        return {
            'user_name': data.get('user_name', None),
            'user_rank': data.get('user_rank', None),
            'user_owns': data.get('user_owns', None),
            'user_system_owns': data.get('user_system_owns', None),
            'user_ranking': data.get('user_ranking', None),
            'user_avatar': data.get('user_avatar', None),
            'user_points': data.get('user_points', None),
            'user_respects': data.get('user_respects', None),
            'last_update': data.get('last_update', None),
            'last_activity': data.get('last_activity', None),
        }

# Replace placeholders in the HTML file
def replace_placeholders_in_html(html_path, user_data):
    with open(html_path, 'r') as file:
        html_content = file.read()

    # Track any missing values
    missing_values = []

    # Replace all placeholders in the HTML content
    for key, value in user_data.items():
        placeholder = f'${key}$'
        if value is not None:
            html_content = html_content.replace(placeholder, str(value))
        else:
            missing_values.append(key)

    # Write the updated content back to the HTML file (overwriting the copied file)
    with open(html_path, 'w') as file:
        file.write(html_content)

    # Print if any placeholders were not replaced due to missing values
    if missing_values:
        print(f"\nWarning: The following placeholders were not replaced due to missing values in '{YAML_FILE_NAME}'\n: {', '.join(missing_values)}")
    else:
        # print(f"{Fore.GREEN} Rendering Output.. {Style.RESET_ALL}")
        print(Style.BRIGHT + Fore.YELLOW + " Rendering Output.. " + Style.RESET_ALL)
        print(f"\n    All template placeholders in were successfully replaced. {Style.RESET_ALL}")

# Convert HTML to PNG with transparency
def html_to_png_with_transparency(BADGE_OUTPUT_HTML, BADGE_OUTPUT_PNG):
    # Step 1: Convert HTML to PNG using imgkit
    options = {
        'enable-local-file-access': '',     # Allow local file access if necessary
        'transparent': ''                  # Might not work directly for transparency
        # 'width': '875',                     # Force the width to 826px
        # 'disable-smart-width': '',          # Disable smart width adjustment
    }
    try:
        # Suppress output
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = devnull
            sys.stderr = devnull
            imgkit.from_file(BADGE_OUTPUT_HTML, BADGE_OUTPUT_PNG, options=options)
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            #print(f"\n{Fore.GREEN} ✔️ Badge created succesfully.")
            print(Style.BRIGHT + Fore.GREEN + f"\n ✔️  Badge created succesfully and saved in the {BADGE_OUTPUT_DIR} folder.")
    except Exception as e:
        print(f"\nError generating PNG from {BADGE_OUTPUT_HTML}: {e}\n")
        return

    # Step 2: Check if the PNG file was created successfully
    if not os.path.exists(BADGE_OUTPUT_PNG):
        print(f"\nPNG file {BADGE_OUTPUT_PNG} was not created. Exiting.\n")
        return

    # Step 3: Open the PNG image and process the transparency
    img = Image.open(BADGE_OUTPUT_PNG)
    img = img.convert("RGBA")  # Ensure the image is in RGBA mode

    # Create a new data array for the modified image
    new_data = []
    
    for item in img.getdata():
        # Check if the pixel is white (R=255, G=255, B=255)
        if item[:3] == (255, 255, 255):  # Pure white
            new_data.append((255, 255, 255, 0))  # Make it fully transparent
        else:
            new_data.append(item)  # Keep original pixels

    # Apply the new data to the image and save it
    img.putdata(new_data)
    img.save(BADGE_OUTPUT_PNG, "PNG")
    # print(f"\nConverted {BADGE_OUTPUT_HTML} to PNG with transparent background saved as {BADGE_OUTPUT_PNG}")

# Main execution
if __name__ == "__main__":
    try:
        # Step 1: Copy the BADGE_OUTPUT_NAME file to the target location
        shutil.copyfile(BADGE_TEMPLATE_PATH, BADGE_OUTPUT_HTML)
        # print(f"\n{Fore.GREEN} Preparing Template.. {Style.RESET_ALL}")
        print(Style.BRIGHT + Fore.YELLOW + " \n Preparing Template.. " + Style.RESET_ALL)
        print(f"\n    Template file copied successfully.\n")

        # Step 2: Load user data from YAML
        user_data = get_user_data_from_yaml(YAML_FILE_PATH)

        # Step 3: Replace placeholders in the copied HTML file
        replace_placeholders_in_html(BADGE_OUTPUT_HTML, user_data)

        # Step 4: Convert the updated HTML file to PNG with transparency
        html_to_png_with_transparency(BADGE_OUTPUT_HTML, BADGE_OUTPUT_PNG)

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")

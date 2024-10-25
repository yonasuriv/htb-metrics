#!/usr/bin/env python3
# ID 1 - data_GET_init.py

import requests
import json
import os
import shutil
import sys

# Get environment variables
DATA_DIR = os.environ.get('DATA_DIR')
USER_ID = os.environ.get('USER_ID')

# Constants
API_URL = "https://labs.hackthebox.com/api/v4"

# Request Headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Python-Script/1.0'
}

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)

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

print(f"\nInitializing..\n")

def user_save_to_json(data, filename):
    """Save the fetched data to a JSON file."""
    global user_save_failed
    try:
        with open(os.path.join(DATA_DIR, filename), 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f" {filename} data created.")
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
        user_save_to_json(data, f"ud{fileid_counter}{endpoint_name}.json")
        fileid_counter += 1  # Increment the counter for the next file

# Loop through all user endpoints and process each
for name, url in user_endpoints.items():
    user_process_and_save(name, url)

# Function to check if 'team' key exists in profile_data.json
def check_team_in_profile():
    global TEAM_ID
    profile_file = os.path.join(DATA_DIR, next((f for f in os.listdir(DATA_DIR) if f.startswith('ud1')), ''))

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
                print(f"\n Team ID found: {TEAM_ID}\n")
            else:
                print("Team ID not found in the team information.")
        else:
            print("Team information not found in the profile data.")
    else:
        print(f"{profile_file} not found.")


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
            with open(os.path.join(DATA_DIR, filename), 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f" {filename} data created.")
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
            team_save_to_json(data, f"ut{fileid_counter}{endpoint_name}.json")
            fileid_counter += 1  # Increment the counter for the next file

    # Loop through all team endpoints and process each
    for name, url in team_endpoints.items():
        team_process_and_save(name, url)

    print(f"\nTeam data files created successfully.")
else:
    print("No valid TEAM_ID found. Skipping team data fetch.")
    sys.exit(0)

    # print(f"\nData files created successfully.")


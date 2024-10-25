#!/usr/bin/env python3
# ID 2 - data_GET_create.py

import json
import yaml
import os
import re
from datetime import datetime

# Get environment variables
DATA_FILE_YML = os.environ.get('DATA_FILE_YML')
DATA_PATH = os.environ.get('DATA_PATH')

# Constants
BASE_URL = "https://labs.hackthebox.com"

print(f"\nGenerating dataset..")

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

def json_to_flat_yaml(DATA_FILE_YML):
    # Directories to read JSON files from
    directories = ['data']
    
    # Clean (truncate) the output YAML file at the start
    open(DATA_FILE_YML, 'w').close()

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
                        if file_name.startswith('ud'):
                            flattened = {f"user_{k}": v for k, v in flattened.items()}
                        elif file_name.startswith('ut'):
                            flattened = {f"team_{k}": v for k, v in flattened.items()}

                        combined_data.update(flattened)
                        
                    except AttributeError as e:
                        print(f"Error processing JSON object in file {json_file}: {e}")

    # Convert the combined data to YAML format and write to the output file
    with open(DATA_PATH, 'a') as f:  # Use 'a' to append in the correct order
        yaml.dump(combined_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

if __name__ == "__main__":

    # Call the conversion function for all JSON files in the specified directories
    json_to_flat_yaml(DATA_PATH)

    print(f"\nA dataset with a flattened structure has been successfully generated at {DATA_PATH}.")

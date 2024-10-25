#!/usr/bin/env python3
# ID 0 - main.py

import os
import ast
import subprocess

# User-related configuration
USER_ID = 780424 # 6-digit user ID (linked to ID1) - 780424 - 000000

# Data-related configuration
ROOT_DIR = os.getcwd()
DATA_EXT = '*.yml'                                  # File extension for data files (used in ID3)
DATA_DIR = 'data'                                   # Directory containing data files (used in ID3)
DATA_FILE_YML = 'userdatabase.yml'                  # YML file name (used in ID2 and ID4)
DATA_PATH = f'{DATA_DIR}/{DATA_FILE_YML}'           # Full path to the YML file (used in ID2 and ID4)

# Asset-related configuration
ASSETS_DIR = 'assets'                               # Directory containing asset files (no associated ID)
DIR_CSS = f'{ASSETS_DIR}/css'
DIR_JS = f'{ASSETS_DIR}/js'

DATA_FILE_JS = 'userdata.js'                        # JavaScript file for loading data (no associated ID)
DATA_FILE_JS_PATH = f'{DIR_JS}/{DATA_FILE_JS}'      # Full path to JS file (used in ID4)

BADGE_FILE_NAME = 'badge-default'
BADGE_FILE_HTML = f'{BADGE_FILE_NAME}.html'
DIR_TEMPLATES = f'{ASSETS_DIR}/templates'
TEMPLATE_DEFAULT = f'{DIR_TEMPLATES}/{BADGE_FILE_NAME}.html'

PNG_FILE_NAME = f'{BADGE_FILE_NAME}.png'
PNG_FILE_OUTPUT = f'{ROOT_DIR}/{PNG_FILE_NAME}'

# # Library Priorities: Define ID mappings for specific operations
# # Pull endpoints data and generate individual files
# ID1 = 'data_GET_init.py'                        
# # Get the previous files and create a single dataset
# ID2 = 'data_GET_create.py'                  
# # Sanitize the dataset
# ID3 = 'data_PATCH.py'                          
# # Convert the dataset into a javascript file
# ID4 = 'data_PUT.py'      

# Library Priorities: Define ID mappings for specific operations
ID_SCRIPTS = [
    'data_GET_init.py',     # ID1 - Pull endpoints data and generate individual files
    'data_GET_create.py',   # ID2 - Get the previous files and create a single dataset
    'data_PATCH.py',        # ID3 - Sanitize the dataset
    # 'data_PUT.py',          # ID4 - Convert the dataset into a JavaScript file
    # 'data_CONVERT.py',      # ID5 - Read the dataset and modify the HTML file
    # 'data_GENERATE.py',     # ID6 - Convert the HTML file into a PNG
    'template.py',
]

# Export variables as environment variables for the scripts to use
os.environ['USER_ID'] = str(USER_ID)
os.environ['ROOT_DIR'] = ROOT_DIR
os.environ['DATA_EXT'] = DATA_EXT
os.environ['DATA_DIR'] = DATA_DIR
os.environ['DATA_FILE_YML'] = DATA_FILE_YML
os.environ['DATA_PATH'] = DATA_PATH
os.environ['ASSETS_DIR'] = ASSETS_DIR
os.environ['DIR_CSS'] = DIR_CSS
os.environ['DIR_JS'] = DIR_JS
os.environ['DATA_FILE_JS'] = DATA_FILE_JS
os.environ['DATA_FILE_JS_PATH'] = DATA_FILE_JS_PATH
os.environ['TEMPLATE_DEFAULT'] = TEMPLATE_DEFAULT
os.environ['BADGE_FILE_HTML'] = BADGE_FILE_HTML
os.environ['BADGE_FILE_NAME'] = BADGE_FILE_NAME
os.environ['DIR_TEMPLATES'] = DIR_TEMPLATES
os.environ['PNG_FILE_NAME'] = PNG_FILE_NAME
os.environ['PNG_FILE_OUTPUT'] = PNG_FILE_OUTPUT

def execute_scripts_by_id():
    for script_id in ID_SCRIPTS:
        script_path = os.path.join(ROOT_DIR, 'lib', script_id)
        result = subprocess.run(['python', script_path], check=True)
        
        
        if os.path.isfile(script_path):
            continue
        else:
            print(f"Script {script_id} does not exist at {result.returncode}")

        if result.returncode != 0:
            print(f"Script {script_path} failed with exit code {result.returncode}. Stopping further execution.")
            sys.exit(1)

def main():
    # Execute scripts in the order defined by their ID
    execute_scripts_by_id()

if __name__ == "__main__":
    main()
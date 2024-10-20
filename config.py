#!/usr/bin/env python3

# User-related configuration
USER_ID = 000000  # 6-digit user ID (linked to ID1) - 780424                  

# Data-related configuration
DATA_EXT = '*.yml'                                  # File extension for data files (used in ID3)
DATA_DIR = 'data'                                   # Directory containing data files (used in ID3)
DATA_FILE_YML = 'data.yml'                          # YML file name (used in ID2 and ID4)
DATA_PATH = f'{DATA_DIR}/{DATA_FILE_YML}'           # Full path to the YML file (used in ID2 and ID4)

# Asset-related configuration
ASSETS_DIR = 'assets'                               # Directory containing asset files (no associated ID)
DATA_FILE_JS = 'data_LOAD.js'                       # JavaScript file for loading data (no associated ID)
DATA_FILE_JS_PATH = f'{ASSETS_DIR}/{DATA_FILE_JS}'  # Full path to JS file (used in ID4)


TEMPLATES = f'{ASSETS_DIR}/templates'
TEMPLATE1 = f'{TEMPLATES}/default.html'
BADGE_FILE_HTML = 'badge.html'

# Library Priorities: Define ID mappings for specific operations
PRIORITY_IDS = {
    'ID1': 'data_GET.init',                         # Pull endpoints data and generate individual files
    'ID2': 'data_GET.create',                       # Get the previous files and create a single dataset
    'ID3': 'data_PATCH',                            # Sanitize the dataset
    'ID4': 'data_PUT'                               # Convert the dataset into a javascript file
}

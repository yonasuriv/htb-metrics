#!/usr/bin/env python3
# ID 4 - data_PUT.py

import yaml
import os

# Get environment variables
DATA_FILE_YML = os.environ.get('DATA_FILE_YML')
DATA_PATH = os.environ.get('DATA_PATH')
DATA_FILE_JS_PATH = os.environ.get('DATA_FILE_JS_PATH')

# Step 1: Read YAML file
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Step 2: Generate JavaScript file
def generate_js_from_yaml(yaml_data, output_file):
    with open(output_file, 'w') as js_file:
        js_file.write("// Generated JavaScript from input.yml\n")
        js_file.write("document.addEventListener('DOMContentLoaded', function() {\n")
        
        # Iterate over the YAML data and write JS code for each key-value pair
        for key, value in yaml_data.items():
            js_file.write(f"    document.querySelector('.{key}').textContent = '{value}';\n")
        
        js_file.write("});\n")

# Main function to load YAML and generate JS
if __name__ == "__main__":
        
    yaml_data = load_yaml(DATA_PATH)
    generate_js_from_yaml(yaml_data, DATA_FILE_JS_PATH)
    
    print(f"\nJavaScript file '{DATA_FILE_JS_PATH}' has been generated.")

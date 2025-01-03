import yaml
import os
import shutil  # Used to copy the BADGE_FILE_NAME file
import imgkit
from PIL import Image

# Get environment variables
ROOT_DIR = os.environ.get('ROOT_DIR')
DATA_PATH = os.environ.get('DATA_PATH')
BADGE_FILE_NAME = os.environ.get('BADGE_FILE_NAME')
BADGE_FILE_HTML = os.environ.get('BADGE_FILE_HTML')
PNG_FILE_NAME = os.environ.get('PNG_FILE_NAME')
PNG_FILE_OUTPUT = os.environ.get('PNG_FILE_OUTPUT')
TEMPLATE_DEFAULT = os.environ.get('TEMPLATE_DEFAULT')
DATA_FILE_YML = os.environ.get('DATA_FILE_YML')

# Check if required environment variables are set
if not all([ROOT_DIR, DATA_PATH, BADGE_FILE_NAME, BADGE_FILE_HTML, PNG_FILE_NAME, PNG_FILE_OUTPUT, TEMPLATE_DEFAULT]):
    raise ValueError("One or more required environment variables are not set. Please ensure all are configured correctly.")

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
        print(f"\nWarning: The following placeholders were not replaced due to missing values in '{DATA_FILE_YML}'\n: {', '.join(missing_values)}")
    else:
        print(f"All placeholders in {html_path} were successfully replaced.\n")

# Convert HTML to PNG with transparency
def html_to_png_with_transparency(BADGE_FILE_HTML, PNG_FILE_OUTPUT):
    # Step 1: Convert HTML to PNG using imgkit
    options = {
        'enable-local-file-access': '',     # Allow local file access if necessary
        'transparent': '',                  # Might not work directly for transparency
        # 'width': '875',                     # Force the width to 826px
        # 'disable-smart-width': '',          # Disable smart width adjustment
    }
    try:
        imgkit.from_file(BADGE_FILE_HTML, PNG_FILE_OUTPUT, options=options)
        print(f"\nGenerated PNG from {BADGE_FILE_HTML} successfully.")
    except Exception as e:
        print(f"\nError generating PNG from {BADGE_FILE_HTML}: {e}\n")
        return

    # Step 2: Check if the PNG file was created successfully
    if not os.path.exists(PNG_FILE_OUTPUT):
        print(f"\nPNG file {PNG_FILE_OUTPUT} was not created. Exiting.\n")
        return

    # Step 3: Open the PNG image and process the transparency
    img = Image.open(PNG_FILE_OUTPUT)
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
    img.save(PNG_FILE_OUTPUT, "PNG")
    # print(f"\nConverted {BADGE_FILE_HTML} to PNG with transparent background saved as {PNG_FILE_OUTPUT}")

# Main execution
if __name__ == "__main__":
    try:
        # Step 1: Copy the BADGE_FILE_NAME file to the target location
        shutil.copyfile(TEMPLATE_DEFAULT, BADGE_FILE_HTML)
        print(f"\nCopied template file {TEMPLATE_DEFAULT} to {BADGE_FILE_HTML}\n")

        # Step 2: Load user data from YAML
        user_data = get_user_data_from_yaml(DATA_PATH)

        # Step 3: Replace placeholders in the copied HTML file
        replace_placeholders_in_html(BADGE_FILE_HTML, user_data)

        # Step 4: Convert the updated HTML file to PNG with transparency
        html_to_png_with_transparency(BADGE_FILE_HTML, PNG_FILE_OUTPUT)

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")

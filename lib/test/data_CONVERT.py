import yaml
import os

# Define paths for the YAML and HTML files
yaml_file_path = os.path.join(os.getcwd(), '../data/userdatabase.yml')
html_file_path = os.path.join(os.getcwd(), '../test.html')

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

    # Write the updated content back to the HTML file
    with open(html_path, 'w') as file:
        file.write(html_content)

    # Print if any placeholders were not replaced due to missing values
    if missing_values:
        print(f"Warning: The following placeholders were not replaced due to missing values in 'userdatabase.yml': {', '.join(missing_values)}")
    else:
        print(f"All placeholders in {html_path} were successfully replaced.")

# Main execution
if __name__ == "__main__":
    user_data = get_user_data_from_yaml(yaml_file_path)
    replace_placeholders_in_html(html_file_path, user_data)

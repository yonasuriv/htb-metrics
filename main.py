import config
import importlib
import os
import sys

# Add the root directory (HTB_badge_metrics_final) to sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, 'lib'))

def run_script(script_name):
    """
    Dynamically import and run a Python script from the 'lib' directory.
    """
    script_module = f'{script_name}'  # Reference module using dot notation
    try:
        # Dynamically import the script as a module
        module = importlib.import_module(script_module)
        
        # Try to execute 'main' function if it exists
        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"Module {script_module} does not have a 'main' function.")
    except Exception as e:
        print(f"Error executing {script_module}: {e}")

def main():
    """
    Main function to execute scripts in the order defined by config priorities.
    """
    # Execute the scripts in order
    for priority_id, script_name in config.PRIORITY_IDS.items():
        print(f"Executing {priority_id}: {script_name}")
        run_script(script_name)

if __name__ == "__main__":
    main()

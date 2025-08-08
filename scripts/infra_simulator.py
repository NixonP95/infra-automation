# scripts/infra_simulator.py
# ------------------------------------------
# DevOps Infrastructure Provisioning Simulator
# - Collects & validates VM details from the user
# - Persists machines to configs/instances.json
# - Installs a service (Nginx) via a Bash script
# - Logs everything to logs/provisioning.log
# ------------------------------------------

# Imports section
import json
import subprocess
import sys
import logging
from pathlib import Path
from jsonschema import validate, ValidationError

# Add the src/ directory to the Python path so we can import the Machine class
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.append(str(SRC_DIR))
from machine import Machine

# Ensure logs and configs directories exist before writing files
Path("logs").mkdir(exist_ok=True)
config_file = Path("configs/instances.json")
config_file.parent.mkdir(parents=True, exist_ok=True)

# Absolute path to scripts/setup_nginx.sh (same folder as this .py)
SCRIPT_PATH = Path(__file__).resolve().parent / "setup_nginx.sh"

# ========= Logging setup =========
# - Single, centralized log file for the whole tool
# - Include timestamps, severity, and message
logging.basicConfig(
    filename="logs/provisioning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ========= Input normalization (aliases) =========
# Map common user shortcuts and weird casing to a canonical OS name
OS_aliases = {
    "linux": "linux",
    "lin": "linux",
    "windows": "windows",
    "win": "windows",
    "macos": "macOs",
    "mac": "macOs",
    "osx": "macOs"
}

# Define JSON schema for validating VM configurations
vm_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "os": {"type": "string", "enum": ["linux", "windows", "macOs"]},
        "cpu": {"type": "integer", "minimum": 1},
        "ram": {"type": "integer", "minimum": 1}
    },
    "required": ["name", "os", "cpu", "ram"]
}

def get_user_input():
    """
    Prompt the user for VM details with guard-rails:
    - Friendly messages for the user (print)
    - Developer/audit trail in logs (logging.*)
    - Re-prompt until valid input is received
    """
    print("Create a new virtual machine\n")
    logging.info("Prompted user to create a new machine.")

    while True:
        name = input("Enter machine name: ").strip()
        if not name:
            print("Machine name cannot be empty.\n")
            logging.warning("Empty machine name entered.")
        else:
            break

    while True:
        os_input = input("Enter operating system (linux/windows/macOs): ").strip().lower()
        if os_input in OS_aliases:
            os_type = OS_aliases[os_input]
            break
        print("Invalid OS entered. Please choose from: linux, windows, macOs.\n")
        logging.warning(f"Invalid OS entered: {os_input}")
    
    while True:
        try:
            cpu = int(input("Enter number of CPUs: "))
            if cpu <= 0:
                print("CPU must be greater than 0.\n")
                logging.warning(f"Invalid CPU value entered: {cpu}")
            else:
                break
        except ValueError:
            print("CPU must be a number.\n")
            logging.warning("CPU input was not a number.")
            
    while True:    
        try:
            ram = int(input("Enter amount of RAM (in GB): "))
            if ram <= 0:
                print("RAM must be greater than 0.\n")
                logging.warning(f"Invalid RAM value entered: {ram}")
            else:
                break
        except ValueError:
            print("RAM must be a number.\n")
            logging.warning("RAM input was not a number.")
        
    
    return Machine(name, os_type, cpu, ram)

def save_machine(machine):
    """
    Validate the machine dict against the JSON schema and
    append it to configs/instances.json. Creates the file if missing.
    """
    machine_dict = machine.to_dict()

    # Validate structure/values early to avoid bad data in our file
    try:
        validate(instance=machine_dict, schema=vm_schema)
    except ValidationError as e:
        logging.error(f"Validation failed: {e.message}")
        return

     # Load any existing machines (start fresh if JSON is empty/corrupt)   
    all_machines = []
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                all_machines = json.load(f)
        except json.JSONDecodeError:
            logging.warning("Invalid or empty config file. Overwriting...")
            all_machines = []


    # Append this machine and write back
    all_machines.append(machine_dict)
    with open(config_file, "w") as f:
        json.dump(all_machines, f, indent=4)

    logging.info(f"Machine '{machine.name}' saved successfully.")

def install_service():
    """
    Execute the Bash script to install/configure Nginx.
    - Uses Git Bash on Windows, 'bash' elsewhere
    - Logs success/failure and prints user-friendly messages
    """
    print("\nAttempting to install Nginx...\n")
    logging.info("Attempting to install Nginx...")

    if not SCRIPT_PATH.exists():
        print("Nginx script not found. Skipping.")
        logging.error(f"setup_nginx.sh not found at: {SCRIPT_PATH}")
        return

    bash_path = r"C:\Program Files\Git\bin\bash.exe" if sys.platform == "win32" else "bash"

    try:
        result = subprocess.run(
            [bash_path, str(SCRIPT_PATH)],                  
            check=True,
            text=True
        )
        print("Bash script executed successfully.\n")
        logging.info("Nginx installation script ran successfully.")
    except subprocess.CalledProcessError as e:
        print("Bash script failed to run.")
        logging.error("Nginx installation script failed.")
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    print("Welcome to the VM Provisioner!")
    logging.info("Provisioning session started.")

    # Main loop: create & save machines until the user decides to stop
    while True:
        machine = get_user_input()
        save_machine(machine)
        install_service()

        another_machine = input("Would you like to create another machine? (yes/no): ").strip().lower()
        if another_machine not in ("yes", "y"):
            print("\nProvisioning process completed. Goodbye!")
            logging.info("Provisioner exited by user.")
            break
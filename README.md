# 🛠 DevOps Infrastructure Provisioning & Configuration Automation

## 📌 Project Overview
This project is a **rolling DevOps automation tool** designed to simulate infrastructure provisioning and service configuration.  
It will evolve over time as new concepts are learned, with future enhancements including **AWS** and **Terraform** integrations to create real resources.

At its current stage, the provisioning process is **mocked** to simulate infrastructure automation while focusing on:
- Python modular design
- Input validation
- Service automation with Bash
- Logging and error handling

---

## 🎯 Objectives
- Develop a modular Python-based automation tool that simulates VM provisioning.
- Accept user input for defining virtual machines (VMs).
- Validate input using **Python** and **jsonschema**.
- Store VM configurations in **JSON** format.
- Use **classes** for clean, reusable code.
- Automate service installation using **Bash scripts**.
- Implement logging for both Python and Bash.
- Provide error handling for a robust experience.

---

## 📂 Project Structure
```text
infra-automation/
├─ scripts/
│  ├─ infra_simulator.py      # Main provisioning script (Python)
│  └─ setup_nginx.sh          # Service installer (Bash; dnf/yum/apt-get)
│
├─ configs/
│  └─ instances.json          # Stored VM configurations (runtime data)
│
├─ logs/
│  └─ provisioning.log        # Provisioning & error logs (runtime data)
│
├─ src/
│  └─ machine.py              # Machine class definition
│
├─ requirements.txt           # Python dependencies (pip)
└─ README.md                  # Project documentation


🛠 Prerequisites
Before running this project, ensure you have:

Python 3 installed

pip (Python package manager)

Bash (Windows users can use Git Bash)

apt, yum, or dnf package manager (for Nginx installation on Linux)

##⚙️ Setup Instructions

1️⃣ Clone the repository
bash
Copy
Edit
git clone https://github.com/your-username/infra-automation.git
cd infra-automation
2️⃣ Create a Python virtual environment
bash
Copy
Edit
python -m venv venv
3️⃣ Activate the virtual environment
Windows (PowerShell):

powershell
Copy
Edit
venv\Scripts\Activate.ps1
Linux/macOS:

bash
Copy
Edit
source venv/bin/activate
4️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt

---

▶️ Usage
Run the provisioning tool:

bash
Copy
Edit
python scripts/infra_simulator.py
Example interaction:
vbnet
Copy
Edit
🚀 Welcome to the VM Provisioner!
Let's get your virtual machines up and running.

Create a new virtual machine

Enter machine name: web01
Enter operating system (linux/windows/macOs): lin
Enter number of CPUs: 4
Enter amount of RAM (in GB): 8

 Attempting to install Nginx...

Bash script executed successfully.

Would you like to create another machine? (yes/no): no

✅ Provisioning process completed. Goodbye! 👋
📝 Features
User input validation (name, OS, CPU, RAM).

Aliases for OS names (win → windows, mac → macOs).

Persistent storage in configs/instances.json.

Service automation with Bash (setup_nginx.sh).

Logging system:

Logs stored in logs/provisioning.log.

Captures provisioning start/end, errors, and success messages.

Cross-platform support for Windows, macOS, and Linux.

🔍 Example Log Output (logs/provisioning.log)
pgsql
Copy
Edit
2025-08-07 18:15:23,452 - INFO - Prompted user to create a new machine.
2025-08-07 18:15:25,320 - INFO - Machine 'web01' saved successfully.
2025-08-07 18:15:27,112 - INFO - Nginx installation script ran successfully.
2025-08-07 18:15:29,876 - INFO - Provisioner exited by user.
📦 Requirements
All Python dependencies are listed in requirements.txt:

nginx
Copy
Edit
python3
jsonschema
(You can add more packages here as the project grows.)

📌 Next Steps
Integrate AWS EC2 provisioning using boto3.

Add Terraform templates for real infrastructure creation.

Expand service automation (e.g., Apache, MySQL).

Implement a GUI for easier interaction.

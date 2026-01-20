🔐 GitHub Repository Security Scanner

A developer-focused security scanning tool that analyzes public GitHub repositories to detect exposed secrets, .env files, suspicious configurations, and overall repository structure — all through an intuitive dashboard.

🚀 Key Features

🔍 Scan public GitHub repositories for security insights

🛡️ Detect common security risks and unsafe patterns

📊 Repository-level security overview

⚡ Fast, automated analysis

🌐 Easy-to-use web interface built with Streamlit

🛠️ Tech Stack

Language: Python

UI: Streamlit

Analysis: Regex-based Static Code Analysis

Visualization: Streamlit Charts & Metrics

Deployment: Render

⚙️ Installation & Setup

1️⃣ Clone the repository
git clone https://github.com/JheelPashine123/Git_Analyzer.git;
cd Git_Analyzer

2️⃣ Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
streamlit run streamlit_app.py

🧪 How It Works

User enters a public GitHub repository URL

The repo is cloned temporarily

Files are scanned for:

Secrets

Sensitive files

Configurations

A security report is generated

Repo is cleaned up automatically

Results are shown in an interactive dashboard

👤 Author

Developed by Jheel Pashine

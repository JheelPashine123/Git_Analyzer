# 🔐 GitHub Repository Security Scanner

A developer-focused security scanning tool that analyzes public GitHub repositories to detect exposed secrets, `.env` files, suspicious configurations, and overall repository structure — all through an intuitive dashboard.

---

# 🚀 Key Features

- 🔍 Scan public GitHub repositories for security insights

- 🛡️ Detect common security risks and unsafe patterns

- 📊 Repository-level security overview

- ⚡ Fast, automated analysis

- 🌐 Easy-to-use web interface built with Streamlit

---

# 🛠️ Tech Stack

- **Language:** Python

- **UI:** Streamlit

- **Analysis:** Regex-based Static Code Analysis

- **Visualization:** Streamlit Charts & Metrics

- **Deployment:** Render

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the repository

```bash
git clone https://github.com/JheelPashine123/Git_Analyzer.git

cd Git_Analyzer
```

---

## 2️⃣ Create virtual environment (recommended)

### macOS / Linux

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run the app

```bash
streamlit run streamlit_app.py
```

---

# 🧪 How It Works

1️⃣ User enters a public GitHub repository URL

2️⃣ The repository is cloned temporarily

3️⃣ Files are scanned for:

- Secrets

- Sensitive files

- Unsafe configurations

4️⃣ A security report is generated

5️⃣ Repository data is cleaned automatically

6️⃣ Results are displayed in an interactive dashboard

---

# 👤 Author

Developed by **Jheel Pashine**

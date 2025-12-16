import streamlit as st
import json
import os

from repo_utils import clone_repo
from scanner.file_scanner import scan_repo
from scanner.report_generator import generate_report


# ---------- Page Config ----------
st.set_page_config(
    page_title="GitHub Repo Security Scanner",
    page_icon="🔍",
    layout="wide"
)

# ---------- Header ----------
st.title("🔍 GitHub Repository Security Scanner")
st.markdown(
    "Scan any public GitHub repository for **secrets, .env files, tech stack, and security risks**."
)

st.divider()

# ---------- Input Section ----------
repo_url = st.text_input(
    "📌 Paste GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)

scan_btn = st.button("🚀 Scan Repository")

# ---------- Scan Logic ----------
if scan_btn:
    if not repo_url.strip():
        st.error("Please enter a valid GitHub repository URL.")
    else:
        with st.spinner("Cloning and scanning repository..."):
            try:
                repo_path = clone_repo(repo_url)
                scan_results = scan_repo(repo_path)
                report = generate_report(repo_path, scan_results)

                st.success("✅ Scan completed successfully!")

                # ---------- Summary ----------
                st.subheader("📊 Repository Summary")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Files Scanned", report["summary"]["total_files_scanned"])
                col2.metric("Total Lines", report["summary"]["total_lines"])
                col3.metric("Secrets Found", report["summary"]["secret_hits"])
                col4.metric(".env Files", report["summary"]["env_files_found"])

                st.divider()

                # ---------- Languages ----------
                st.subheader("🧠 Languages Used")
                st.json(report["summary"]["languages"])

                # ---------- Secrets ----------
                st.subheader("🚨 Secrets Detected")

                if report["secrets"]:
                    for s in report["secrets"]:
                        st.warning(f"**{s['type']}** found in `{s['file']}`")
                else:
                    st.success("No secrets detected 🎉")

                # ---------- Env Files ----------
                st.subheader("📁 Environment / Suspicious Files")

                if report["env_files"]:
                    for f in report["env_files"]:
                        st.warning(f)
                else:
                    st.success("No .env or suspicious files found")

                # ---------- Recommendations ----------
                st.subheader("✅ Recommendations")
                for r in report["recommendations"]:
                    st.info(r)

                # ---------- Download Report ----------
                st.divider()
                st.subheader("⬇️ Download Full Report")

                report_json = json.dumps(report, indent=2)

                st.download_button(
                    label="Download JSON Report",
                    data=report_json,
                    file_name="github_security_report.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"❌ Error occurred: {e}")

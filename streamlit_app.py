import streamlit as st
import json
import os

from repo_utils import clone_repo, cleanup_repo
from scanner.file_scanner import scan_repo
from scanner.report_generator import generate_report


# ---------- Page Config ----------
st.set_page_config(
    page_title="GitHub Repo Security Scanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background */
    body {
        background-color: #fafbfc;
    }
    
    /* Main title styling */
    h1 {
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
        font-weight: 700;
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #2c3e50;
        border-bottom: 1px solid #e1e8ed;
        padding-bottom: 9px;
        font-weight: 600;
    }
    
    /* Card styling */
   .card-section {
    background: linear-gradient(135deg, #1e293b 0%, #2b2f4a 100%);
    padding: 18px 20px;
    border-radius: 14px;
    border: 1px solid #eef1f6;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    margin: 14px 0;
}
    
    /* Metric boxes */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
        transition: transform 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
    }
    
    /* Button styling */
    button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Thin divider */
    hr {
        border: none;
        border-top: 1px solid #e1e8ed;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1>🔍 GitHub Repository Security Scanner</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #555; font-size: 16px; margin-bottom: 30px;'>
    Scan any public GitHub repository for <b>secrets, .env files, tech stack, and security risks</b>.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- Input Section ----------
st.markdown("<div class='card-section'>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    repo_url = st.text_input(
        "📌 Paste GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        label_visibility="collapsed"
    )

with col2:
    st.write("")  # Space for alignment
    scan_btn = st.button("🚀 Scan Repository", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Scan Logic ----------
if scan_btn:
    if not repo_url.strip():
        st.error("❌ Please enter a valid GitHub repository URL.")
    else:
        with st.spinner("⏳ Cloning and scanning repository..."):
            try:
                repo_path = clone_repo(repo_url)
                scan_results = scan_repo(repo_path)
                report = generate_report(repo_path, scan_results)
                cleanup_repo(repo_path)

                st.success("✅ Scan completed successfully!")

                # ---------- Summary Section ----------
                st.markdown("<div class='card-section'>", unsafe_allow_html=True)
                st.markdown("<h2>📊 Repository Summary</h2>", unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("📄 Files Scanned", report["summary"]["total_files_scanned"])
                with col2:
                    st.metric("📝 Total Lines", report["summary"]["total_lines"])
                with col3:
                    st.metric("🔑 Secrets Found", report["summary"]["secret_hits"], 
                             delta_color="inverse" if report["summary"]["secret_hits"] > 0 else "normal")
                with col4:
                    st.metric("⚠️ .env Files", report["summary"]["env_files_found"],
                             delta_color="inverse" if report["summary"]["env_files_found"] > 0 else "normal")
                st.markdown("</div>", unsafe_allow_html=True)

                # ---------- Languages Section ----------
                st.markdown("<div class='card-section'>", unsafe_allow_html=True)
                st.markdown("<h2>🧠 Languages & Tech Stack Detected</h2>", unsafe_allow_html=True)
                
                if report["summary"]["languages"]:
                    # Create a nice display for languages
                    lang_col1, lang_col2 = st.columns(2)
                    
                    with lang_col1:
                        # Bar chart of languages
                        st.bar_chart(report["summary"]["languages"])
                    
                    with lang_col2:
                        st.write("**Detected Languages:**")
                        for lang, count in sorted(report["summary"]["languages"].items(), 
                                                 key=lambda x: x[1], reverse=True):
                            st.write(f"• **{lang}**: {count} files")
                else:
                    st.info("No programming languages detected in this repository.")
                st.markdown("</div>", unsafe_allow_html=True)

                # ---------- Project Structure Section ----------
                st.markdown("<div class='card-section'>", unsafe_allow_html=True)
                st.markdown("<h2>🏗️ Project Structure & Features</h2>", unsafe_allow_html=True)
                
                struct_col1, struct_col2, struct_col3 = st.columns(3)
                
                with struct_col1:
                    st.metric("📋 Has README", "✅" if report["summary"]["has_readme"] else "❌")
                with struct_col2:
                    st.metric("📜 Has LICENSE", "✅" if report["summary"]["has_license"] else "❌")
                with struct_col3:
                    st.metric("🐳 Has Dockerfile", "✅" if report["summary"]["dockerfile"] else "❌")

                if report["summary"]["requirements_count"] > 0:
                    st.success(f"📦 Found **{report['summary']['requirements_count']}** dependencies in requirements.txt")
                st.markdown("</div>", unsafe_allow_html=True)

                # ---------- Security Findings Section ----------
                st.markdown("<div class='card-section'>", unsafe_allow_html=True)
                st.markdown("<h2>🚨 Security Findings</h2>", unsafe_allow_html=True)

                # Secrets section
                st.markdown("### 🔐 Secrets Detected")
                if report["secrets"]:
                    for i, s in enumerate(report["secrets"], 1):
                        with st.expander(f"**⚠️ {s['type']}** (Finding #{i})", expanded=False):
                            st.write(f"**File:** `{s['file']}`")
                            st.warning(f"Found secret of type: **{s['type']}**", icon="⚠️")
                else:
                    st.success("✅ No secrets detected in this repository!", icon="✅")

                st.divider()

                # Env files section
                st.markdown("### 📁 Suspicious Files")
                if report["env_files"]:
                    for f in report["env_files"]:
                        st.warning(f"⚠️ `{f}`", icon="⚠️")
                else:
                    st.success("✅ No .env or suspicious files found!", icon="✅")
                st.markdown("</div>", unsafe_allow_html=True)

                # ---------- Recommendations Section ----------
                st.markdown("<div class='card-section'>", unsafe_allow_html=True)
                st.markdown("<h2>✅ Security Recommendations</h2>", unsafe_allow_html=True)
                for i, r in enumerate(report["recommendations"], 1):
                    if "critical" in r.lower() or "immediately" in r.lower():
                        st.error(f"🔴 {r}", icon="🔴")
                    elif "No critical" in r:
                        st.success(f"✅ {r}", icon="✅")
                    else:
                        st.info(f"💡 {r}", icon="💡")
                st.markdown("</div>", unsafe_allow_html=True)

                # ---------- Download Report Section ----------
                st.markdown("<div class='card-section'>", unsafe_allow_html=True)
                st.markdown("<h2>⬇️ Export Report</h2>", unsafe_allow_html=True)

                col_json, col_info = st.columns([2, 1])
                
                with col_json:
                    report_json = json.dumps(report, indent=2)
                    st.download_button(
                        label="📥 Download Full JSON Report",
                        data=report_json,
                        file_name=f"github_security_report_{report['scanned_at'].replace(':', '-')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col_info:
                    st.caption(f"Scanned: {report['scanned_at']}")
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                error_str = str(e)
                
                # Check if it's a private repo error
                if "PRIVATE" in error_str or "private" in error_str:
                    st.error(error_str, icon="🔒")
                    st.markdown("""
                    ---
                    **Why is this happening?**
                    
                    This scanner can only access **public repositories**. Private repositories require authentication 
                    and special permissions which aren't supported in this tool.
                    
                    **What you can do:**
                    1. Make the repository public temporarily for scanning
                    2. Run this scanner on a different public repository
                    3. Contact the repository owner to make it public
                    """)
                else:
                    st.error(f"❌ Error occurred: {error_str}", icon="❌")
                    st.write("Please ensure the GitHub URL is valid and the repository is public.")

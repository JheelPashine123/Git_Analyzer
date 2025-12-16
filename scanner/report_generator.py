import os
import json
from datetime import datetime


def generate_report(repo_path, scan_results):
    """Generates a security & structure report for a repository."""

    summary = {
        "total_files_scanned": scan_results.get("total_files", 0),
        "total_lines": scan_results.get("total_lines", 0),
        "env_files_found": len(scan_results.get("env_files", [])),
        "secret_hits": len(scan_results.get("secrets", [])),
        "languages": scan_results.get("languages", {}),
        "has_readme": scan_results.get("has_readme", False),
        "has_license": scan_results.get("has_license", False),
        "requirements_count": len(scan_results.get("requirements", [])),
        "dockerfile": scan_results.get("dockerfile", False),
        "ci_configs_count": len(scan_results.get("ci_configs", []))
    }

    report = {
        "repo_path": repo_path,
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": summary,
        "env_files": scan_results.get("env_files", []),
        "secrets": scan_results.get("secrets", []),
        "requirements": scan_results.get("requirements", []),
        "recommendations": []
    }

    # Add recommendations
    if summary["env_files_found"] > 0:
        report["recommendations"].append(
            "Remove .env files from repository and add them to .gitignore"
        )

    if summary["secret_hits"] > 0:
        report["recommendations"].append(
            "Rotate exposed secrets immediately and revoke old keys"
        )

    if not report["recommendations"]:
        report["recommendations"].append(
            "No critical security issues detected"
        )

    return report

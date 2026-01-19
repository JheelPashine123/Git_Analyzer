import os
import shutil
import subprocess

TEMP_DIR = "temp_repos"

def clone_repo(repo_url):
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_path = os.path.join(TEMP_DIR, repo_name)

    # delete old copy if exists
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    try:
        result = subprocess.run(
            ["git", "clone", repo_url, repo_path],
            check=True,
            capture_output=True,
            text=True
        )
        return repo_path
    except subprocess.CalledProcessError as e:
        # Check if error is due to private repo or authentication
        error_msg = e.stderr.lower()
        if "permission denied" in error_msg or "authentication" in error_msg or "not found" in error_msg:
            raise Exception(
                "🔒 This repository appears to be **PRIVATE**. \n\n"
                "This scanner only works with **public repositories**. "
                "Please ensure the repository is public or provide a public URL."
            )
        else:
            raise Exception(f"Failed to clone repository: {e.stderr}")

def get_all_files(repo_path):
    all_files = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    return all_files

def cleanup_repo(repo_path):
    """Delete the cloned repository after scanning"""
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

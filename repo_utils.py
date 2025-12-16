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

    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    return repo_path

def get_all_files(repo_path):
    all_files = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    return all_files

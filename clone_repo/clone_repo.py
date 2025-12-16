import os
import subprocess
import uuid

def clone_repo(repo_url):
    # create unique folder for each repo
    repo_id = str(uuid.uuid4())[:8]
    target_dir = f"repos/repo_{repo_id}"

    os.makedirs("repos", exist_ok=True)

    print("📥 Cloning repository...")
    subprocess.run(
        ["git", "clone", repo_url, target_dir],
        check=True
    )

    return target_dir


if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ").strip()
    local_path = clone_repo(repo_url)

    print(f"✅ Repo cloned at: {local_path}")

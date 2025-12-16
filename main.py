import json
import os
import sys
from repo_utils import clone_repo, get_all_files
from scanner.file_scanner import scan_repo
from scanner.report_generator import generate_report


def main():
    repo_url = input("Paste GitHub repo URL: ")

    # Allow local path input for faster testing
    if os.path.exists(repo_url):
        repo_path = repo_url
    else:
        try:
            repo_path = clone_repo(repo_url)
        except Exception as e:
            print(f"Error cloning repository: {e}")
            sys.exit(1)

    files = get_all_files(repo_path)
    print(f"Total files found: {len(files)}")

    scan_results = scan_repo(repo_path)

    report = generate_report(repo_path, scan_results)

    # save report
    repo_name = os.path.basename(repo_path.rstrip('/'))
    report_path = f"github_report_{repo_name}.json"

    with open(report_path, 'w', encoding='utf-8') as rf:
        json.dump(report, rf, indent=2)

    print(f"Report saved to {report_path}")
    print(json.dumps(report['summary'], indent=2))


if __name__ == '__main__':
    main()

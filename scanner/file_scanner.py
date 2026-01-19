import os
import re

# Common secret patterns
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+=]{40}['\"]",
    "Generic API Key": r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
    "Password": r"(?i)password\s*=\s*['\"][^'\"]+['\"]",
    "JWT Token": r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
}

SUSPICIOUS_FILES = [
    ".env",
    ".env.local",
    ".env.prod",
    "config.js",
    "settings.py"
]

EXT_LANGUAGE_MAP = {
    # Python
    '.py': 'Python',
    '.pyw': 'Python',
    '.pyx': 'Python',
    
    # JavaScript & TypeScript
    '.js': 'JavaScript',
    '.mjs': 'JavaScript',
    '.cjs': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript',
    '.jsx': 'JavaScript',
    
    # Java & JVM
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.groovy': 'Groovy',
    
    # Go
    '.go': 'Go',
    
    # Rust
    '.rs': 'Rust',
    
    # Ruby
    '.rb': 'Ruby',
    '.erb': 'Ruby (ERB)',
    
    # PHP
    '.php': 'PHP',
    '.phtml': 'PHP',
    
    # C/C++
    '.c': 'C',
    '.h': 'C',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.hpp': 'C++',
    '.hh': 'C++',
    
    # C#
    '.cs': 'C#',
    
    # Swift
    '.swift': 'Swift',
    
    # Objective-C
    '.m': 'Objective-C',
    '.mm': 'Objective-C++',
    
    # Shell
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.zsh': 'Zsh',
    
    # CSS/SCSS/LESS
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'LESS',
    
    # HTML
    '.html': 'HTML',
    '.htm': 'HTML',
    
    # SQL
    '.sql': 'SQL',
    
    # Markup/Config
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.xml': 'XML',
    '.toml': 'TOML',
    '.ini': 'INI',
    '.cfg': 'Config',
    '.conf': 'Config',
    
    # Markdown
    '.md': 'Markdown',
    '.markdown': 'Markdown',
    
    # R
    '.r': 'R',
    '.R': 'R',
    
    # Julia
    '.jl': 'Julia',
    
    # Perl
    '.pl': 'Perl',
    '.pm': 'Perl',
    
    # Lua
    '.lua': 'Lua',
    
    # Dart
    '.dart': 'Dart',
    
    # Elixir
    '.ex': 'Elixir',
    '.exs': 'Elixir',
    
    # Haskell
    '.hs': 'Haskell',
    
    # Clojure
    '.clj': 'Clojure',
    '.cljs': 'ClojureScript',
    
    # Dockerfile
    'Dockerfile': 'Docker',
    '.dockerfile': 'Docker',
}


def scan_repo(repo_path: str):
    """Scan repository for secrets and produce basic repo metrics."""
    findings = {
        "total_files": 0,
        "total_lines": 0,
        "languages": {},
        "env_files": [],
        "suspicious_files": [],
        "secrets": [],
        "has_readme": False,
        "has_license": False,
        "requirements": [],
        "dockerfile": False,
        "ci_configs": []
    }

    from collections import defaultdict
    lang_counts = defaultdict(int)

    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            findings["total_files"] += 1

            lower = file.lower()

            # Readme / License / Dockerfile / CI
            if lower.startswith('readme'):
                findings["has_readme"] = True
            if 'license' in lower or lower == 'license' or lower.startswith('license'):
                findings["has_license"] = True
            if file == 'Dockerfile':
                findings["dockerfile"] = True
            if root.find('.github') != -1 or (lower.endswith(('.yml', '.yaml')) and '.github' in root):
                findings["ci_configs"].append(file_path)

            if lower in SUSPICIOUS_FILES:
                findings["env_files"].append(file_path)

            # Count lines and detect languages
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
                    lines = fh.readlines()
                    findings["total_lines"] += len(lines)

                    # detect secrets
                    content = ''.join(lines)
                    for secret_name, pattern in SECRET_PATTERNS.items():
                        if re.search(pattern, content):
                            findings["secrets"].append({
                                "type": secret_name,
                                "file": file_path
                            })

                    # requirements
                    if file == 'requirements.txt':
                        for l in lines:
                            l = l.strip()
                            if l and not l.startswith('#'):
                                findings['requirements'].append(l)

            except Exception:
                # skip binary or unreadable files
                continue

            # language by extension
            _, ext = os.path.splitext(file)
            lang = EXT_LANGUAGE_MAP.get(ext) or EXT_LANGUAGE_MAP.get(file)
            if lang:
                lang_counts[lang] += 1

    findings['languages'] = dict(lang_counts)

    return findings


# backward compatibility
scan_repository = scan_repo

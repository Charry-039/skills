#!/usr/bin/env python3
"""
check-staged.py - Pre-check staged changes and scan for sensitive files
Usage: python scripts/check-staged.py
Cross-platform: Windows / Linux / macOS
"""
import subprocess
import sys
import re


def run(cmd):
    """Run a shell command, return stdout."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"  Command failed: {cmd} -> {e}")
        return ""


def main():
    print("=== Git Status ===")
    status = run("git status --short")
    print(status or "(no changes)")
    print()

    print("=== Staged Files ===")
    staged_files_str = run("git diff --cached --name-only")
    staged_files = [f for f in staged_files_str.split("\n") if f]
    print("\n".join(staged_files) if staged_files else "(none)")
    print()

    print("=== Staged Diff Stats ===")
    stats = run("git diff --cached --stat")
    print(stats or "(none)")
    print()

    # Sensitive file patterns
    SENSITIVE_PATTERNS = [
        r"\.env",
        r"\.pem$",
        r"\.key$",
        r"credentials",
        r"id_rsa",
        r"\.npmrc",
        r"secret",
        r"\.p12$",
        r"\.pfx$",
        r"aws_",
        r"gcp-",
        r"azure-",
    ]

    print("=== Sensitive File Scan ===")
    found_sensitive = []
    for file in staged_files:
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, file, re.IGNORECASE):
                found_sensitive.append(file)
                break

    if found_sensitive:
        print("WARNING: sensitive files found:")
        for f in found_sensitive:
            print(f"  - {f}")
            print("Please handle manually before continuing.")
        sys.exit(1)
    else:
            print("No sensitive files found.")
    print()

    # Binary / build artifact patterns
    BINARY_PATTERNS = [
        r"\.log$",
        r"\.tmp$",
        r"\.temp$",
        r"/dist/",
        r"/build/",
        r"/node_modules/",
        r"\.cache/",
    ]

    print("=== Binary / Build Artifact Scan ===")
    found_binary = []
    for file in staged_files:
        for pattern in BINARY_PATTERNS:
            if re.search(pattern, file):
                found_binary.append(file)
                break

    if found_binary:
        print("WARNING: possible files that should not be committed:")
        for f in found_binary:
            print(f"  - {f}")
    else:
            print("No obvious build artifacts or log files found.")
    print()

    # Staged + unstaged same-file check
    print("=== Staged + Unstaged Same-File Check ===")
    unstaged_files_str = run("git diff --name-only")
    unstaged_files = set(f for f in unstaged_files_str.split("\n") if f)
    staged_set = set(staged_files)

    common = staged_set & unstaged_files
    if common:
        print("WARNING: the following files are both staged and unstaged:")
        for f in sorted(common):
            print(f"  - {f}")
        print("This workflow may affect working tree state.")
    else:
        print("No files are both staged and unstaged.")
    print()

    # Branch state
    print("=== Branch Status ===")
    branch = run("git rev-parse --abbrev-ref HEAD")
    print(f"Current branch: {branch}")

    # Check unpushed commits — use Python to handle remote detection properly
    unpushed = ""
    try:
        # Get remote tracking branch
        tracking = run("git rev-parse --abbrev-ref %s@{upstream}" % branch)
        if tracking:
            unpushed = run(f"git log {tracking}..{branch} --oneline")
    except Exception:
        pass

    if unpushed:
        print("WARNING: unpushed commits found:")
        print(unpushed)
    else:
        print("No unpushed commits (or no upstream).")
    print()

    print("=== Check complete ===")


if __name__ == "__main__":
    main()
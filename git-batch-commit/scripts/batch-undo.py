#!/usr/bin/env python3
"""
batch-undo.py - Undo commits created by the last batch-commit run
Usage:
    python scripts/batch-undo.py                    # interactive confirmation
    python scripts/batch-undo.py --all              # undo all without per-commit confirmation

Cross-platform: Windows / Linux / macOS
"""
import argparse
import subprocess
import sys


def run(cmd, capture=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return result.stdout.strip() if capture else None


def main():
    parser = argparse.ArgumentParser(description="Undo commits from the last batch-commit run")
    parser.add_argument("--all", action="store_true", help="Undo all without per-commit confirmation")
    args = parser.parse_args()

    # Check if .git-batch-manifest.json exists
    import os
    manifest_file = ".git-batch-manifest.json"
    manifest_exists = os.path.exists(manifest_file)

    if manifest_exists:
        print(f">>> Found manifest file: {manifest_file}")
        print(">>> Last batch commit records are available.")
    else:
        print(">>> Manifest file not found, attempting to infer from recent commits.")

    # Get recent commits
    print("\n=== Last 10 commits ===")
    log = run("git log --oneline -10")
    print(log or "(no commits)")

    print()
    commits = []

    # Try to read from manifest
    if manifest_exists:
        import json
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            commits = [(m["message"], None) for m in manifest.get("commits", [])]
        except Exception:
            pass

    # If no manifest, prompt for count
    if not commits:
        print(">>> Enter the number of commits to undo (default 1):")
        count_input = input("Count: ").strip()
        try:
            count = int(count_input) if count_input else 1
        except ValueError:
            print("Invalid input, using default 1")
            count = 1

        for i in range(count):
            commits.append((f"commit {i+1}", None))

    # Confirm undo
    if args.all:
        print(f"\n>>> Will undo {len(commits)} commits (--all mode)")
    else:
        print(f"\n>>> Will undo {len(commits)} commits (interactive mode)")
        confirm = input("Confirm undo? Type 'yes' to continue: ").strip()
        if confirm != "yes":
            print("Undo canceled.")
            sys.exit(0)

    # Execute undo
    for i, (msg, _) in enumerate(reversed(commits), 1):
        print(f">>> Undo [{i}/{len(commits)}]: {msg}")
        run("git reset --soft HEAD~1")
        print("    >>> Undid one commit (soft reset)")
        print("    Files restored to staged state.")

    print("\n=== Undo complete ===")
    print(f"Undid {len(commits)} commits. All changes are staged.")
    print("To discard changes completely, run: git reset --hard HEAD~N")

    if manifest_exists:
        try:
            os.remove(manifest_file)
            print("Manifest file cleaned up.")
        except Exception:
            pass


if __name__ == "__main__":
    main()
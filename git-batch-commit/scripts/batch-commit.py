#!/usr/bin/env python3
"""
batch-commit.py - Run git commits in batches (based on a manifest file)
Usage:
    python scripts/batch-commit.py                    # run
    python scripts/batch-commit.py --dry-run          # preview
    python scripts/batch-commit.py --rollback-on-fail  # rollback on failure

Cross-platform: Windows / Linux / macOS
"""
import argparse
import glob
import json
import os
import subprocess
import sys


def run(cmd, check=True, capture=True):
    """Run a git command, return result."""
    result = subprocess.run(
        cmd, shell=True, capture_output=capture, text=True
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Run git commits in batches")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no commits")
    parser.add_argument("--rollback-on-fail", action="store_true", help="Rollback on failure")
    args = parser.parse_args()

    manifest_file = ".git-batch-manifest.json"

    if not os.path.exists(manifest_file):
        print(f"Error: manifest file not found: {manifest_file}")
        print("Please generate a grouping plan first (run the git-batch-commit skill).")
        sys.exit(1)

    print(f">>> Read manifest: {manifest_file}")
    if args.dry_run:
        print(">>> Mode: DRY-RUN (preview only, no commits)")
    print()

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    commits = manifest.get("commits", [])
    total = len(commits)

    # Save current HEAD for rollback
    original_head = run("git rev-parse HEAD", check=True, capture=True).stdout.strip()
    print(f">>> Current HEAD: {original_head}")

    successful = []

    for idx, item in enumerate(commits, 1):
        msg = item.get("message", "")
        files = item.get("files", [])

        if not msg or not files:
            print(f"Warning: commit {idx} missing message or files, skipping")
            continue

        print(f">>> [{idx}/{total}] {msg}")

        # Expand glob patterns
        expanded = []
        for pattern in files:
            matched = glob.glob(pattern, recursive=True)
            if matched:
                expanded.extend(matched)
            elif os.path.exists(pattern):
                expanded.append(pattern)
            else:
                expanded.append(pattern)

        expanded = sorted(set(expanded))
        print(f"    File patterns: {', '.join(files)}")
        print(f"    Expanded:      {', '.join(expanded)}")

        if args.dry_run:
            # Dry-run: simulate git add without staging
            run("git reset HEAD --quiet", check=True)
            file_list = " ".join(f'"{f}"' for f in expanded)
            run(f"git add --dry-run {file_list}", check=True, capture=True)
            print(f"    [DRY-RUN] git add {' '.join(expanded)}")
            print(f"    [DRY-RUN] git commit -m \"{msg}\"")
            print("    >>> Dry-run: this commit would succeed")
        else:
            # Execute
            run("git reset HEAD --quiet", check=True)
            file_list = " ".join(f'"{f}"' for f in expanded)
            run(f"git add {file_list}", check=True)

            staged = run("git diff --cached --name-only", check=True, capture=True).stdout.strip()
            print(f"    Staged: {staged or '(none)'}")

            result = run(f'git commit -m "{msg}"', check=False, capture=True)

            if result.returncode == 0:
                commit_hash = run("git rev-parse --short HEAD", check=True, capture=True).stdout.strip()
                print(f"    >>> Commit succeeded ({commit_hash})")
                successful.append((msg, commit_hash))
            else:
                print(f"    >>> Commit failed: {result.stderr.strip()}")
                run("git reset HEAD --quiet", check=True)

                if args.rollback_on_fail and successful:
                    print(f"\n!!! Rollback mode enabled, resetting to: {original_head}")
                    run(f"git reset --hard {original_head}", check=True)
                    print(f"Rolled back {len(successful)} commits")
                elif successful:
                    print(f"\n!!! Failed on commit {idx}. {len(successful)} commits succeeded and remain on the branch.")
                    for m, h in successful:
                        print(f"  - {m} ({h})")
                    print("\nTo rollback, run: git reset --hard <desired-head>")
                sys.exit(1)

        print()

    if args.dry_run:
        print("=== Dry-run complete ===")
        print("These are the operations the script would run. No commits were created.")
        print(f"Manifest file retained at: {manifest_file}")
        print("When ready, run: python scripts/batch-commit.py")
    else:
        if os.path.exists(manifest_file):
            os.remove(manifest_file)
        print("=== Execution complete ===")
        print(f"Success: {len(successful)} commits")
        if successful:
            print("Commit list:")
            for msg, h in successful:
                print(f"  - {msg} ({h})")
        print("\nManifest file cleaned up.")


if __name__ == "__main__":
    main()
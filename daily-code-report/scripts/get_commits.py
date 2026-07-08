#!/usr/bin/env python3
"""
获取指定日期范围内的 git commit 历史。

用法：
    python3 get_commits.py --repo <PATH> --since <ISO8601> --until <ISO8601> --author <NAME>

输出：
    JSON 数组，每个元素包含 hash、date、author、message、files。
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git_command(repo, args):
    """在指定仓库运行 git 命令，返回输出字符串。"""
    result = subprocess.run(
        ["git", "-C", str(repo)] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"git 命令失败: {result.stderr.strip()}")
    return result.stdout


def validate_repo(repo):
    """验证路径是 git 仓库。"""
    repo_path = Path(repo).resolve()
    if not repo_path.exists():
        raise FileNotFoundError(f"仓库路径不存在: {repo_path}")
    if not repo_path.is_dir():
        raise NotADirectoryError(f"仓库路径不是目录: {repo_path}")

    try:
        run_git_command(repo_path, ["rev-parse", "--git-dir"])
    except RuntimeError as exc:
        raise RuntimeError(f"指定路径不是 git 仓库: {repo_path}") from exc

    return repo_path


def parse_commits(repo, since, until, author):
    """解析 git log 输出为结构化数据。"""
    # 使用 --name-only 获取文件列表，配合 --pretty 自定义分隔符
    log_format = "%H%x1f%ai%x1f%an%x1f%s%x1e"
    args = [
        "log",
        f"--since={since}",
        f"--until={until}",
        f"--author={author}",
        "--pretty=format:" + log_format,
        "--name-only",
        "--no-merges",
        "--reverse",
    ]

    output = run_git_command(repo, args)
    if not output.strip():
        return []

    commits = []
    current_commit = None

    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue

        # 包含 \x1f 的行是 commit 元数据行
        if "\x1f" in line:
            if current_commit is not None:
                commits.append(current_commit)

            meta_parts = line.split("\x1f")
            if len(meta_parts) < 4:
                current_commit = None
                continue

            commit_hash, date_str, commit_author, message = meta_parts[:4]

            # 标准化日期格式
            try:
                date_obj = datetime.fromisoformat(date_str.strip())
                date_iso = date_obj.isoformat()
            except ValueError:
                date_iso = date_str.strip()

            current_commit = {
                "hash": commit_hash.strip()[:7],
                "date": date_iso,
                "author": commit_author.strip(),
                "message": message.strip(),
                "files": [],
            }
        elif current_commit is not None:
            current_commit["files"].append(line)

    if current_commit is not None:
        commits.append(current_commit)

    return commits


def main():
    parser = argparse.ArgumentParser(description="获取 git commit 历史")
    parser.add_argument("--repo", required=True, help="git 仓库路径")
    parser.add_argument("--since", required=True, help="开始时间（ISO8601）")
    parser.add_argument("--until", required=True, help="结束时间（ISO8601）")
    parser.add_argument("--author", required=True, help="作者名")

    args = parser.parse_args()

    try:
        repo_path = validate_repo(args.repo)
        commits = parse_commits(repo_path, args.since, args.until, args.author)
        print(json.dumps(commits, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

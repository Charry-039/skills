#!/usr/bin/env python3
"""
batch-commit.py - 基于清单文件批量运行 git 提交
Usage:
    python scripts/batch-commit.py                     # 执行提交
    python scripts/batch-commit.py --dry-run           # 空运行预览（零副作用，不动索引）
    python scripts/batch-commit.py --rollback-on-fail  # 失败时自动回滚
    python scripts/batch-commit.py --force             # 跳过暂存文件覆盖度检查

Cross-platform: Windows / Linux / macOS
"""
import argparse
import fnmatch
import glob
import json
import os
import subprocess
import sys


def run(cmd, check=True, capture=True):
    """运行 git 命令，返回结果。"""
    result = subprocess.run(
        cmd, shell=True, capture_output=capture, text=True
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"命令执行失败: {cmd}\n{result.stderr}")
    return result


def main():
    parser = argparse.ArgumentParser(description="按批次运行 git 提交")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不提交")
    parser.add_argument("--rollback-on-fail", action="store_true", help="失败时回滚")
    parser.add_argument("--force", action="store_true", help="跳过暂存文件覆盖度检查")
    args = parser.parse_args()

    manifest_file = ".git-batch-manifest.json"

    if not os.path.exists(manifest_file):
        print(f"错误：未找到清单文件: {manifest_file}")
        print("请先生成分组计划（运行 git-batch-commit skill）。")
        sys.exit(1)

    print(f">>> 读取清单: {manifest_file}")
    if args.dry_run:
        print(">>> 模式: 空运行（仅预览，不提交）")
    print()

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    commits = manifest.get("commits", [])
    total = len(commits)

    # 覆盖度预检：确保每个已暂存文件都落到某个分组。
    # 因为每个分组提交前都会 reset 索引，未被任何分组覆盖的文件会被静默取消暂存。
    staged_result = run("git diff --cached --name-only", check=False, capture=True)
    original_staged = set()
    if staged_result.returncode == 0:
        original_staged = {
            line for line in staged_result.stdout.splitlines() if line.strip()
        }

    if original_staged and not args.force:
        patterns = []
        for item in commits:
            patterns.extend(item.get("files", []))

        covered = set()
        for pattern in patterns:
            matched = {f for f in original_staged if fnmatch.fnmatch(f, pattern)}
            if not matched:
                matched = set(glob.glob(pattern, recursive=True))
            covered |= matched

        uncovered = sorted(original_staged - covered)
        if uncovered:
            print("!!! 覆盖度检查失败：以下已暂存文件未出现在任何分组中")
            for name in uncovered:
                print(f"    - {name}")
            print("\n继续执行会清空暂存区（每个分组提交前都会 reset 索引），导致这些改动丢失。")
            print("请修正清单后重试，或加 --force 强制跳过该检查。")
            sys.exit(1)
        print(f">>> 覆盖度检查通过：{len(original_staged)} 个暂存文件全部被分组覆盖")
        print()

    # 保存当前 HEAD 以便回滚
    head_result = run("git rev-parse HEAD", check=False, capture=True)
    if head_result.returncode != 0:
        print("!!! 无法解析 HEAD（分支可能尚无提交，或分支引用丢失）。")
        print(f"    git rev-parse HEAD -> {head_result.stderr.strip()}")
        print("    请先修复仓库引用状态（可用 ORIG_HEAD / .git/logs/HEAD 找回提交），再执行批量提交。")
        sys.exit(1)
    original_head = head_result.stdout.strip()
    print(f">>> 当前 HEAD: {original_head}")

    successful = []

    for idx, item in enumerate(commits, 1):
        msg = item.get("message", "")
        files = item.get("files", [])

        if not msg or not files:
            print(f"警告：第 {idx} 个提交缺少 message 或 files，已跳过")
            continue

        print(f">>> [{idx}/{total}] {msg}")

        # 展开 glob 模式
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
        print(f"    文件模式: {', '.join(files)}")
        print(f"    展开结果: {', '.join(expanded)}")

        if args.dry_run:
            # 空运行：只预览，绝不改动索引。
            # 注意：这里曾经执行真实的 `git reset HEAD --quiet`，会把用户已暂存的改动全部清空。
            file_list = " ".join(f'"{f}"' for f in expanded)
            run(f"git add --dry-run {file_list}", check=True, capture=True)
            print(f"    [空运行] git add {' '.join(expanded)}")
            print(f"    [空运行] git commit -m \"{msg}\"")
            print("    >>> 空运行：该提交将成功执行")
        else:
            # 执行提交
            run("git reset HEAD --quiet", check=True)
            file_list = " ".join(f'"{f}"' for f in expanded)
            run(f"git add {file_list}", check=True)

            staged = run("git diff --cached --name-only", check=True, capture=True).stdout.strip()
            print(f"    已暂存: {staged or '(无)'}")

            result = run(f'git commit -m "{msg}"', check=False, capture=True)

            if result.returncode == 0:
                commit_hash = run("git rev-parse --short HEAD", check=True, capture=True).stdout.strip()
                print(f"    >>> 提交成功 ({commit_hash})")
                successful.append((msg, commit_hash))
            else:
                print(f"    >>> 提交失败: {result.stderr.strip()}")
                run("git reset HEAD --quiet", check=True)

                if args.rollback_on_fail and successful:
                    print(f"\n!!! 已启用回滚模式，重置到: {original_head}")
                    run(f"git reset --hard {original_head}", check=True)
                    print(f"已回滚 {len(successful)} 个提交")
                elif successful:
                    print(f"\n!!! 第 {idx} 个提交失败。已有 {len(successful)} 个提交成功并保留在分支上。")
                    for m, h in successful:
                        print(f"  - {m} ({h})")
                    print("\n如需回滚，请运行: git reset --hard <desired-head>")
                sys.exit(1)

        print()

    if args.dry_run:
        print("=== 空运行完成 ===")
        print("上述为脚本将执行的操作，未创建任何提交。")
        print(f"清单文件保留在: {manifest_file}")
        print("准备就绪后，请运行: python scripts/batch-commit.py")
    else:
        if os.path.exists(manifest_file):
            os.remove(manifest_file)
        print("=== 执行完成 ===")
        print(f"成功: {len(successful)} 个提交")
        if successful:
            print("提交列表:")
            for msg, h in successful:
                print(f"  - {msg} ({h})")
        print("\n清单文件已清理。")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
batch-undo.py - 撤销上一批次提交
Usage:
    python scripts/batch-undo.py                    # 交互式确认
    python scripts/batch-undo.py --all              # 撤销全部，无需逐个确认

Cross-platform: Windows / Linux / macOS
"""
import argparse
import subprocess
import sys


def run(cmd, capture=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return result.stdout.strip() if capture else None


def main():
    parser = argparse.ArgumentParser(description="撤销上一批次提交")
    parser.add_argument("--all", action="store_true", help="撤销全部，无需逐个确认")
    args = parser.parse_args()

    # 检查 .git-batch-manifest.json 是否存在
    import os
    manifest_file = ".git-batch-manifest.json"
    manifest_exists = os.path.exists(manifest_file)

    if manifest_exists:
        print(f">>> 找到清单文件: {manifest_file}")
        print(">>> 上一批次提交记录可用。")
    else:
        print(">>> 未找到清单文件，尝试从最近提交推断。")

    # 获取最近提交
    print("\n=== 最近 10 条提交 ===")
    log = run("git log --oneline -10")
    print(log or "(无提交)")

    print()
    commits = []

    # 尝试从清单读取
    if manifest_exists:
        import json
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            commits = [(m["message"], None) for m in manifest.get("commits", [])]
        except Exception:
            pass

    # 无清单则提示输入数量
    if not commits:
        print(">>> 输入要撤销的提交数量（默认 1）：")
        count_input = input("数量: ").strip()
        try:
            count = int(count_input) if count_input else 1
        except ValueError:
            print("输入无效，使用默认值 1")
            count = 1

        for i in range(count):
            commits.append((f"提交 {i+1}", None))

    # 确认撤销
    if args.all:
        print(f"\n>>> 将撤销 {len(commits)} 个提交（--all 模式）")
    else:
        print(f"\n>>> 将撤销 {len(commits)} 个提交（交互模式）")
        confirm = input("确认撤销？输入 yes 继续: ").strip()
        if confirm != "yes":
            print("撤销已取消。")
            sys.exit(0)

    # 执行撤销
    for i, (msg, _) in enumerate(reversed(commits), 1):
        print(f">>> 撤销 [{i}/{len(commits)}]: {msg}")
        run("git reset --soft HEAD~1")
        print("    >>> 已撤销 1 个提交（软重置）")
        print("    文件已恢复到暂存状态。")

    print("\n=== 撤销完成 ===")
    print(f"已撤销 {len(commits)} 个提交。所有变更已回到暂存区。")
    print("如需完全丢弃变更，请运行: git reset --hard HEAD~N")

    if manifest_exists:
        try:
            os.remove(manifest_file)
            print("清单文件已清理。")
        except Exception:
            pass


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
check-staged.py - 预检暂存区变更并扫描敏感文件
Usage: python scripts/check-staged.py
Cross-platform: Windows / Linux / macOS
"""
import subprocess
import sys
import re


def run(cmd):
    """运行 shell 命令，返回标准输出。"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"  命令执行失败: {cmd} -> {e}")
        return ""


def main():
    print("=== Git 状态 ===")
    status = run("git status --short")
    print(status or "(无变更)")
    print()

    print("=== 暂存区文件 ===")
    staged_files_str = run("git diff --cached --name-only")
    staged_files = [f for f in staged_files_str.split("\n") if f]
    print("\n".join(staged_files) if staged_files else "(无)")
    print()

    print("=== 暂存区差异统计 ===")
    stats = run("git diff --cached --stat")
    print(stats or "(无)")
    print()

    # 敏感文件模式
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

    print("=== 敏感文件扫描 ===")
    found_sensitive = []
    for file in staged_files:
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, file, re.IGNORECASE):
                found_sensitive.append(file)
                break

    if found_sensitive:
        print("警告：发现敏感文件：")
        for f in found_sensitive:
            print(f"  - {f}")
            print("请先手动处理这些文件，然后再继续。")
        sys.exit(1)
    else:
            print("未发现敏感文件。")
    print()

    # 二进制 / 构建产物模式
    BINARY_PATTERNS = [
        r"\.log$",
        r"\.tmp$",
        r"\.temp$",
        r"/dist/",
        r"/build/",
        r"/node_modules/",
        r"\.cache/",
    ]

    print("=== 二进制 / 构建产物扫描 ===")
    found_binary = []
    for file in staged_files:
        for pattern in BINARY_PATTERNS:
            if re.search(pattern, file):
                found_binary.append(file)
                break

    if found_binary:
        print("警告：以下文件可能不应该被提交：")
        for f in found_binary:
            print(f"  - {f}")
    else:
            print("未发现明显的构建产物或日志文件。")
    print()

    # 同时处于暂存与未暂存状态的文件检查
    print("=== 暂存 + 未暂存同文件检查 ===")
    unstaged_files_str = run("git diff --name-only")
    unstaged_files = set(f for f in unstaged_files_str.split("\n") if f)
    staged_set = set(staged_files)

    common = staged_set & unstaged_files
    if common:
        print("警告：以下文件同时处于暂存和未暂存状态：")
        for f in sorted(common):
            print(f"  - {f}")
        print("此工作流可能会影响工作区状态。")
    else:
        print("没有文件同时处于暂存和未暂存状态。")
    print()

    # 分支状态
    print("=== 分支状态 ===")
    branch = run("git rev-parse --abbrev-ref HEAD")
    print(f"当前分支: {branch}")

    # 检查未推送提交 —— 使用 Python 正确处理远程追踪分支
    unpushed = ""
    try:
        # 获取远程追踪分支
        tracking = run("git rev-parse --abbrev-ref %s@{upstream}" % branch)
        if tracking:
            unpushed = run(f"git log {tracking}..{branch} --oneline")
    except Exception:
        pass

    if unpushed:
        print("警告：发现未推送提交：")
        print(unpushed)
    else:
        print("没有未推送提交（或无上游分支）。")
    print()

    print("=== 检查完成 ===")


if __name__ == "__main__":
    main()

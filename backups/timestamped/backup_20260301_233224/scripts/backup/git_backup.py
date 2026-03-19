#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Git 提交并备份脚本
自动提交更改到 Git 并创建备份
"""

import os
import subprocess
import datetime
import sys

def run_command(command, cwd=None):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, str(e)

def git_commit(message):
    """提交到 Git"""
    print("=" * 60)
    print("Git 提交")
    print("=" * 60)
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 添加所有更改
    print("添加文件...")
    code, output = run_command("git add .", cwd=project_root)
    print(output)
    
    # 检查是否有更改
    code, output = run_command("git status --porcelain", cwd=project_root)
    if not output.strip():
        print("没有需要提交的更改")
        return True
    
    # 提交
    print(f"提交：{message}")
    code, output = run_command(f'git commit -m "{message}"', cwd=project_root)
    print(output)
    
    if code != 0:
        print(f"[错误] Git 提交失败")
        return False
    
    print("✓ Git 提交成功")
    return True

def create_backup():
    """创建备份"""
    print("\n" + "=" * 60)
    print("创建备份")
    print("=" * 60)
    
    backup_script = os.path.join(os.path.dirname(__file__), 'auto_backup.py')
    if os.path.exists(backup_script):
        code, output = run_command(f'python "{backup_script}"')
        print(output)
        return code == 0
    else:
        print(f"[警告] 备份脚本不存在：{backup_script}")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Git 提交并备份系统")
    print(f"时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 获取提交信息
    if len(sys.argv) > 1:
        commit_message = ' '.join(sys.argv[1:])
    else:
        commit_message = f"Auto backup: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    try:
        # 1. Git 提交
        if not git_commit(commit_message):
            print("\n[警告] Git 提交失败，继续备份...")
        
        # 2. 创建备份
        create_backup()
        
        print("\n" + "=" * 60)
        print("全部完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[错误] 操作失败：{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

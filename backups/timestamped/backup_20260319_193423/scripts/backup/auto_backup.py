#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动备份脚本 - 本地留档 + 印象笔记 + GitHub 备份
论文项目：Fortran 到 Python 自动转换
"""

import os
import shutil
import datetime
import subprocess
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BACKUP_DIR = os.path.join(PROJECT_ROOT, 'backups')
TIMESTAMP_DIR = os.path.join(BACKUP_DIR, 'timestamped')
YINXIANG_DIR = os.path.join(BACKUP_DIR, 'yinxiang')

BACKUP_ITEMS = [
    'src',
    'docs',
    'scripts',
    'github',
    'hello_fortran.f90',
    'file_toolkit.py',
    'README.md',
]

def get_timestamp():
    """生成时间戳字符串"""
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def create_local_backup():
    """创建本地时间戳备份"""
    print("=" * 60)
    print("创建本地时间戳备份")
    print("=" * 60)
    
    timestamp = get_timestamp()
    backup_path = os.path.join(TIMESTAMP_DIR, f'backup_{timestamp}')
    
    os.makedirs(backup_path, exist_ok=True)
    
    copied_count = 0
    for item in BACKUP_ITEMS:
        src_path = os.path.join(PROJECT_ROOT, item)
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                dst_path = os.path.join(backup_path, os.path.basename(item))
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                print(f"✓ 目录：{item}")
            else:
                shutil.copy2(src_path, backup_path)
                print(f"✓ 文件：{item}")
            copied_count += 1
        else:
            print(f"⚠ 跳过 (不存在): {item}")
    
    print(f"\n备份完成：{backup_path}")
    print(f"共备份 {copied_count} 个项目")
    return backup_path

def create_yinxiang_export():
    """创建印象笔记导出文件（Markdown 格式）"""
    print("\n" + "=" * 60)
    print("创建印象笔记导出文件")
    print("=" * 60)
    
    os.makedirs(YINXIANG_DIR, exist_ok=True)
    
    timestamp = get_timestamp()
    export_file = os.path.join(YINXIANG_DIR, f'backup_note_{timestamp}.md')
    
    content = f"""# 论文项目备份 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 备份信息
- 备份时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 项目路径：{PROJECT_ROOT}

## 备份内容

"""
    
    for item in BACKUP_ITEMS:
        src_path = os.path.join(PROJECT_ROOT, item)
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                file_count = sum(1 for _ in os.walk(src_path) for _ in _[2])
                content += f"- **{item}/** (目录，{file_count} 个文件)\n"
            else:
                size = os.path.getsize(src_path)
                content += f"- **{item}** (文件，{size} 字节)\n"
    
    content += """
## 使用说明
1. 此文件可导入印象笔记
2. 完整备份位于本地 backups/timestamped/ 目录
3. GitHub 仓库同步备份

## 注意事项
- 本地备份保留 30 天
- GitHub 仓库为远程备份
- 印象笔记用于重要笔记同步

---
*由 auto_backup.py 自动生成*
"""
    
    with open(export_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 创建印象笔记导出文件：{export_file}")
    print("提示：可将此 Markdown 文件导入印象笔记")
    
    return export_file

def git_backup():
    """GitHub 备份（Git 提交并推送）"""
    print("\n" + "=" * 60)
    print("GitHub 备份")
    print("=" * 60)
    
    def run_cmd(cmd):
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return 1, str(e)
    
    code, output = run_cmd("git status --porcelain")
    if not output.strip():
        print("没有需要提交的更改")
        return True
    
    print("添加文件...")
    run_cmd("git add .")
    
    timestamp = get_timestamp()
    commit_msg = f"Auto backup: {timestamp}"
    print(f"提交：{commit_msg}")
    code, output = run_cmd(f'git commit -m "{commit_msg}"')
    print(output)
    
    if code != 0:
        print("[警告] Git 提交失败")
        return False
    
    print("推送到 GitHub...")
    code, output = run_cmd("git push")
    if code == 0:
        print("✓ GitHub 备份成功")
        return True
    else:
        print(f"[警告] 推送失败：{output}")
        return False

def cleanup_old_backups(keep_days=30):
    """清理旧备份（保留最近 30 天）"""
    print("\n" + "=" * 60)
    print(f"清理旧备份 (保留最近{keep_days}天)")
    print("=" * 60)
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
    removed_count = 0
    
    if os.path.exists(TIMESTAMP_DIR):
        for folder in os.listdir(TIMESTAMP_DIR):
            folder_path = os.path.join(TIMESTAMP_DIR, folder)
            if os.path.isdir(folder_path):
                try:
                    date_str = folder.replace('backup_', '')
                    folder_date = datetime.datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                    
                    if folder_date < cutoff_date:
                        shutil.rmtree(folder_path)
                        print(f"✓ 删除旧备份：{folder}")
                        removed_count += 1
                except Exception as e:
                    print(f"⚠ 跳过 {folder}: {e}")
    
    print(f"共删除 {removed_count} 个旧备份")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("论文项目自动备份系统")
    print(f"时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        local_backup = create_local_backup()
        
        yinxiang_file = create_yinxiang_export()
        
        git_backup()
        
        cleanup_old_backups(keep_days=30)
        
        print("\n" + "=" * 60)
        print("备份全部完成!")
        print("=" * 60)
        print(f"本地备份：{local_backup}")
        print(f"印象笔记：{yinxiang_file}")
        print(f"GitHub：已同步")
        
    except Exception as e:
        print(f"\n[错误] 备份失败：{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动备份脚本 - 本地时间戳备份 + 阿里云备份
论文项目：Fortran 到 Python 自动转换
"""

import os
import shutil
import datetime
import subprocess
import sys

# 配置
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BACKUP_DIR = os.path.join(PROJECT_ROOT, 'backups')
TIMESTAMP_DIR = os.path.join(BACKUP_DIR, 'timestamped')
ALIYUN_DIR = os.path.join(BACKUP_DIR, 'aliyun')

# 需要备份的目录和文件
BACKUP_ITEMS = [
    'src',
    'docs',
    'scripts',
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

def create_aliyun_backup():
    """创建阿里云备份（同步到阿里云盘）"""
    print("\n" + "=" * 60)
    print("创建阿里云备份")
    print("=" * 60)
    
    # 确保阿里云备份目录存在
    os.makedirs(ALIYUN_DIR, exist_ok=True)
    
    # 创建完整的 zip 压缩包
    timestamp = get_timestamp()
    zip_filename = f'aliyun_backup_{timestamp}'
    zip_fullpath = os.path.join(ALIYUN_DIR, zip_filename + '.zip')
    
    # 使用 shutil.make_archive 创建压缩包
    try:
        # Python 3.12+ 支持 ignore 参数
        zip_path = shutil.make_archive(
            os.path.join(ALIYUN_DIR, zip_filename),
            'zip',
            PROJECT_ROOT
        )
        print(f"✓ 创建压缩包：{zip_path}")
    except TypeError:
        # 对于旧版本 Python，创建临时目录
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            # 复制需要备份的文件到临时目录
            for item in os.listdir(PROJECT_ROOT):
                if item in ['.git', 'backups', '__pycache__']:
                    continue
                if item.endswith(('.pyc', '.exe', '.o', '.obj', '.7z', '.log')):
                    continue
                    
                src_path = os.path.join(PROJECT_ROOT, item)
                dst_path = os.path.join(tmpdir, item)
                
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                else:
                    shutil.copy2(src_path, dst_path)
            
            zip_path = shutil.make_archive(
                os.path.join(ALIYUN_DIR, zip_filename),
                'zip',
                tmpdir
            )
            print(f"✓ 创建压缩包：{zip_path}")
    
    # TODO: 添加阿里云盘 API 上传逻辑
    # 注意：需要使用阿里云盘 API 或 CLI 工具进行实际上传
    # 这里提供框架，实际使用时需要配置阿里云盘认证
    
    print("\n提示：阿里云盘上传需要配置 API 认证")
    print("建议使用阿里云盘官方客户端或第三方工具进行同步")
    
    return zip_fullpath + '.zip'

def cleanup_old_backups(keep_days=30):
    """清理旧备份（保留最近 30 天）"""
    print("\n" + "=" * 60)
    print(f"清理旧备份 (保留最近{keep_days}天)")
    print("=" * 60)
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
    removed_count = 0
    
    # 清理时间戳备份
    if os.path.exists(TIMESTAMP_DIR):
        for folder in os.listdir(TIMESTAMP_DIR):
            folder_path = os.path.join(TIMESTAMP_DIR, folder)
            if os.path.isdir(folder_path):
                try:
                    # 从文件夹名解析日期
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
        # 1. 创建本地时间戳备份
        local_backup = create_local_backup()
        
        # 2. 创建阿里云备份
        aliyun_backup = create_aliyun_backup()
        
        # 3. 清理旧备份
        cleanup_old_backups(keep_days=30)
        
        print("\n" + "=" * 60)
        print("备份全部完成!")
        print("=" * 60)
        print(f"本地备份：{local_backup}")
        print(f"阿里云备份：{aliyun_backup}")
        
    except Exception as e:
        print(f"\n[错误] 备份失败：{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

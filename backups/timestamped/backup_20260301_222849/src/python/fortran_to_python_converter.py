#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fortran 到 Python 自动转换主控脚本
论文项目：使用 AI agent 实现 Fortran 到 Python 自动转换
用于不可约构型、超胞构建、特殊准随机结构搜索、有序结构小集合搜索
"""

import os
import re
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

class FortranToPythonConverter:
    """Fortran 到 Python 转换器类"""
    
    def __init__(self):
        self.fortran_code = ""
        self.python_code = ""
        self.conversion_log = []
        self.current_line_num = 0
        
    def load_fortran_file(self, filepath):
        """加载 Fortran 源代码文件"""
        print(f"加载 Fortran 文件: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            self.fortran_code = f.read()
        print(f"✓ 加载完成，共 {len(self.fortran_code.splitlines())} 行")
        
    def save_python_file(self, filepath):
        """保存 Python 代码到文件"""
        print(f"保存 Python 文件: {filepath}")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.python_code)
        print(f"✓ 保存完成")
        
    def convert_program_structure(self, code_lines):
        """转换程序结构"""
        converted_lines = []
        
        for line_num, line in enumerate(code_lines, 1):
            self.current_line_num = line_num
            
            # 跳过空行
            stripped = line.strip()
            if not stripped:
                converted_lines.append('')
                continue
            
            # 转换注释（将!转换为#）
            if stripped.startswith('!'):
                converted_lines.append(f'    # {stripped[1:]}')
                self.conversion_log.append(f"Line {line_num}: Converted comment")
                continue
                
            # 转换 program 语句
            if re.match(r'^\s*program\s+', line, re.IGNORECASE):
                prog_name = re.search(r'program\s+(\w+)', line, re.IGNORECASE)
                if prog_name:
                    converted_lines.append(f'def main():  # Converted from Fortran program {prog_name.group(1)}')
                    self.conversion_log.append(f"Line {line_num}: Converted 'program {prog_name.group(1)}' to 'def main()'")
                else:
                    converted_lines.append('# Converted program statement')
                    self.conversion_log.append(f"Line {line_num}: Converted program statement")
                continue
                
            # 转换 end program 语句
            if re.match(r'^\s*end\s+program', line, re.IGNORECASE):
                converted_lines.append('    pass')
                converted_lines.append('')
                converted_lines.append('if __name__ == "__main__":')
                converted_lines.append('    main()')
                self.conversion_log.append(f"Line {line_num}: Converted 'end program' to Python main guard")
                continue
                
            # 转换 implicit none
            if re.match(r'^\s*implicit\s+none', line, re.IGNORECASE):
                converted_lines.append('# Converted from "implicit none" - Python handles variables dynamically')
                self.conversion_log.append(f"Line {line_num}: Handled 'implicit none'")
                continue
                
            # 转换变量声明 (integer, real, etc.)
            var_decl_match = re.match(r'^(\s*)(integer|real|double\s+precision|character|logical)\s*(.*)', line, re.IGNORECASE)
            if var_decl_match:
                indent = var_decl_match.group(1)
                var_type = var_decl_match.group(2).lower()
                var_defs = var_decl_match.group(3)
                
                # 提取变量名 (忽略数组声明和 ::)
                if '::' in var_defs:
                    var_defs = var_defs.split('::')[1]
                
                # 简单变量初始化（在 Python 中不需要显式声明）
                var_names = [v.strip() for v in var_defs.replace(',', ', ').replace('&', ',').split(',') if v.strip()]
                
                # 注释掉原声明
                converted_lines.append(f'{indent}# Converted from: {var_type} :: {", ".join(var_names)}')
                
                # 如果是整数类型且有初始化，添加初始化
                if 'integer' in var_type.lower():
                    for var_name in var_names:
                        if '=' in var_name:
                            # 分离变量名和初始值
                            parts = var_name.split('=')
                            if len(parts) == 2:
                                var = parts[0].strip()
                                val = parts[1].strip()
                                converted_lines.append(f'{indent}{var} = {val}  # Integer variable initialized')
                
                self.conversion_log.append(f"Line {line_num}: Converted variable declaration '{var_type}'")
                continue
                
            # 转换 print 语句
            print_match = re.match(r'^(\s*)print\s*\*\s*,\s*(.+)', line, re.IGNORECASE)
            if print_match:
                indent = print_match.group(1)
                content = print_match.group(2).strip()
                
                # 移除外层括号（如果有的话）
                if content.startswith('(') and content.endswith(')'):
                    content = content[1:-1]
                
                # 处理字符串常量
                content = content.strip()
                
                # 转换到 Python print
                converted_lines.append(f'{indent}print({content})')
                self.conversion_log.append(f"Line {line_num}: Converted print statement")
                continue
                
            # 转换 do 循环
            do_match = re.match(r'^(\s*)do\s+(\w+)\s*=\s*(\d+)\s*,\s*(\d+)', line, re.IGNORECASE)
            if do_match:
                indent = do_match.group(1)
                var = do_match.group(2)
                start_val = do_match.group(3)
                end_val = do_match.group(4)
                
                # Python 的 range 是开区间，所以结束值要加1
                converted_lines.append(f'{indent}for {var} in range({start_val}, {int(end_val)+1}):')
                self.conversion_log.append(f"Line {line_num}: Converted do loop to for loop")
                continue
                
            # 转换 end do
            if re.match(r'^\s*end\s+do', line, re.IGNORECASE):
                # Python 不需要 end do，跳过
                self.conversion_log.append(f"Line {line_num}: Removed 'end do' (handled by Python indentation)")
                continue
                
            # 转换赋值语句 (例如: sum = sum + i)
            assignment_match = re.match(r'^(\s*)(\w+)\s*=\s*(.+)', line)
            if assignment_match:
                indent = assignment_match.group(1)
                var = assignment_match.group(2)
                expr = assignment_match.group(3).strip()
                
                converted_lines.append(f'{indent}{var} = {expr}')
                self.conversion_log.append(f"Line {line_num}: Converted assignment statement")
                continue
                
            # 如果没有匹配到任何转换规则，则保持原样但添加注释
            converted_lines.append(f'# Original: {line.strip()}')
            
        return converted_lines
    
    def convert(self, fortran_file=None, python_file=None):
        """执行转换"""
        print("=" * 60)
        print("Fortran 到 Python 转换器")
        print("=" * 60)
        
        if fortran_file:
            self.load_fortran_file(fortran_file)
        
        print(f"开始转换...")
        
        # 分割代码为行
        lines = self.fortran_code.splitlines()
        
        # 转换代码结构
        converted_lines = self.convert_program_structure(lines)
        
        # 组合转换后的代码
        self.python_code = '\n'.join(converted_lines)
        
        # 添加 Python 标准库导入
        header = ('#!/usr/bin/env python\n'
                 '# -*- coding: utf-8 -*-\n'
                 '"""\n'
                 'Converted from Fortran code\n'
                 f'Conversion time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
                 '"""\n\n')
        
        self.python_code = header + self.python_code
        
        print(f"✓ 转换完成")
        
        if python_file:
            self.save_python_file(python_file)
        
        # 输出转换日志
        print(f"\n转换日志 (共 {len(self.conversion_log)} 项):")
        for log_entry in self.conversion_log[-10:]:  # 只显示最后10条
            print(f"  {log_entry}")
        
        if len(self.conversion_log) > 10:
            print(f"  ... 还有 {len(self.conversion_log) - 10} 项")
        
        return self.python_code


def analyze_fortran_code(file_path):
    """分析 Fortran 代码结构"""
    print(f"\n{'='*60}")
    print("Fortran 代码分析")
    print("="*60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    analysis = {
        'total_lines': len(lines),
        'code_lines': 0,
        'comment_lines': 0,
        'program_statements': [],
        'variable_declarations': [],
        'loops': [],
        'functions_subroutines': [],
        'print_statements': []
    }
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        if not stripped:
            continue
        elif stripped.startswith('!'):
            analysis['comment_lines'] += 1
        else:
            analysis['code_lines'] += 1
            
            # 检查程序结构
            if re.match(r'^\s*program\s+', line, re.IGNORECASE):
                match = re.search(r'program\s+(\w+)', line, re.IGNORECASE)
                if match:
                    analysis['program_statements'].append((i, match.group(1)))
            
            # 检查变量声明
            if re.match(r'^\s*(integer|real|double\s+precision|character|logical)\s+', line, re.IGNORECASE):
                analysis['variable_declarations'].append((i, line.strip()))
            
            # 检查循环
            if re.match(r'^\s*do\s+', line, re.IGNORECASE):
                analysis['loops'].append((i, line.strip()))
            
            # 检查函数/子程序
            if re.match(r'^\s*(function|subroutine)\s+', line, re.IGNORECASE):
                match = re.search(r'(function|subroutine)\s+(\w+)', line, re.IGNORECASE)
                if match:
                    analysis['functions_subroutines'].append((i, match.group(1), match.group(2)))
            
            # 检查打印语句
            if re.match(r'^\s*print\s+', line, re.IGNORECASE):
                analysis['print_statements'].append((i, line.strip()))
    
    # 输出分析结果
    print(f"总行数: {analysis['total_lines']}")
    print(f"代码行数: {analysis['code_lines']}")
    print(f"注释行数: {analysis['comment_lines']}")
    print(f"程序声明: {len(analysis['program_statements'])}")
    for stmt in analysis['program_statements']:
        print(f"  - 第{stmt[0]}行: program {stmt[1]}")
    print(f"变量声明: {len(analysis['variable_declarations'])}")
    print(f"循环结构: {len(analysis['loops'])}")
    for loop in analysis['loops']:
        print(f"  - 第{loop[0]}行: {loop[1]}")
    print(f"打印语句: {len(analysis['print_statements'])}")
    for print_stmt in analysis['print_statements']:
        print(f"  - 第{print_stmt[0]}行: {print_stmt[1]}")
    
    return analysis


def main():
    """主函数"""
    print("\n" + "="*60)
    print("Fortran 到 Python 转换主控脚本")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 设置默认路径
    src_dir = Path('src/fortran')
    dst_dir = Path('src/python')
    
    # 查找 Fortran 源文件
    fortran_files = list(src_dir.glob('*.f90')) + list(src_dir.glob('*.f'))
    
    if not fortran_files:
        print(f"[警告] 在 {src_dir} 中未找到 Fortran 文件")
        # 使用项目根目录的 hello_fortran.f90
        root_fortran = Path('hello_fortran.f90')
        if root_fortran.exists():
            fortran_files = [root_fortran]
            print(f"使用根目录的 {root_fortran}")
        else:
            print("[错误] 未找到任何 Fortran 文件")
            sys.exit(1)
    
    print(f"找到 {len(fortran_files)} 个 Fortran 文件:")
    for f in fortran_files:
        print(f"  - {f}")
    
    # 对每个 Fortran 文件进行处理
    for fortran_file in fortran_files:
        print(f"\n处理文件: {fortran_file}")
        
        # 分析代码
        analysis = analyze_fortran_code(fortran_file)
        
        # 执行转换
        converter = FortranToPythonConverter()
        
        # 生成输出文件路径
        output_file = dst_dir / f"{fortran_file.stem}_converted.py"
        
        # 执行转换
        converter.convert(str(fortran_file), str(output_file))
        
        print(f"\n✓ 转换完成: {output_file}")
        
        # 显示转换后的代码预览（前20行）
        print(f"\n转换后代码预览 ({output_file}):")
        print("-" * 40)
        with open(output_file, 'r', encoding='utf-8') as f:
            preview_lines = f.readlines()[:20]
            for i, line in enumerate(preview_lines, 1):
                print(f"{i:3d}: {line.rstrip()}")
            if len(preview_lines) == 20:
                print("...")
        print("-" * 40)
    
    print(f"\n{'='*60}")
    print("转换任务完成!")
    print("="*60)
    print("输出文件位置:")
    for fortran_file in fortran_files:
        output_file = dst_dir / f"{fortran_file.stem}_converted.py"
        print(f"  - {output_file}")
    
    # 运行备份
    print(f"\n运行自动备份...")
    backup_script = Path('scripts/backup/auto_backup.py')
    if backup_script.exists():
        try:
            subprocess.run(['python', str(backup_script)], check=True)
            print("✓ 备份完成")
        except subprocess.CalledProcessError:
            print("[警告] 备份脚本执行失败")
    else:
        print(f"[警告] 备份脚本不存在: {backup_script}")


if __name__ == '__main__':
    main()

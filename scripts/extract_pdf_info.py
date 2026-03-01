#!/usr/bin/env python
"""
PDF 文献信息提取脚本
用于从 PDF 文件中提取文本内容，便于后续分析
"""

import os
from pypdf import PdfReader

def extract_pdf_info(pdf_path, output_path=None):
    """提取 PDF 文件的关键信息"""
    
    print(f"\n{'='*80}")
    print(f"正在处理：{os.path.basename(pdf_path)}")
    print(f"{'='*80}\n")
    
    try:
        reader = PdfReader(pdf_path)
        print(f"总页数：{len(reader.pages)}\n")
        
        # 提取元数据
        metadata = reader.metadata
        print("元数据信息:")
        print(f"  标题：{metadata.get('/Title', 'N/A')}")
        print(f"  作者：{metadata.get('/Author', 'N/A')}")
        print(f"  主题：{metadata.get('/Subject', 'N/A')}")
        print(f"  关键词：{metadata.get('/Keywords', 'N/A')}")
        print(f"  创建者：{metadata.get('/Creator', 'N/A')}")
        print(f"  生产者：{metadata.get('/Producer', 'N/A')}")
        print(f"  创建日期：{metadata.get('/CreationDate', 'N/A')}")
        print()
        
        # 提取前几页的内容（通常是摘要和引言）
        text_content = []
        max_pages_to_extract = min(5, len(reader.pages))  # 提取前 5 页
        
        print(f"提取前 {max_pages_to_extract} 页内容...\n")
        
        for i in range(max_pages_to_extract):
            page = reader.pages[i]
            text = page.extract_text()
            if text:
                text_content.append(f"\n--- 第 {i+1} 页 ---\n{text}")
                print(f"第 {i+1} 页提取完成")
        
        # 保存提取的内容
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"PDF 文件：{os.path.basename(pdf_path)}\n")
                f.write(f"总页数：{len(reader.pages)}\n")
                f.write(f"{'='*80}\n\n")
                
                for content in text_content:
                    f.write(content)
                    f.write("\n\n")
            
            print(f"\n提取内容已保存到：{output_path}")
        
        return '\n'.join(text_content)
    
    except Exception as e:
        print(f"错误：{e}")
        return None

def main():
    """主函数：处理所有 PDF 文献"""
    
    pdf_dir = r"d:\Trae CN\论文\文献"
    output_dir = r"d:\Trae CN\论文\docs\literature_notes"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # PDF 文件列表
    pdf_files = [
        "1990-Special Quasirandom Structures.pdf",
        "2016-Efficient Ab initio Modeling of Random Multicomponent Alloys.pdf",
        "2020-disorder-Algorithm for generating irreducible site-occupancy configurations.pdf"
    ]
    
    results = {}
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        output_file = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}_extracted.txt")
        
        if os.path.exists(pdf_path):
            content = extract_pdf_info(pdf_path, output_file)
            results[pdf_file] = content
        else:
            print(f"文件不存在：{pdf_path}")
    
    print(f"\n{'='*80}")
    print("所有 PDF 文献提取完成！")
    print(f"输出目录：{output_dir}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()

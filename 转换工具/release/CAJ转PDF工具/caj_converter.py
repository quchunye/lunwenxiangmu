# -*- coding: utf-8 -*-
"""
CAJ文件转换工具 v3.2
直接使用本地cajparser.py转换，无需mutool
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional, List
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "data", "config.json")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "data", "conversion_history.json")

PYMUPDF_PRO_KEY = "iX1faENEIU1jG9jGNrEKPQVJ"

class CAJConverter:
    """CAJ文件转换器核心类"""
    
    def __init__(self):
        self.config = self.load_config()
        self.history = self.load_history()
        
    def load_config(self) -> dict:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "output_dir": "",
            "auto_open": True,
            "keep_original": True
        }
    
    def save_config(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def load_history(self) -> List[dict]:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_history(self, source: str, target: str, success: bool, error: str = ""):
        from datetime import datetime
        record = {
            "source": source,
            "target": target,
            "success": success,
            "error": error,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.insert(0, record)
        if len(self.history) > 50:
            self.history = self.history[:50]
        self.save_history()
    
    def check_pymupdf(self) -> tuple:
        try:
            import fitz
            return True, f"PyMuPDF {fitz.__version__} 已安装"
        except ImportError:
            return False, "PyMuPDF 未安装"
    
    def check_pypdf2(self) -> tuple:
        try:
            import PyPDF2
            return True, "PyPDF2 已安装"
        except ImportError:
            return False, "PyPDF2 未安装"
    
    def check_imagesize(self) -> tuple:
        try:
            import imagesize
            return True, "imagesize 已安装"
        except ImportError:
            return False, "imagesize 未安装"
    
    def check_dependencies(self) -> dict:
        results = {
            "pymupdf": self.check_pymupdf(),
            "pypdf2": self.check_pypdf2(),
            "imagesize": self.check_imagesize()
        }
        return results
    
    def show_info(self, input_path: str) -> tuple:
        """显示CAJ文件信息"""
        try:
            os.environ["PYMUPDF_PRO_KEY"] = PYMUPDF_PRO_KEY
            script_dir = os.path.dirname(__file__)
            core_dir = os.path.join(script_dir, "core")
            sys.path.insert(0, core_dir)
            
            from cajparser import CAJParser
            caj = CAJParser(input_path)
            
            if caj.format == "PDF" or caj.format == "KDH":
                info = f"File: {input_path}\nType: {caj.format}\n"
            else:
                info = f"File: {input_path}\nType: {caj.format}\nPage count: {caj.page_num}\nOutlines count: {caj.toc_num}\n"
            return True, info
        except SystemExit as e:
            return False, str(e)
        except Exception as e:
            return False, f"读取失败: {str(e)}"
    
    def convert(self, input_path: str, output_path: Optional[str] = None) -> tuple:
        """转换CAJ文件为PDF"""
        if not os.path.exists(input_path):
            return False, "输入文件不存在", None
        
        if not input_path.lower().endswith('.caj'):
            return False, "输入文件不是CAJ格式", None
        
        if output_path is None:
            output_path = input_path.rsplit('.', 1)[0] + '.pdf'
        
        try:
            os.environ["PYMUPDF_PRO_KEY"] = PYMUPDF_PRO_KEY
            
            script_dir = os.path.dirname(__file__)
            core_dir = os.path.join(script_dir, "core")
            original_cwd = os.getcwd()
            os.chdir(core_dir)
            sys.path.insert(0, core_dir)
            
            from cajparser import CAJParser
            caj = CAJParser(input_path)
            caj.convert(output_path)
            
            os.chdir(original_cwd)
            
            if os.path.exists(output_path):
                self.add_history(input_path, output_path, True)
                return True, "转换成功", output_path
            else:
                self.add_history(input_path, output_path, False, "输出文件未生成")
                return False, "转换失败: 输出文件未生成", None
                
        except SystemExit as e:
            error_msg = str(e)
            if "Unknown file type" in error_msg:
                error_msg = "不支持的文件类型 - 该CAJ文件格式暂不支持转换"
            self.add_history(input_path, output_path, False, error_msg)
            return False, error_msg, None
        except Exception as e:
            error_msg = f"转换出错: {str(e)}"
            self.add_history(input_path, output_path, False, error_msg)
            return False, error_msg, None


class ConverterGUI:
    """图形界面"""
    
    def __init__(self):
        self.converter = CAJConverter()
        self.root = tk.Tk()
        self.root.title("CAJ转PDF转换工具 v3.2")
        self.root.geometry("850x600")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.check_deps()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        input_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="CAJ文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path_var = tk.StringVar(
            value=r"D:\download\_AI嵌入对平台供应链信息传导效率的影响研究——基于网络结构中介与SEM-fsQCA的混合方法.caj"
        )
        ttk.Entry(input_frame, textvariable=self.input_path_var, width=70).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(input_frame, text="浏览...", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(input_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar(value=self.converter.config.get("output_dir", ""))
        ttk.Entry(input_frame, textvariable=self.output_dir_var, width=70).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(input_frame, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2, padx=5, pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        options_frame = ttk.LabelFrame(main_frame, text="选项", padding="10")
        options_frame.pack(fill=tk.X, pady=5)
        
        self.auto_open_var = tk.BooleanVar(value=self.converter.config.get("auto_open", True))
        ttk.Checkbutton(options_frame, text="转换完成后自动打开PDF", variable=self.auto_open_var).pack(anchor=tk.W)
        
        self.keep_original_var = tk.BooleanVar(value=self.converter.config.get("keep_original", True))
        ttk.Checkbutton(options_frame, text="保留原始CAJ文件", variable=self.keep_original_var).pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.convert_btn = ttk.Button(btn_frame, text="开始转换", command=self.start_convert, width=12)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="查看文件信息", command=self.show_file_info, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存配置", command=self.save_config, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="帮助", command=self.show_help, width=8).pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(btn_frame, variable=self.progress_var, maximum=100, length=200)
        self.progress.pack(side=tk.LEFT, padx=10)
        
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(btn_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        log_frame = ttk.Frame(notebook, padding="5")
        notebook.add(log_frame, text="日志")
        
        self.log_text = tk.Text(log_frame, height=12, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_frame = ttk.Frame(notebook, padding="5")
        notebook.add(history_frame, text="转换历史")
        
        columns = ("time", "source", "target", "status")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        self.history_tree.heading("time", text="时间")
        self.history_tree.heading("source", text="源文件")
        self.history_tree.heading("target", text="目标文件")
        self.history_tree.heading("status", text="状态")
        
        self.history_tree.column("time", width=150)
        self.history_tree.column("source", width=300)
        self.history_tree.column("target", width=300)
        self.history_tree.column("status", width=80)
        
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_history_to_tree()
        
    def log(self, message: str):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="选择CAJ文件",
            filetypes=[("CAJ文件", "*.caj"), ("所有文件", "*.*")]
        )
        if file_path:
            self.input_path_var.set(file_path)
            
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir_var.set(dir_path)
            
    def check_deps(self):
        results = self.converter.check_dependencies()
        
        pymupdf_ok, pymupdf_msg = results["pymupdf"]
        self.log(f"{'✓' if pymupdf_ok else '✗'} {pymupdf_msg}")
        
        pypdf2_ok, pypdf2_msg = results["pypdf2"]
        self.log(f"{'✓' if pypdf2_ok else '✗'} {pypdf2_msg}")
        
        imagesize_ok, imagesize_msg = results["imagesize"]
        self.log(f"{'✓' if imagesize_ok else '✗'} {imagesize_msg}")
        
        if pymupdf_ok and pypdf2_ok and imagesize_ok:
            self.log("\n✓ 所有依赖已就绪，可以开始转换！")
        else:
            self.log("\n⚠ 部分依赖缺失，请安装")
        
    def save_config(self):
        self.converter.config["output_dir"] = self.output_dir_var.get()
        self.converter.config["auto_open"] = self.auto_open_var.get()
        self.converter.config["keep_original"] = self.keep_original_var.get()
        self.converter.save_config()
        self.log("配置已保存")
    
    def show_help(self):
        help_text = """CAJ转PDF转换工具 v3.2

【使用步骤】
1. 选择CAJ文件
2. (可选) 设置输出目录
3. 点击"开始转换"

【支持的格式】
- CAJ格式：完全支持
- HN格式：部分支持
- KDH格式：支持

【注意事项】
- 如果显示"Unknown file type"，
  说明该文件格式暂不支持
- 大文件转换可能需要较长时间
"""
        messagebox.showinfo("使用帮助", help_text)
    
    def show_file_info(self):
        input_path = self.input_path_var.get()
        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("错误", "请选择有效的CAJ文件")
            return
        
        self.status_var.set("正在读取文件信息...")
        self.log(f"读取文件信息: {input_path}")
        
        success, info = self.converter.show_info(input_path)
        if success:
            self.log(f"文件信息:\n{info}")
            messagebox.showinfo("文件信息", info)
        else:
            self.log(f"读取失败: {info}")
            messagebox.showerror("错误", f"读取失败: {info}")
        
        self.status_var.set("就绪")
        
    def start_convert(self):
        input_path = self.input_path_var.get()
        output_dir = self.output_dir_var.get()
        
        if not input_path:
            messagebox.showerror("错误", "请选择CAJ文件")
            return
            
        if not os.path.exists(input_path):
            messagebox.showerror("错误", "输入文件不存在")
            return
            
        self.convert_btn.config(state=tk.DISABLED)
        self.status_var.set("正在转换...")
        self.progress_var.set(0)
        self.log(f"开始转换: {input_path}")
        
        def do_convert():
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                filename = os.path.basename(input_path).rsplit('.', 1)[0] + '.pdf'
                output_path = os.path.join(output_dir, filename)
            else:
                output_path = None
                
            success, msg, out_path = self.converter.convert(input_path, output_path)
            self.root.after(0, lambda: self.convert_complete(success, msg, out_path))
            
        self.progress_var.set(30)
        threading.Thread(target=do_convert, daemon=True).start()
        
    def convert_complete(self, success: bool, msg: str, output_path: str):
        self.progress_var.set(100)
        self.log(msg)
        self.status_var.set("转换完成" if success else "转换失败")
        self.convert_btn.config(state=tk.NORMAL)
        
        self.load_history_to_tree()
        
        if success:
            if self.auto_open_var.get() and output_path:
                self.log(f"正在打开: {output_path}")
                os.startfile(output_path)
            messagebox.showinfo("成功", f"转换成功!\n输出文件: {output_path}")
        else:
            messagebox.showerror("失败", msg)
            
    def load_history_to_tree(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        for record in self.converter.history:
            status = "成功" if record.get("success") else "失败"
            self.history_tree.insert("", tk.END, values=(
                record.get("time", ""),
                record.get("source", ""),
                record.get("target", ""),
                status
            ))
            
    def run(self):
        self.root.mainloop()


def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        converter = CAJConverter()
        
        print(f"正在转换: {input_file}")
        success, msg, output = converter.convert(input_file)
        print(msg)
        
        if success and output:
            print(f"输出文件: {output}")
    else:
        app = ConverterGUI()
        app.run()


if __name__ == "__main__":
    main()

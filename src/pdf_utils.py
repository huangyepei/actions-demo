"""
PDF操作工具类
提供PDF文件的删除页面、插入页面、合并文件等功能
"""

from PyPDF2 import PdfReader, PdfWriter
from typing import Union, List
import os


class PDFUtils:
    """PDF操作工具类"""
    
    def __init__(self):
        self.reader = None
        self.writer = PdfWriter()
    
    def load_pdf(self, file_path: str) -> None:
        """
        加载PDF文件
        
        Args:
            file_path: PDF文件路径
        
        Raises:
            FileNotFoundError: 文件不存在
            Exception: 文件读取失败
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        try:
            self.reader = PdfReader(file_path)
        except Exception as e:
            raise Exception(f"PDF文件读取失败: {e}")
    
    def delete_pages(self, file_path: str, pages_to_delete: Union[int, List[int]], 
                    output_path: str) -> None:
        """
        删除指定页码的页面
        
        Args:
            file_path: 输入PDF文件路径
            pages_to_delete: 要删除的页码（从0开始）或页码列表
            output_path: 输出文件路径
        
        Raises:
            ValueError: 页码超出范围
        """
        self.load_pdf(file_path)
        
        # 统一处理页码参数
        if isinstance(pages_to_delete, int):
            pages_to_delete = [pages_to_delete]
        
        # 验证页码范围
        total_pages = len(self.reader.pages)
        for page_num in pages_to_delete:
            if page_num < 0 or page_num >= total_pages:
                raise ValueError(f"页码 {page_num} 超出范围 (0-{total_pages-1})")
        
        # 创建新的PDF写入器
        writer = PdfWriter()
        
        # 复制除了要删除的页面之外的所有页面
        for page_num in range(total_pages):
            if page_num not in pages_to_delete:
                writer.add_page(self.reader.pages[page_num])
        
        # 保存结果
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
    
    def insert_pages(self, target_file: str, insert_file: str, 
                    insert_position: int, output_path: str) -> None:
        """
        在指定位置插入页面
        
        Args:
            target_file: 目标PDF文件路径
            insert_file: 要插入的PDF文件路径
            insert_position: 插入位置（从0开始）
            output_path: 输出文件路径
        
        Raises:
            ValueError: 插入位置超出范围
        """
        # 加载目标文件
        self.load_pdf(target_file)
        target_reader = self.reader
        
        # 加载要插入的文件
        insert_reader = PdfReader(insert_file)
        
        # 验证插入位置
        total_pages = len(target_reader.pages)
        if insert_position < 0 or insert_position > total_pages:
            raise ValueError(f"插入位置 {insert_position} 超出范围 (0-{total_pages})")
        
        # 创建新的PDF写入器
        writer = PdfWriter()
        
        # 插入前的页面
        for i in range(insert_position):
            writer.add_page(target_reader.pages[i])
        
        # 插入新页面
        for page in insert_reader.pages:
            writer.add_page(page)
        
        # 插入后的页面
        for i in range(insert_position, total_pages):
            writer.add_page(target_reader.pages[i])
        
        # 保存结果
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
    
    def merge_pdfs(self, file1: str, file2: str, output_path: str) -> None:
        """
        合并两个PDF文件
        
        Args:
            file1: 第一个PDF文件路径
            file2: 第二个PDF文件路径
            output_path: 输出文件路径
        """
        # 创建PDF写入器
        writer = PdfWriter()
        
        # 添加第一个文件的所有页面
        reader1 = PdfReader(file1)
        for page in reader1.pages:
            writer.add_page(page)
        
        # 添加第二个文件的所有页面
        reader2 = PdfReader(file2)
        for page in reader2.pages:
            writer.add_page(page)
        
        # 保存合并结果
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
    
    def get_page_count(self, file_path: str) -> int:
        """
        获取PDF文件的页数
        
        Args:
            file_path: PDF文件路径
        
        Returns:
            页数
        """
        self.load_pdf(file_path)
        return len(self.reader.pages)
"""
PDFUtils类的单元测试
"""

import pytest
import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pdf_utils import PDFUtils


class TestPDFUtils:
    """PDFUtils测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.pdf_utils = PDFUtils()
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试用的PDF文件
        self.create_test_pdfs()
    
    def teardown_method(self):
        """测试后清理"""
        # 清理临时文件
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_test_pdfs(self):
        """创建测试用的PDF文件"""
        # 创建第一个测试PDF（3页）
        writer1 = PdfWriter()
        for i in range(3):
            writer1.add_blank_page(width=200, height=200)
        
        self.test_pdf1 = os.path.join(self.temp_dir, "test1.pdf")
        with open(self.test_pdf1, 'wb') as f:
            writer1.write(f)
        
        # 创建第二个测试PDF（2页）
        writer2 = PdfWriter()
        for i in range(2):
            writer2.add_blank_page(width=200, height=200)
        
        self.test_pdf2 = os.path.join(self.temp_dir, "test2.pdf")
        with open(self.test_pdf2, 'wb') as f:
            writer2.write(f)
        
        # 创建插入用的PDF（1页）
        writer3 = PdfWriter()
        writer3.add_blank_page(width=200, height=200)
        
        self.insert_pdf = os.path.join(self.temp_dir, "insert.pdf")
        with open(self.insert_pdf, 'wb') as f:
            writer3.write(f)
    
    def test_load_pdf_success(self):
        """测试成功加载PDF文件"""
        self.pdf_utils.load_pdf(self.test_pdf1)
        assert self.pdf_utils.reader is not None
        assert len(self.pdf_utils.reader.pages) == 3
    
    def test_load_pdf_file_not_found(self):
        """测试加载不存在的文件"""
        with pytest.raises(FileNotFoundError):
            self.pdf_utils.load_pdf("nonexistent.pdf")
    
    def test_load_pdf_invalid_file(self):
        """测试加载无效文件"""
        # 创建一个无效的PDF文件
        invalid_pdf = os.path.join(self.temp_dir, "invalid.pdf")
        with open(invalid_pdf, 'w') as f:
            f.write("This is not a PDF file")
        
        with pytest.raises(Exception):
            self.pdf_utils.load_pdf(invalid_pdf)
    
    def test_delete_single_page(self):
        """测试删除单页"""
        output_path = os.path.join(self.temp_dir, "delete_single.pdf")
        
        # 删除第1页（索引为1）
        self.pdf_utils.delete_pages(self.test_pdf1, 1, output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 2  # 原3页，删除1页后剩2页
    
    def test_delete_multiple_pages(self):
        """测试删除多页"""
        output_path = os.path.join(self.temp_dir, "delete_multiple.pdf")
        
        # 删除第0页和第2页
        self.pdf_utils.delete_pages(self.test_pdf1, [0, 2], output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 1  # 原3页，删除2页后剩1页
    
    def test_delete_page_out_of_range(self):
        """测试删除超出范围的页码"""
        output_path = os.path.join(self.temp_dir, "delete_out_of_range.pdf")
        
        with pytest.raises(ValueError):
            self.pdf_utils.delete_pages(self.test_pdf1, 5, output_path)
    
    def test_delete_negative_page(self):
        """测试删除负数页码"""
        output_path = os.path.join(self.temp_dir, "delete_negative.pdf")
        
        with pytest.raises(ValueError):
            self.pdf_utils.delete_pages(self.test_pdf1, -1, output_path)
    
    def test_insert_page_at_beginning(self):
        """测试在开头插入页面"""
        output_path = os.path.join(self.temp_dir, "insert_beginning.pdf")
        
        # 在第0个位置插入
        self.pdf_utils.insert_pages(self.test_pdf1, self.insert_pdf, 0, output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 4  # 原3页 + 插入1页 = 4页
    
    def test_insert_page_at_middle(self):
        """测试在中间插入页面"""
        output_path = os.path.join(self.temp_dir, "insert_middle.pdf")
        
        # 在第1个位置插入
        self.pdf_utils.insert_pages(self.test_pdf1, self.insert_pdf, 1, output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 4  # 原3页 + 插入1页 = 4页
    
    def test_insert_page_at_end(self):
        """测试在末尾插入页面"""
        output_path = os.path.join(self.temp_dir, "insert_end.pdf")
        
        # 在第3个位置插入（末尾）
        self.pdf_utils.insert_pages(self.test_pdf1, self.insert_pdf, 3, output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 4  # 原3页 + 插入1页 = 4页
    
    def test_insert_position_out_of_range(self):
        """测试插入位置超出范围"""
        output_path = os.path.join(self.temp_dir, "insert_out_of_range.pdf")
        
        with pytest.raises(ValueError):
            self.pdf_utils.insert_pages(self.test_pdf1, self.insert_pdf, 5, output_path)
    
    def test_insert_negative_position(self):
        """测试插入负数位置"""
        output_path = os.path.join(self.temp_dir, "insert_negative.pdf")
        
        with pytest.raises(ValueError):
            self.pdf_utils.insert_pages(self.test_pdf1, self.insert_pdf, -1, output_path)
    
    def test_merge_pdfs(self):
        """测试合并两个PDF文件"""
        output_path = os.path.join(self.temp_dir, "merged.pdf")
        
        self.pdf_utils.merge_pdfs(self.test_pdf1, self.test_pdf2, output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 5  # 3页 + 2页 = 5页
    
    def test_merge_pdfs_with_nonexistent_file(self):
        """测试合并不存在的文件"""
        output_path = os.path.join(self.temp_dir, "merge_nonexistent.pdf")
        
        with pytest.raises(Exception):
            self.pdf_utils.merge_pdfs("nonexistent1.pdf", "nonexistent2.pdf", output_path)
    
    def test_get_page_count(self):
        """测试获取页数"""
        page_count = self.pdf_utils.get_page_count(self.test_pdf1)
        assert page_count == 3
        
        page_count = self.pdf_utils.get_page_count(self.test_pdf2)
        assert page_count == 2
        
        page_count = self.pdf_utils.get_page_count(self.insert_pdf)
        assert page_count == 1
    
    def test_delete_all_pages(self):
        """测试删除所有页面（边界情况）"""
        output_path = os.path.join(self.temp_dir, "delete_all.pdf")
        
        # 删除所有页面
        self.pdf_utils.delete_pages(self.test_pdf1, [0, 1, 2], output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 0  # 所有页面都被删除
    
    def test_insert_multiple_pages(self):
        """测试插入多页PDF"""
        output_path = os.path.join(self.temp_dir, "insert_multiple.pdf")
        
        # 插入一个2页的PDF
        self.pdf_utils.insert_pages(self.test_pdf1, self.test_pdf2, 1, output_path)
        
        # 验证结果
        reader = PdfReader(output_path)
        assert len(reader.pages) == 5  # 原3页 + 插入2页 = 5页


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
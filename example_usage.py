"""
PDFUtils使用示例
"""

from pdf_utils import PDFUtils
import os


def main():
    """主函数 - 演示PDFUtils的各种用法"""
    pdf_utils = PDFUtils()
    
    # 创建示例PDF文件
    create_sample_pdfs()
    
    print("=== PDF操作工具类使用示例 ===\n")
    
    # 示例1：删除页面
    print("1. 删除页面示例")
    try:
        pdf_utils.delete_pages("sample1.pdf", [0], "result_delete.pdf")
        page_count = pdf_utils.get_page_count("result_delete.pdf")
        print(f"   ✓ 删除第1页成功，结果文件页数: {page_count}")
    except Exception as e:
        print(f"   ✗ 删除页面失败: {e}")
    
    # 示例2：插入页面
    print("\n2. 插入页面示例")
    try:
        pdf_utils.insert_pages("sample1.pdf", "sample2.pdf", 1, "result_insert.pdf")
        page_count = pdf_utils.get_page_count("result_insert.pdf")
        print(f"   ✓ 在第2个位置插入页面成功，结果文件页数: {page_count}")
    except Exception as e:
        print(f"   ✗ 插入页面失败: {e}")
    
    # 示例3：合并PDF文件
    print("\n3. 合并PDF文件示例")
    try:
        pdf_utils.merge_pdfs("sample1.pdf", "sample2.pdf", "result_merge.pdf")
        page_count = pdf_utils.get_page_count("result_merge.pdf")
        print(f"   ✓ 合并PDF文件成功，结果文件页数: {page_count}")
    except Exception as e:
        print(f"   ✗ 合并PDF文件失败: {e}")
    
    # 示例4：获取页数
    print("\n4. 获取页数示例")
    try:
        page_count = pdf_utils.get_page_count("sample1.pdf")
        print(f"   ✓ sample1.pdf 页数: {page_count}")
        
        page_count = pdf_utils.get_page_count("sample2.pdf")
        print(f"   ✓ sample2.pdf 页数: {page_count}")
    except Exception as e:
        print(f"   ✗ 获取页数失败: {e}")
    
    print("\n=== 示例执行完成 ===")
    
    # 清理临时文件
    cleanup_files()


def create_sample_pdfs():
    """创建示例PDF文件"""
    from PyPDF2 import PdfWriter
    
    # 创建第一个示例PDF（3页）
    writer1 = PdfWriter()
    for i in range(3):
        writer1.add_blank_page(width=595, height=842)  # A4尺寸
    
    with open("sample1.pdf", 'wb') as f:
        writer1.write(f)
    
    # 创建第二个示例PDF（2页）
    writer2 = PdfWriter()
    for i in range(2):
        writer2.add_blank_page(width=595, height=842)  # A4尺寸
    
    with open("sample2.pdf", 'wb') as f:
        writer2.write(f)


def cleanup_files():
    """清理临时文件"""
    files_to_cleanup = ["sample1.pdf", "sample2.pdf", 
                       "result_delete.pdf", "result_insert.pdf", "result_merge.pdf"]
    
    for file in files_to_cleanup:
        if os.path.exists(file):
            os.remove(file)
            print(f"   ✓ 清理文件: {file}")


if __name__ == "__main__":
    main()
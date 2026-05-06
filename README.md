# PDF操作工具类

一个Python工具类，提供PDF文件的删除页面、插入页面、合并文件等功能。

## 功能特性

- ✅ 删除指定一页或多页
- ✅ 在指定位置插入一页或多页
- ✅ 合并两个PDF文件
- ✅ 获取PDF文件页数
- ✅ 完整的单元测试覆盖
- ✅ 错误处理和边界情况处理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 依赖包

- PyPDF2==3.0.1 - PDF文件操作库
- pytest==7.4.0 - 单元测试框架
- pytest-cov==4.1.0 - 测试覆盖率工具

## 使用方法

### 基本使用

```python
from pdf_utils import PDFUtils

# 创建工具实例
pdf_utils = PDFUtils()

# 删除页面
pdf_utils.delete_pages("input.pdf", [0, 2], "output_delete.pdf")

# 插入页面
pdf_utils.insert_pages("target.pdf", "insert.pdf", 1, "output_insert.pdf")

# 合并PDF文件
pdf_utils.merge_pdfs("file1.pdf", "file2.pdf", "output_merge.pdf")

# 获取页数
page_count = pdf_utils.get_page_count("input.pdf")
```

### 运行示例

```bash
python example_usage.py
```

### 运行测试

```bash
# 运行所有测试
pytest test_pdf_utils.py -v

# 运行测试并显示覆盖率
pytest test_pdf_utils.py --cov=pdf_utils
```

## 类方法说明

### PDFUtils类

- `delete_pages(file_path, pages_to_delete, output_path)` - 删除指定页码
- `insert_pages(target_file, insert_file, insert_position, output_path)` - 插入页面
- `merge_pdfs(file1, file2, output_path)` - 合并PDF文件
- `get_page_count(file_path)` - 获取PDF页数
- `load_pdf(file_path)` - 加载PDF文件（内部使用）

## 注意事项

- 页码从0开始计数
- 插入位置可以是0到总页数之间的任何位置
- 支持删除和插入多个页面
- 包含完整的错误处理和边界情况检查
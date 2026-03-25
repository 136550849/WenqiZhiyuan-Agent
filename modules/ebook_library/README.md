# 📚 Calibre 电子书库管理模块

**版本**: v1.0  
**创建日期**: 2026-03-25  
**状态**: 🟡 开发中  

---

## 🎯 模块概述

本模块用于管理 Calibre 电子书库，提供书籍扫描、元数据提取、质量评估、分类整理等功能。

### 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 书籍扫描 | ⏳ 待开发 | 扫描 Calibre 书库 |
| 元数据提取 | ⏳ 待开发 | 提取书名/作者/简介等 |
| 质量评估 | ⏳ 待开发 | A/B/C/D 级评估 |
| 格式转换 | ⏳ 待开发 | azw3/epub/pdf 互转 |
| 重复检测 | ⏳ 待开发 | 基于书名/作者/ISBN |
| 分类整理 | ⏳ 待开发 | 按领域/难度/优先级 |

---

## 📂 目录结构

```
modules/ebook_library/
├── __init__.py              # 模块初始化
├── scanner.py               # 书籍扫描器
├── metadata.py              # 元数据提取
├── quality.py               # 质量评估
├── dedup.py                 # 重复检测
├── organizer.py             # 分类整理
├── config.py                # 配置文件
└── README.md                # 使用说明
```

---

## 🔧 技术实现

### 1. 书籍扫描器 (scanner.py)

```python
"""
Calibre 电子书库扫描器
扫描书库，提取书籍文件列表
"""

import os
from pathlib import Path
from typing import List, Dict

class CalibreScanner:
    def __init__(self, library_path: str):
        """
        初始化扫描器
        
        Args:
            library_path: Calibre 书库路径
        """
        self.library_path = Path(library_path)
        self.supported_formats = ['.azw3', '.epub', '.pdf', '.mobi', '.txt']
    
    def scan(self) -> List[Dict]:
        """
        扫描书库
        
        Returns:
            书籍文件列表
        """
        books = []
        
        for root, dirs, files in os.walk(self.library_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.supported_formats:
                    book_info = {
                        'path': str(file_path),
                        'filename': file_path.name,
                        'size': file_path.stat().st_size,
                        'format': file_path.suffix.lower(),
                        'modified': file_path.stat().st_mtime
                    }
                    books.append(book_info)
        
        return books
    
    def get_statistics(self, books: List[Dict]) -> Dict:
        """
        获取统计信息
        
        Args:
            books: 书籍列表
        
        Returns:
            统计信息
        """
        stats = {
            'total_books': len(books),
            'total_size': sum(b['size'] for b in books),
            'by_format': {}
        }
        
        # 按格式统计
        for book in books:
            fmt = book['format']
            if fmt not in stats['by_format']:
                stats['by_format'][fmt] = {'count': 0, 'size': 0}
            stats['by_format'][fmt]['count'] += 1
            stats['by_format'][fmt]['size'] += book['size']
        
        return stats


# 使用示例
if __name__ == '__main__':
    scanner = CalibreScanner('E:/Calibre 书库')
    books = scanner.scan()
    stats = scanner.get_statistics(books)
    
    print(f"总书籍数：{stats['total_books']}")
    print(f"总大小：{stats['total_size'] / 1024 / 1024:.2f} MB")
    print(f"格式分布：{stats['by_format']}")
```

---

### 2. 元数据提取器 (metadata.py)

```python
"""
电子书元数据提取器
支持 azw3/epub/pdf 格式
"""

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import fitz  # PyMuPDF for PDF
from typing import Dict, Optional

class MetadataExtractor:
    def __init__(self):
        """初始化提取器"""
        pass
    
    def extract(self, file_path: str) -> Optional[Dict]:
        """
        提取元数据
        
        Args:
            file_path: 文件路径
        
        Returns:
            元数据字典
        """
        ext = file_path.lower().split('.')[-1]
        
        if ext == 'epub':
            return self._extract_epub(file_path)
        elif ext == 'azw3':
            return self._extract_azw3(file_path)
        elif ext == 'pdf':
            return self._extract_pdf(file_path)
        else:
            return None
    
    def _extract_epub(self, file_path: str) -> Dict:
        """提取 EPUB 元数据"""
        book = epub.read_epub(file_path)
        
        metadata = {
            'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else '',
            'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else '',
            'language': book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else '',
            'publisher': book.get_metadata('DC', 'publisher')[0][0] if book.get_metadata('DC', 'publisher') else '',
            'isbn': book.get_metadata('DC', 'identifier')[0][0] if book.get_metadata('DC', 'identifier') else '',
        }
        
        return metadata
    
    def _extract_azw3(self, file_path: str) -> Dict:
        """
        提取 AZW3 元数据
        注：需要 Calibre 的 ebook-meta 工具
        """
        import subprocess
        
        try:
            result = subprocess.run(
                ['ebook-meta', file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            metadata = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            
            return metadata
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_pdf(self, file_path: str) -> Dict:
        """提取 PDF 元数据"""
        doc = fitz.open(file_path)
        metadata = doc.metadata
        
        return {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
        }


# 使用示例
if __name__ == '__main__':
    extractor = MetadataExtractor()
    metadata = extractor.extract('books/example.epub')
    print(f"书名：{metadata['title']}")
    print(f"作者：{metadata['author']}")
```

---

### 3. 质量评估器 (quality.py)

```python
"""
电子书质量评估器
根据文件大小、格式、完整度等评估质量等级
"""

from pathlib import Path
from typing import Dict, Tuple

class QualityAssessor:
    """质量评估器"""
    
    # 质量等级标准
    GRADE_STANDARDS = {
        'A': {'min_size_kb': 500, 'has_metadata': True, 'complete': True},
        'B': {'min_size_kb': 200, 'has_metadata': True},
        'C': {'min_size_kb': 50},
        'D': {'min_size_kb': 0}
    }
    
    def __init__(self):
        """初始化评估器"""
        pass
    
    def assess(self, book_info: Dict, metadata: Dict = None) -> Tuple[str, str]:
        """
        评估书籍质量
        
        Args:
            book_info: 书籍信息
            metadata: 元数据
        
        Returns:
            (等级，评估理由)
        """
        size_kb = book_info['size'] / 1024
        has_metadata = metadata is not None and len(metadata) > 0
        
        # A 级：大文件 + 完整元数据
        if size_kb >= 500 and has_metadata:
            return 'A', '高质量：大文件 + 完整元数据'
        
        # B 级：中等文件 + 有元数据
        if size_kb >= 200 and has_metadata:
            return 'B', '良好：中等文件 + 有元数据'
        
        # C 级：小文件
        if size_kb >= 50:
            return 'C', '一般：小文件'
        
        # D 级：极小文件
        return 'D', '低质量：文件过小'
    
    def batch_assess(self, books: list) -> Dict:
        """
        批量评估
        
        Args:
            books: 书籍列表
        
        Returns:
            评估结果统计
        """
        results = {'A': [], 'B': [], 'C': [], 'D': []}
        
        for book in books:
            grade, reason = self.assess(book)
            book['quality_grade'] = grade
            book['quality_reason'] = reason
            results[grade].append(book)
        
        return results


# 使用示例
if __name__ == '__main__':
    assessor = QualityAssessor()
    
    books = [
        {'path': 'book1.epub', 'size': 1024*1024},  # 1MB
        {'path': 'book2.epub', 'size': 300*1024},   # 300KB
        {'path': 'book3.epub', 'size': 80*1024},    # 80KB
    ]
    
    results = assessor.batch_assess(books)
    
    print(f"A 级：{len(results['A'])} 本")
    print(f"B 级：{len(results['B'])} 本")
    print(f"C 级：{len(results['C'])} 本")
    print(f"D 级：{len(results['D'])} 本")
```

---

### 4. 重复检测器 (dedup.py)

```python
"""
电子书重复检测器
基于书名、作者、ISBN、文件哈希等检测重复
"""

import hashlib
from typing import List, Dict, Set

class DedupDetector:
    """重复检测器"""
    
    def __init__(self):
        """初始化检测器"""
        pass
    
    def detect_duplicates(self, books: List[Dict]) -> Dict:
        """
        检测重复书籍
        
        Args:
            books: 书籍列表（包含元数据）
        
        Returns:
            重复组字典
        """
        # 按书名 + 作者分组
        groups = {}
        
        for book in books:
            key = self._generate_key(book)
            if key not in groups:
                groups[key] = []
            groups[key].append(book)
        
        # 过滤出重复组
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        
        return duplicates
    
    def _generate_key(self, book: Dict) -> str:
        """
        生成书籍唯一键
        
        Args:
            book: 书籍信息
        
        Returns:
            唯一键
        """
        # 优先使用 ISBN
        if 'isbn' in book and book['isbn']:
            return f"isbn:{book['isbn']}"
        
        # 否则使用书名 + 作者
        title = book.get('title', '').lower().strip()
        author = book.get('author', '').lower().strip()
        
        return f"title:{title}|author:{author}"
    
    def calculate_file_hash(self, file_path: str) -> str:
        """
        计算文件哈希（用于检测完全相同的文件）
        
        Args:
            file_path: 文件路径
        
        Returns:
            MD5 哈希值
        """
        hash_md5 = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        
        return hash_md5.hexdigest()
    
    def remove_duplicates(self, duplicates: Dict, keep_strategy: str = 'best') -> List[Dict]:
        """
        移除重复书籍
        
        Args:
            duplicates: 重复组字典
            keep_strategy: 保留策略 ('best' | 'first' | 'largest')
        
        Returns:
            要删除的书籍列表
        """
        to_delete = []
        
        for key, books in duplicates.items():
            if keep_strategy == 'best':
                # 保留质量最好的
                sorted_books = sorted(books, key=lambda x: x.get('quality_grade', 'D'), reverse=True)
                to_delete.extend(sorted_books[1:])
            elif keep_strategy == 'largest':
                # 保留文件最大的
                sorted_books = sorted(books, key=lambda x: x.get('size', 0), reverse=True)
                to_delete.extend(sorted_books[1:])
            else:
                # 保留第一个
                to_delete.extend(books[1:])
        
        return to_delete


# 使用示例
if __name__ == '__main__':
    detector = DedupDetector()
    
    books = [
        {'title': 'Python 编程', 'author': '张三', 'path': 'book1.epub'},
        {'title': 'Python 编程', 'author': '张三', 'path': 'book2.epub'},  # 重复
        {'title': '机器学习', 'author': '李四', 'path': 'book3.epub'},
    ]
    
    duplicates = detector.detect_duplicates(books)
    print(f"发现 {len(duplicates)} 组重复")
    
    to_delete = detector.remove_duplicates(duplicates)
    print(f"将删除 {len(to_delete)} 本书")
```

---

### 5. 分类整理器 (organizer.py)

```python
"""
电子书分类整理器
按领域、难度、优先级等分类
"""

from pathlib import Path
from typing import Dict, List

class LibraryOrganizer:
    """图书馆整理器"""
    
    # 领域分类关键词
    DOMAIN_KEYWORDS = {
        '经济学': ['经济学', '经济', 'macroeconomics', 'microeconomics'],
        '投资学': ['投资', '股票', '基金', 'investing', 'stock'],
        '管理学': ['管理', '领导', '团队', 'management', 'leadership'],
        '心理学': ['心理', '行为', 'cognitive', 'psychology'],
        '哲学': ['哲学', '思维', 'philosophy'],
        '传记': ['传记', '自传', 'biography'],
        '其他': []
    }
    
    def __init__(self, output_path: str):
        """
        初始化整理器
        
        Args:
            output_path: 输出目录
        """
        self.output_path = Path(output_path)
    
    def classify_by_domain(self, book: Dict) -> str:
        """
        按领域分类
        
        Args:
            book: 书籍信息
        
        Returns:
            领域名称
        """
        title = book.get('title', '').lower()
        author = book.get('author', '').lower()
        
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title or keyword.lower() in author:
                    return domain
        
        return '其他'
    
    def classify_by_difficulty(self, book: Dict) -> str:
        """
        按难度分类
        
        Args:
            book: 书籍信息
        
        Returns:
            难度等级
        """
        # 简单规则：根据书名关键词判断
        title = book.get('title', '').lower()
        
        if any(kw in title for kw in ['入门', '基础', 'intro', 'beginner']):
            return '入门'
        elif any(kw in title for kw in ['进阶', '中级', 'intermediate']):
            return '进阶'
        elif any(kw in title for kw in ['高级', 'advanced', 'expert']):
            return '高级'
        else:
            return '中级'
    
    def organize(self, books: List[Dict]) -> Dict:
        """
        整理书籍
        
        Args:
            books: 书籍列表
        
        Returns:
            分类结果
        """
        result = {
            'by_domain': {},
            'by_difficulty': {},
            'by_quality': {}
        }
        
        for book in books:
            # 按领域
            domain = self.classify_by_domain(book)
            if domain not in result['by_domain']:
                result['by_domain'][domain] = []
            result['by_domain'][domain].append(book)
            
            # 按难度
            difficulty = self.classify_by_difficulty(book)
            if difficulty not in result['by_difficulty']:
                result['by_difficulty'][difficulty] = []
            result['by_difficulty'][difficulty].append(book)
            
            # 按质量
            quality = book.get('quality_grade', 'C')
            if quality not in result['by_quality']:
                result['by_quality'][quality] = []
            result['by_quality'][quality].append(book)
        
        return result
    
    def export_to_bitable(self, books: List[Dict], app_token: str, table_id: str):
        """
        导出到飞书 Bitable
        
        Args:
            books: 书籍列表
            app_token: Bitable app_token
            table_id: 表格 ID
        """
        # TODO: 调用飞书 API 导入
        pass


# 使用示例
if __name__ == '__main__':
    organizer = LibraryOrganizer('output/')
    
    books = [
        {'title': '经济学原理', 'author': '曼昆', 'quality_grade': 'A'},
        {'title': 'Python 入门', 'author': '张三', 'quality_grade': 'B'},
        {'title': '机器学习进阶', 'author': '李四', 'quality_grade': 'A'},
    ]
    
    result = organizer.organize(books)
    
    print(f"按领域：{list(result['by_domain'].keys())}")
    print(f"按难度：{list(result['by_difficulty'].keys())}")
    print(f"按质量：{list(result['by_quality'].keys())}")
```

---

## 🔐 安全提示

**重要**: 请勿将敏感信息提交到 Git 仓库！

### 敏感文件（已加入 .gitignore）
- `.env` - 环境配置（API Token、密码等）
- `models.json` - 模型配置（API Key）
- `*.local` - 本地配置文件
- `logs/` - 日志文件

### 配置示例
```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 填入实际值
# 请勿将 .env 提交到 Git！
```

### 已保护的内容
- ✅ Tushare API Token
- ✅ 飞书 API Token
- ✅ 数据库连接字符串
- ✅ 本地路径配置

---

## 📋 使用流程

### 1. 扫描书库

```bash
cd modules/ebook_library
python scanner.py
```

### 2. 提取元数据

```bash
python metadata.py --input books/
```

### 3. 质量评估

```bash
python quality.py --input scan_results.json
```

### 4. 重复检测

```bash
python dedup.py --input metadata_results.json
```

### 5. 分类整理

```bash
python organizer.py --input quality_results.json --output organized/
```

### 6. 导出到 Bitable

```bash
python organizer.py --export-bitable --app-token BVxPbe1AnayZEBswgdxcN3yqnrb
```

---

## 📊 预期效果

### 处理流程

```
Calibre 书库 (原始)
    ↓ 扫描
书籍文件列表
    ↓ 元数据提取
完整元数据
    ↓ 质量评估
A/B/C/D 分级
    ↓ 重复检测
去重后书库
    ↓ 分类整理
按领域/难度/质量分类
    ↓ 导出
Bitable 书库
```

### 预期成果

| 指标 | 目标 |
|------|------|
| 扫描速度 | 1000 本/分钟 |
| 元数据提取率 | >80% |
| 质量评估准确率 | >90% |
| 重复检测准确率 | >95% |
| 空间节省 | 20-30% |

---

## 🔗 相关资源

- [Calibre 官方文档](https://manual.calibre-ebook.com/)
- [ebooklib](https://github.com/aerkalov/ebooklib)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [飞书 Bitable API](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14SM2ATN)

---

*文骐致远 · 电子书库管理模块*  
**版本**: v1.0  
**创建时间**: 2026-03-25  
**状态**: 🟡 开发中

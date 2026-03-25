"""
电子书元数据提取器
支持 azw3/epub/pdf 格式
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    HAS_EBOOKLIB = True
except ImportError:
    HAS_EBOOKLIB = False
    print("警告：ebooklib 未安装，EPUB 元数据提取将不可用")
    print("安装：pip install ebooklib beautifulsoup4")

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    print("警告：PyMuPDF 未安装，PDF 元数据提取将不可用")
    print("安装：pip install pymupdf")


class MetadataExtractor:
    """电子书元数据提取器"""
    
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
        elif ext == 'mobi':
            return self._extract_mobi(file_path)
        else:
            # 其他格式返回基本信息
            return self._extract_basic(file_path)
    
    def _extract_epub(self, file_path: str) -> Dict:
        """提取 EPUB 元数据"""
        if not HAS_EBOOKLIB:
            return self._extract_basic(file_path)
        
        try:
            book = epub.read_epub(file_path)
            
            metadata = {
                'title': '',
                'author': '',
                'language': '',
                'publisher': '',
                'isbn': '',
                'date': '',
                'description': '',
                'subjects': [],
                'extracted_at': datetime.now().isoformat()
            }
            
            # 提取 DC 元数据
            title_list = book.get_metadata('DC', 'title')
            if title_list:
                metadata['title'] = title_list[0][0]
            
            creator_list = book.get_metadata('DC', 'creator')
            if creator_list:
                metadata['author'] = creator_list[0][0]
            
            lang_list = book.get_metadata('DC', 'language')
            if lang_list:
                metadata['language'] = lang_list[0][0]
            
            publisher_list = book.get_metadata('DC', 'publisher')
            if publisher_list:
                metadata['publisher'] = publisher_list[0][0]
            
            id_list = book.get_metadata('DC', 'identifier')
            if id_list:
                metadata['isbn'] = id_list[0][0]
            
            date_list = book.get_metadata('DC', 'date')
            if date_list:
                metadata['date'] = date_list[0][0]
            
            # 提取简介
            for item in book.get_items_of_kind('kind'):
                if item.get_type() == ebooklib.ITEM_COVER:
                    continue
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    # 查找描述段落
                    for p in soup.find_all(['p', 'div']):
                        text = p.get_text().strip()
                        if len(text) > 50 and len(text) < 500:
                            metadata['description'] = text
                            break
            
            # 提取主题
            for item in book.get_items_of_kind('kind'):
                if 'subject' in item.get_name().lower():
                    metadata['subjects'].append(item.get_name())
            
            return metadata
            
        except Exception as e:
            print(f"EPUB 元数据提取失败 {file_path}: {e}")
            return self._extract_basic(file_path)
    
    def _extract_azw3(self, file_path: str) -> Dict:
        """
        提取 AZW3 元数据
        使用 Calibre 的 ebook-meta 工具
        """
        try:
            # 检查 ebook-meta 是否可用
            result = subprocess.run(
                ['ebook-meta', file_path],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                return self._extract_basic(file_path)
            
            metadata = {
                'extracted_at': datetime.now().isoformat()
            }
            
            # 解析输出
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()
                    
                    if key == 'title':
                        metadata['title'] = value
                    elif key in ['author', 'authors']:
                        metadata['author'] = value
                    elif key == 'isbn':
                        metadata['isbn'] = value
                    elif key == 'publisher':
                        metadata['publisher'] = value
                    elif key == 'languages':
                        metadata['language'] = value
                    elif key == 'comments':
                        metadata['description'] = value
                    elif key == 'tags':
                        metadata['subjects'] = value.split(', ')
                    elif key == 'pubdate':
                        metadata['date'] = value
            
            return metadata
            
        except FileNotFoundError:
            print("警告：ebook-meta 未找到，请安装 Calibre")
            return self._extract_basic(file_path)
        except Exception as e:
            print(f"AZW3 元数据提取失败 {file_path}: {e}")
            return self._extract_basic(file_path)
    
    def _extract_pdf(self, file_path: str) -> Dict:
        """提取 PDF 元数据"""
        if not HAS_PYMUPDF:
            return self._extract_basic(file_path)
        
        try:
            doc = fitz.open(file_path)
            metadata = doc.metadata
            
            return {
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'creation_date': metadata.get('creationDate', ''),
                'mod_date': metadata.get('modDate', ''),
                'pages': len(doc),
                'extracted_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"PDF 元数据提取失败 {file_path}: {e}")
            return self._extract_basic(file_path)
    
    def _extract_mobi(self, file_path: str) -> Dict:
        """提取 MOBI 元数据（使用 ebook-meta）"""
        return self._extract_azw3(file_path)
    
    def _extract_basic(self, file_path: str) -> Dict:
        """提取基本文件信息"""
        path = Path(file_path)
        
        return {
            'filename': path.name,
            'path': str(path),
            'size': path.stat().st_size,
            'format': path.suffix.lower(),
            'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            'extracted_at': datetime.now().isoformat()
        }
    
    def batch_extract(self, books: List[Dict], output_path: str = None) -> List[Dict]:
        """
        批量提取元数据
        
        Args:
            books: 书籍列表（包含 path 字段）
            output_path: 输出文件路径（可选）
        
        Returns:
            包含元数据的书籍列表
        """
        results = []
        total = len(books)
        
        print(f"开始批量提取元数据，共 {total} 本书")
        
        for i, book in enumerate(books, 1):
            if i % 10 == 0:
                print(f"进度：{i}/{total} ({i/total*100:.1f}%)")
            
            file_path = book.get('path', '')
            if not file_path or not os.path.exists(file_path):
                print(f"跳过：文件不存在 {file_path}")
                continue
            
            metadata = self.extract(file_path)
            
            # 合并原有信息
            book_with_meta = {**book, **metadata}
            results.append(book_with_meta)
        
        print(f"元数据提取完成，成功 {len(results)}/{total} 本")
        
        # 保存结果
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"结果已保存：{output_file}")
        
        return results


def main():
    """主函数"""
    # 从扫描结果读取
    scan_results_path = 'modules/ebook_library/output/scan_results.json'
    output_path = 'modules/ebook_library/output/metadata_results.json'
    
    if not os.path.exists(scan_results_path):
        print(f"错误：扫描结果文件不存在：{scan_results_path}")
        print("请先运行：python scanner.py")
        return
    
    # 读取扫描结果
    with open(scan_results_path, 'r', encoding='utf-8') as f:
        books = json.load(f)
    
    print(f"读取到 {len(books)} 本书")
    
    # 批量提取元数据
    extractor = MetadataExtractor()
    results = extractor.batch_extract(books, output_path)
    
    # 统计
    with_metadata = sum(1 for b in results if b.get('title'))
    print(f"\n=== 元数据统计 ===")
    print(f"总书籍数：{len(results)}")
    print(f"有书名：{with_metadata} 本 ({with_metadata/len(results)*100:.1f}%)")


if __name__ == '__main__':
    main()

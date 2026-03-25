"""
Calibre 电子书库扫描器
扫描书库，提取书籍文件列表
"""

import os
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

class CalibreScanner:
    """Calibre 电子书库扫描器"""
    
    def __init__(self, library_path: str):
        """
        初始化扫描器
        
        Args:
            library_path: Calibre 书库路径
        """
        self.library_path = Path(library_path)
        self.supported_formats = ['.azw3', '.epub', '.pdf', '.mobi', '.txt', '.fb2']
    
    def scan(self) -> List[Dict]:
        """
        扫描书库
        
        Returns:
            书籍文件列表
        """
        print(f"开始扫描书库：{self.library_path}")
        books = []
        
        for root, dirs, files in os.walk(self.library_path):
            # 跳过隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.supported_formats:
                    book_info = {
                        'path': str(file_path),
                        'filename': file_path.name,
                        'size': file_path.stat().st_size,
                        'format': file_path.suffix.lower(),
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        'scanned_at': datetime.now().isoformat()
                    }
                    books.append(book_info)
        
        print(f"扫描完成，发现 {len(books)} 本书")
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
            'total_size_mb': sum(b['size'] for b in books) / 1024 / 1024,
            'by_format': {}
        }
        
        # 按格式统计
        for book in books:
            fmt = book['format']
            if fmt not in stats['by_format']:
                stats['by_format'][fmt] = {'count': 0, 'size': 0}
            stats['by_format'][fmt]['count'] += 1
            stats['by_format'][fmt]['size'] += book['size']
        
        # 添加格式统计的 MB
        for fmt in stats['by_format']:
            stats['by_format'][fmt]['size_mb'] = stats['by_format'][fmt]['size'] / 1024 / 1024
        
        return stats
    
    def save_results(self, books: List[Dict], output_path: str):
        """
        保存扫描结果
        
        Args:
            books: 书籍列表
            output_path: 输出路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        
        print(f"扫描结果已保存：{output_file}")


def main():
    """主函数"""
    # 配置书库路径
    library_path = 'E:/Calibre 书库'
    output_path = 'modules/ebook_library/output/scan_results.json'
    
    # 检查路径是否存在
    if not os.path.exists(library_path):
        print(f"错误：书库路径不存在：{library_path}")
        return
    
    # 扫描书库
    scanner = CalibreScanner(library_path)
    books = scanner.scan()
    
    # 获取统计
    stats = scanner.get_statistics(books)
    
    # 打印统计
    print(f"\n=== 书库统计 ===")
    print(f"总书籍数：{stats['total_books']}")
    print(f"总大小：{stats['total_size_mb']:.2f} MB")
    print(f"\n格式分布:")
    for fmt, info in stats['by_format'].items():
        print(f"  {fmt}: {info['count']} 本 ({info['size_mb']:.2f} MB)")
    
    # 保存结果
    scanner.save_results(books, output_path)


if __name__ == '__main__':
    main()

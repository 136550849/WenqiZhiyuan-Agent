"""
电子书重复检测器
基于书名、作者、ISBN、文件哈希等检测重复
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Tuple
from datetime import datetime


class DedupDetector:
    """电子书重复检测器"""
    
    def __init__(self):
        """初始化检测器"""
        pass
    
    def detect_duplicates(self, books: List[Dict], strategy: str = 'smart') -> Dict:
        """
        检测重复书籍
        
        Args:
            books: 书籍列表（包含元数据）
            strategy: 检测策略 ('smart' | 'strict' | 'loose')
        
        Returns:
            重复组字典
        """
        if strategy == 'smart':
            return self._detect_smart(books)
        elif strategy == 'strict':
            return self._detect_strict(books)
        elif strategy == 'loose':
            return self._detect_loose(books)
        else:
            raise ValueError(f"未知策略：{strategy}")
    
    def _detect_smart(self, books: List[Dict]) -> Dict:
        """
        智能检测（推荐）
        优先级：ISBN > 书名 + 作者 > 书名（模糊匹配）
        """
        groups = {}
        
        for book in books:
            # 优先使用 ISBN
            if book.get('isbn'):
                key = f"isbn:{book['isbn']}"
            # 其次使用书名 + 作者
            elif book.get('title') and book.get('author'):
                title = self._normalize_text(book['title'])
                author = self._normalize_text(book['author'])
                key = f"title_author:{title}|{author}"
            # 最后仅使用书名
            elif book.get('title'):
                title = self._normalize_text(book['title'])
                key = f"title:{title}"
            else:
                continue
            
            if key not in groups:
                groups[key] = []
            groups[key].append(book)
        
        # 过滤出重复组
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        
        return duplicates
    
    def _detect_strict(self, books: List[Dict]) -> Dict:
        """
        严格检测
        仅匹配完全相同的书名 + 作者 + ISBN
        """
        groups = {}
        
        for book in books:
            title = self._normalize_text(book.get('title', ''))
            author = self._normalize_text(book.get('author', ''))
            isbn = book.get('isbn', '')
            
            key = f"strict:{title}|{author}|{isbn}"
            
            if key not in groups:
                groups[key] = []
            groups[key].append(book)
        
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        return duplicates
    
    def _detect_loose(self, books: List[Dict]) -> Dict:
        """
        宽松检测
        仅匹配书名（模糊）
        """
        groups = {}
        
        for book in books:
            if not book.get('title'):
                continue
            
            title = self._normalize_text(book['title'])
            # 移除副标题等
            title = title.split(':')[0].split('(')[0].strip()
            
            key = f"loose:{title}"
            
            if key not in groups:
                groups[key] = []
            groups[key].append(book)
        
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        return duplicates
    
    def _normalize_text(self, text: str) -> str:
        """
        标准化文本（用于比较）
        
        Args:
            text: 原始文本
        
        Returns:
            标准化后的文本
        """
        if not text:
            return ''
        
        # 转小写
        text = text.lower()
        
        # 移除特殊字符
        text = ''.join(c for c in text if c.isalnum() or c.isspace())
        
        # 移除多余空格
        text = ' '.join(text.split())
        
        return text
    
    def calculate_file_hash(self, file_path: str) -> str:
        """
        计算文件哈希（用于检测完全相同的文件）
        
        Args:
            file_path: 文件路径
        
        Returns:
            MD5 哈希值
        """
        if not os.path.exists(file_path):
            return ''
        
        hash_md5 = hashlib.md5()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"计算哈希失败 {file_path}: {e}")
            return ''
    
    def detect_by_hash(self, books: List[Dict]) -> Dict:
        """
        基于文件哈希检测重复（完全相同的文件）
        
        Args:
            books: 书籍列表
        
        Returns:
            重复组字典
        """
        groups = {}
        
        for book in books:
            file_path = book.get('path', '')
            if not file_path or not os.path.exists(file_path):
                continue
            
            file_hash = self.calculate_file_hash(file_path)
            if not file_hash:
                continue
            
            if file_hash not in groups:
                groups[file_hash] = []
            groups[file_hash].append(book)
        
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        return duplicates
    
    def remove_duplicates(self, duplicates: Dict, keep_strategy: str = 'best') -> List[Dict]:
        """
        移除重复书籍
        
        Args:
            duplicates: 重复组字典
            keep_strategy: 保留策略
                - 'best': 保留质量最好的
                - 'first': 保留第一个
                - 'largest': 保留文件最大的
                - 'newest': 保留最新的
        
        Returns:
            要删除的书籍列表
        """
        to_delete = []
        kept_books = []
        
        for key, books in duplicates.items():
            if len(books) == 1:
                kept_books.append(books[0])
                continue
            
            # 排序
            if keep_strategy == 'best':
                # 按质量分数排序
                sorted_books = sorted(
                    books,
                    key=lambda x: x.get('quality_score', 0),
                    reverse=True
                )
            elif keep_strategy == 'largest':
                # 按文件大小排序
                sorted_books = sorted(
                    books,
                    key=lambda x: x.get('size', 0),
                    reverse=True
                )
            elif keep_strategy == 'newest':
                # 按修改时间排序
                sorted_books = sorted(
                    books,
                    key=lambda x: x.get('modified', ''),
                    reverse=True
                )
            else:  # first
                sorted_books = books
            
            # 保留最好的
            kept_books.append(sorted_books[0])
            
            # 其余标记为删除
            to_delete.extend(sorted_books[1:])
        
        return to_delete, kept_books
    
    def generate_report(self, duplicates: Dict, to_delete: List[Dict], output_path: str):
        """
        生成去重报告
        
        Args:
            duplicates: 重复组字典
            to_delete: 要删除的书籍列表
            output_path: 输出路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 统计
        total_duplicates = sum(len(books) for books in duplicates.values())
        duplicate_groups = len(duplicates)
        to_delete_count = len(to_delete)
        space_saved = sum(b.get('size', 0) for b in to_delete)
        
        report = f"""# 📋 电子书去重报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 统计摘要

| 指标 | 数值 |
|------|------|
| 重复组数 | {duplicate_groups} |
| 重复书籍总数 | {total_duplicates} |
| 建议删除数量 | {to_delete_count} |
| 预计节省空间 | {space_saved / 1024 / 1024:.2f} MB |

---

## 🔍 重复组详情

"""
        
        # 列出前 20 个重复组
        for i, (key, books) in enumerate(list(duplicates.items())[:20], 1):
            report += f"\n### 重复组 {i}\n\n"
            report += f"**匹配键**: `{key}`\n\n"
            report += "| 书名 | 作者 | 格式 | 大小 | 质量 |\n"
            report += "|------|------|------|------|------|\n"
            
            for book in books:
                title = book.get('title', '未知书名')[:30]
                author = book.get('author', '未知作者')[:20]
                fmt = book.get('format', '未知')
                size_kb = book.get('size', 0) / 1024
                grade = book.get('quality_grade', '?')
                
                report += f"| {title} | {author} | {fmt} | {size_kb:.0f}KB | {grade} |\n"
        
        if duplicate_groups > 20:
            report += f"\n... 还有 {duplicate_groups - 20} 个重复组\n"
        
        report += "\n---\n\n## 🗑️ 建议删除列表\n\n"
        
        if to_delete:
            report += "| 书名 | 作者 | 格式 | 大小 | 删除原因 |\n"
            report += "|------|------|------|------|----------|\n"
            
            for book in to_delete[:50]:  # 只显示前 50 本
                title = book.get('title', '未知书名')[:30]
                author = book.get('author', '未知作者')[:20]
                fmt = book.get('format', '未知')
                size_kb = book.get('size', 0) / 1024
                
                report += f"| {title} | {author} | {fmt} | {size_kb:.0f}KB | 重复 |\n"
            
            if len(to_delete) > 50:
                report += f"\n... 还有 {len(to_delete) - 50} 本\n"
        else:
            report += "无需删除\n"
        
        report += "\n---\n\n*电子书去重检测器 v1.0*\n"
        
        # 保存报告
        report_path = output_file.parent / 'dedup_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存 JSON 结果
        results = {
            'duplicates': duplicates,
            'to_delete': to_delete,
            'statistics': {
                'duplicate_groups': duplicate_groups,
                'total_duplicates': total_duplicates,
                'to_delete_count': to_delete_count,
                'space_saved_mb': space_saved / 1024 / 1024
            },
            'generated_at': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"去重报告已保存:")
        print(f"  - JSON: {output_file}")
        print(f"  - Markdown: {report_path}")


def main():
    """主函数"""
    # 从质量结果读取
    quality_path = 'modules/ebook_library/output/quality_results.json'
    output_path = 'modules/ebook_library/output/dedup_results.json'
    
    if not os.path.exists(quality_path):
        print(f"错误：质量评估文件不存在：{quality_path}")
        print("请先运行：python quality.py")
        return
    
    # 读取质量结果
    with open(quality_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 合并所有等级的书籍
    books = []
    for grade in ['A', 'B', 'C', 'D']:
        if grade in data:
            books.extend(data[grade])
    
    print(f"读取到 {len(books)} 本书")
    
    # 检测重复
    detector = DedupDetector()
    
    print("\n=== 智能检测 ===")
    duplicates = detector.detect_duplicates(books, strategy='smart')
    print(f"发现 {len(duplicates)} 组重复")
    
    # 移除重复
    to_delete, kept = detector.remove_duplicates(duplicates, keep_strategy='best')
    print(f"建议删除：{len(to_delete)} 本")
    print(f"保留：{len(kept)} 本")
    
    # 计算节省空间
    space_saved = sum(b.get('size', 0) for b in to_delete)
    print(f"预计节省空间：{space_saved / 1024 / 1024:.2f} MB")
    
    # 生成报告
    detector.generate_report(duplicates, to_delete, output_path)


if __name__ == '__main__':
    main()

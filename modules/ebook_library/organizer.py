"""
电子书分类整理器
按领域、难度、优先级等分类
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class LibraryOrganizer:
    """电子书图书馆整理器"""
    
    # 领域分类关键词
    DOMAIN_KEYWORDS = {
        '经济学': ['经济学', '经济', 'macroeconomics', 'microeconomics', '曼昆', '萨缪尔森'],
        '投资学': ['投资', '股票', '基金', '债券', 'investing', 'stock', 'value', '证券'],
        '管理学': ['管理', '领导', '团队', '组织', 'management', 'leadership', '德鲁克'],
        '心理学': ['心理', '行为', '认知', 'cognitive', 'psychology', 'behavioral'],
        '哲学': ['哲学', '思维', '逻辑', 'philosophy', '思考'],
        '传记': ['传记', '自传', '回忆录', 'biography', 'memoir'],
        '历史': ['历史', '战争', '政治', 'history', 'war', 'politics'],
        '科学': ['科学', '物理', '数学', '生物', 'science', 'physics', 'math'],
        '文学': ['小说', '散文', '诗歌', 'fiction', 'novel', 'literature'],
        '其他': []
    }
    
    # 难度分类关键词
    DIFFICULTY_KEYWORDS = {
        '入门': ['入门', '基础', '初级', 'introduction', 'beginner', 'guide'],
        '进阶': ['进阶', '中级', 'intermediate', 'advanced'],
        '高级': ['高级', '专家', 'expert', 'master', 'professional'],
        '研究': ['研究', '学术', '论文', 'research', 'academic', 'thesis']
    }
    
    def __init__(self, output_path: str = 'modules/ebook_library/output/'):
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
        title = (book.get('title', '') + ' ' + book.get('author', '')).lower()
        subjects = ' '.join(book.get('subjects', [])).lower()
        
        # 搜索关键词
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title or keyword.lower() in subjects:
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
        title = book.get('title', '').lower()
        
        # 检查难度关键词
        for difficulty, keywords in self.DIFFICULTY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title:
                    return difficulty
        
        # 默认中级
        return '中级'
    
    def classify_by_priority(self, book: Dict) -> str:
        """
        按优先级分类（基于质量等级和用户需求）
        
        Args:
            book: 书籍信息
        
        Returns:
            优先级 (P0/P1/P2/P3)
        """
        quality_grade = book.get('quality_grade', 'C')
        
        # P0: A 级 + 投资/经济领域
        domain = self.classify_by_domain(book)
        if quality_grade == 'A' and domain in ['投资学', '经济学']:
            return 'P0'
        
        # P1: A 级或 B 级
        if quality_grade in ['A', 'B']:
            return 'P1'
        
        # P2: C 级
        if quality_grade == 'C':
            return 'P2'
        
        # P3: D 级
        return 'P3'
    
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
            'by_priority': {},
            'combined': {},
            'statistics': {}
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
            
            # 按优先级
            priority = self.classify_by_priority(book)
            if priority not in result['by_priority']:
                result['by_priority'][priority] = []
            result['by_priority'][priority].append(book)
            
            # 组合分类（领域 + 难度）
            key = f"{domain}_{difficulty}"
            if key not in result['combined']:
                result['combined'][key] = []
            result['combined'][key].append(book)
        
        # 统计信息
        result['statistics'] = {
            'total_books': len(books),
            'by_domain': {k: len(v) for k, v in result['by_domain'].items()},
            'by_difficulty': {k: len(v) for k, v in result['by_difficulty'].items()},
            'by_priority': {k: len(v) for k, v in result['by_priority'].items()},
            'organized_at': datetime.now().isoformat()
        }
        
        return result
    
    def export_to_markdown(self, result: Dict, output_path: str):
        """
        导出为 Markdown 报告
        
        Args:
            result: 分类结果
            output_path: 输出路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        stats = result['statistics']
        
        report = f"""# 📚 电子书分类整理报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 总体统计

| 指标 | 数值 |
|------|------|
| 总书籍数 | {stats['total_books']} |
| 领域分类数 | {len(stats['by_domain'])} |
| 难度分级数 | {len(stats['by_difficulty'])} |
| 优先级分级数 | {len(stats['by_priority'])} |

---

## 📖 按领域分类

| 领域 | 书籍数 | 占比 |
|------|--------|------|
"""
        
        for domain, count in sorted(stats['by_domain'].items(), key=lambda x: x[1], reverse=True):
            pct = count / stats['total_books'] * 100 if stats['total_books'] > 0 else 0
            report += f"| {domain} | {count} | {pct:.1f}% |\n"
        
        report += f"\n---\n\n## 📈 按难度分级\n\n"
        report += "| 难度 | 书籍数 | 占比 |\n"
        report += "|------|--------|------|\n"
        
        for difficulty, count in sorted(stats['by_difficulty'].items(), key=lambda x: x[1], reverse=True):
            pct = count / stats['total_books'] * 100 if stats['total_books'] > 0 else 0
            report += f"| {difficulty} | {count} | {pct:.1f}% |\n"
        
        report += f"\n---\n\n## 🎯 按优先级分类\n\n"
        report += "| 优先级 | 书籍数 | 说明 |\n"
        report += "|--------|--------|------|\n"
        
        priority_desc = {
            'P0': '最高优先级（投资/经济 A 级）',
            'P1': '高优先级（A/B 级）',
            'P2': '中优先级（C 级）',
            'P3': '低优先级（D 级）'
        }
        
        for priority in ['P0', 'P1', 'P2', 'P3']:
            count = stats['by_priority'].get(priority, 0)
            pct = count / stats['total_books'] * 100 if stats['total_books'] > 0 and priority in stats['by_priority'] else 0
            desc = priority_desc.get(priority, '')
            report += f"| {priority} | {count} | {pct:.1f}% - {desc} |\n"
        
        report += f"\n---\n\n## 📋 详细列表\n\n"
        
        # 列出每个领域的前 10 本书
        for domain, books in sorted(result['by_domain'].items(), key=lambda x: len(x[1]), reverse=True):
            report += f"\n### {domain} ({len(books)} 本)\n\n"
            report += "| 书名 | 作者 | 难度 | 质量 |\n"
            report += "|------|------|------|------|\n"
            
            for book in books[:10]:
                title = book.get('title', '未知书名')[:40]
                author = book.get('author', '未知作者')[:20]
                difficulty = self.classify_by_difficulty(book)
                grade = book.get('quality_grade', '?')
                
                report += f"| {title} | {author} | {difficulty} | {grade} |\n"
            
            if len(books) > 10:
                report += f"\n... 还有 {len(books) - 10} 本\n"
        
        report += "\n---\n\n*电子书分类整理器 v1.0*\n"
        
        # 保存报告
        report_path = output_file.parent / 'organization_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"分类报告已保存：{report_path}")
    
    def export_for_bitable(self, books: List[Dict], output_path: str):
        """
        导出为 Bitable 导入格式
        
        Args:
            books: 书籍列表
            output_path: 输出路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 准备 Bitable 字段
        records = []
        
        for book in books:
            record = {
                '书名': book.get('title', ''),
                '作者': book.get('author', ''),
                '领域': self.classify_by_domain(book),
                '难度': self.classify_by_difficulty(book),
                '优先级': self.classify_by_priority(book),
                '质量等级': book.get('quality_grade', ''),
                '质量分数': book.get('quality_score', 0),
                '文件格式': book.get('format', ''),
                '文件大小_KB': round(book.get('size', 0) / 1024, 2),
                'ISBN': book.get('isbn', ''),
                '出版社': book.get('publisher', ''),
                '出版日期': book.get('date', ''),
                '路径': book.get('path', ''),
                '备注': book.get('quality_reason', '')
            }
            records.append(record)
        
        # 保存为 JSON（Bitable 可通过 API 导入）
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        print(f"Bitable 导入文件已保存：{output_file}")
        print(f"共 {len(records)} 条记录")


def main():
    """主函数"""
    # 从去重结果读取
    dedup_path = 'modules/ebook_library/output/dedup_results.json'
    output_dir = 'modules/ebook_library/output/'
    
    if not os.path.exists(dedup_path):
        print(f"错误：去重结果文件不存在：{dedup_path}")
        print("请先运行：python dedup.py")
        return
    
    # 读取去重结果
    with open(dedup_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取保留的书籍（去重后的）
    # 注意：这里简化处理，实际应该从 duplicates 中提取 kept_books
    # 为演示，我们假设所有书籍都保留
    books = []
    for grade in ['A', 'B', 'C', 'D']:
        if grade in data:
            books.extend(data[grade])
    
    # 如果没有分级数据，直接使用 duplicates 中的书籍
    if not books and 'duplicates' in data:
        for key, book_list in data['duplicates'].items():
            books.extend(book_list)
    
    print(f"读取到 {len(books)} 本书")
    
    # 分类整理
    organizer = LibraryOrganizer(output_dir)
    result = organizer.organize(books)
    
    # 打印统计
    stats = result['statistics']
    print(f"\n=== 分类统计 ===")
    print(f"总书籍数：{stats['total_books']}")
    print(f"\n按领域:")
    for domain, count in sorted(stats['by_domain'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain}: {count} 本")
    
    print(f"\n按难度:")
    for difficulty, count in sorted(stats['by_difficulty'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {difficulty}: {count} 本")
    
    print(f"\n按优先级:")
    for priority in ['P0', 'P1', 'P2', 'P3']:
        count = stats['by_priority'].get(priority, 0)
        print(f"  {priority}: {count} 本")
    
    # 导出报告
    organizer.export_to_markdown(result, output_dir + 'organization_results.json')
    
    # 导出 Bitable 格式
    organizer.export_for_bitable(books, output_dir + 'bitable_import.json')


if __name__ == '__main__':
    main()

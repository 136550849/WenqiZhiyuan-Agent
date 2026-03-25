"""
电子书质量评估器
根据文件大小、格式、完整度等评估质量等级
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class QualityAssessor:
    """电子书质量评估器"""
    
    # 质量等级标准
    GRADE_STANDARDS = {
        'A': {
            'min_size_kb': 500,
            'has_metadata': True,
            'has_isbn': False,
            'description': '高质量：大文件 + 完整元数据'
        },
        'B': {
            'min_size_kb': 200,
            'has_metadata': True,
            'has_isbn': False,
            'description': '良好：中等文件 + 有元数据'
        },
        'C': {
            'min_size_kb': 50,
            'has_metadata': False,
            'has_isbn': False,
            'description': '一般：小文件'
        },
        'D': {
            'min_size_kb': 0,
            'has_metadata': False,
            'has_isbn': False,
            'description': '低质量：文件过小或不完整'
        }
    }
    
    # 格式优先级
    FORMAT_PRIORITY = {
        '.epub': 1,      # 最佳（开放标准）
        '.azw3': 2,      # 好（Kindle）
        '.mobi': 3,      # 一般（旧 Kindle）
        '.pdf': 4,       # 一般（固定布局）
        '.fb2': 2,       # 好（XML 格式）
        '.txt': 5        # 差（无格式）
    }
    
    def __init__(self):
        """初始化评估器"""
        pass
    
    def assess(self, book: Dict) -> Tuple[str, str, int]:
        """
        评估单本书质量
        
        Args:
            book: 书籍信息（包含 size, format, metadata）
        
        Returns:
            (等级，评估理由，质量分数 0-100)
        """
        size_kb = book.get('size', 0) / 1024
        file_format = book.get('format', '').lower()
        has_metadata = bool(book.get('title'))
        has_isbn = bool(book.get('isbn'))
        has_author = bool(book.get('author'))
        has_description = bool(book.get('description'))
        
        # 计算质量分数 (0-100)
        score = 0
        
        # 文件大小分数 (0-40 分)
        if size_kb >= 1000:
            score += 40
        elif size_kb >= 500:
            score += 30
        elif size_kb >= 200:
            score += 20
        elif size_kb >= 50:
            score += 10
        
        # 元数据分数 (0-30 分)
        if has_metadata:
            score += 15
        if has_isbn:
            score += 10
        if has_author:
            score += 5
        
        # 描述分数 (0-15 分)
        if has_description:
            score += 15
        
        # 格式分数 (0-15 分)
        format_score = 15 - (self.FORMAT_PRIORITY.get(file_format, 3) * 3)
        score += max(0, format_score)
        
        # 确定等级
        if score >= 80:
            grade = 'A'
            reason = '高质量：大文件 + 完整元数据 + ISBN'
        elif score >= 60:
            grade = 'B'
            reason = '良好：中等文件 + 有元数据'
        elif score >= 40:
            grade = 'C'
            reason = '一般：小文件或元数据不完整'
        else:
            grade = 'D'
            reason = '低质量：文件过小或信息缺失'
        
        return grade, reason, score
    
    def batch_assess(self, books: List[Dict]) -> Dict:
        """
        批量评估
        
        Args:
            books: 书籍列表
        
        Returns:
            评估结果统计
        """
        results = {
            'A': [],
            'B': [],
            'C': [],
            'D': [],
            'statistics': {}
        }
        
        total_score = 0
        
        for book in books:
            grade, reason, score = self.assess(book)
            book['quality_grade'] = grade
            book['quality_reason'] = reason
            book['quality_score'] = score
            book['assessed_at'] = datetime.now().isoformat()
            
            results[grade].append(book)
            total_score += score
        
        # 统计信息
        total_books = len(books)
        results['statistics'] = {
            'total_books': total_books,
            'by_grade': {
                'A': {'count': len(results['A']), 'percentage': len(results['A'])/total_books*100 if total_books > 0 else 0},
                'B': {'count': len(results['B']), 'percentage': len(results['B'])/total_books*100 if total_books > 0 else 0},
                'C': {'count': len(results['C']), 'percentage': len(results['C'])/total_books*100 if total_books > 0 else 0},
                'D': {'count': len(results['D']), 'percentage': len(results['D'])/total_books*100 if total_books > 0 else 0}
            },
            'average_score': total_score / total_books if total_books > 0 else 0,
            'assessed_at': datetime.now().isoformat()
        }
        
        return results
    
    def get_recommendations(self, results: Dict) -> Dict:
        """
        获取处理建议
        
        Args:
            results: 评估结果
        
        Returns:
            建议字典
        """
        stats = results['statistics']
        recommendations = {
            'keep': [],
            'improve': [],
            'remove': [],
            'notes': []
        }
        
        # A 级：保留
        recommendations['keep'] = results['A']
        
        # B 级：保留，可优化元数据
        for book in results['B']:
            if not book.get('isbn'):
                recommendations['improve'].append({
                    'book': book,
                    'action': '补充 ISBN 信息'
                })
        
        # C 级：检查是否需要
        for book in results['C']:
            recommendations['notes'].append({
                'book': book,
                'note': '检查内容价值，决定是否保留'
            })
        
        # D 级：建议删除
        recommendations['remove'] = results['D']
        
        # 总体建议
        if stats['by_grade']['D']['percentage'] > 20:
            recommendations['notes'].append('提示：D 级书籍超过 20%，建议清理书库')
        
        if stats['average_score'] < 50:
            recommendations['notes'].append('提示：平均质量分数较低，建议优化书库')
        
        return recommendations
    
    def export_report(self, results: Dict, output_path: str):
        """
        导出质量报告
        
        Args:
            results: 评估结果
            output_path: 输出路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成 Markdown 报告
        stats = results['statistics']
        
        report = f"""# 📊 电子书质量评估报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📈 总体统计

| 指标 | 数值 |
|------|------|
| 总书籍数 | {stats['total_books']} |
| 平均质量分数 | {stats['average_score']:.1f}/100 |
| 评估时间 | {stats['assessed_at']} |

---

## 📋 质量分级

| 等级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| A | {stats['by_grade']['A']['count']} | {stats['by_grade']['A']['percentage']:.1f}% | 高质量 |
| B | {stats['by_grade']['B']['count']} | {stats['by_grade']['B']['percentage']:.1f}% | 良好 |
| C | {stats['by_grade']['C']['count']} | {stats['by_grade']['C']['percentage']:.1f}% | 一般 |
| D | {stats['by_grade']['D']['count']} | {stats['by_grade']['D']['percentage']:.1f}% | 低质量 |

---

## 💡 处理建议

### 保留书籍 (A 级)
共 {len(results['A'])} 本

### 优化书籍 (B 级)
共 {len(results['B'])} 本
- 建议补充 ISBN 等元数据

### 检查书籍 (C 级)
共 {len(results['C'])} 本
- 检查内容价值，决定是否保留

### 删除书籍 (D 级)
共 {len(results['D'])} 本
- 文件过小或信息不完整

---

## 📊 详细列表

### A 级书籍
"""
        
        for book in results['A'][:20]:  # 只显示前 20 本
            report += f"- {book.get('title', '未知书名')} ({book.get('author', '未知作者')}) - {book.get('quality_score', 0)}分\n"
        
        if len(results['A']) > 20:
            report += f"\n... 还有 {len(results['A']) - 20} 本\n"
        
        report += "\n---\n\n*电子书质量评估器 v1.0*\n"
        
        # 保存报告
        report_path = output_file.parent / 'quality_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存 JSON 结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"质量报告已保存:")
        print(f"  - JSON: {output_file}")
        print(f"  - Markdown: {report_path}")


def main():
    """主函数"""
    # 从元数据结果读取
    metadata_path = 'modules/ebook_library/output/metadata_results.json'
    output_path = 'modules/ebook_library/output/quality_results.json'
    
    if not os.path.exists(metadata_path):
        print(f"错误：元数据文件不存在：{metadata_path}")
        print("请先运行：python metadata.py")
        return
    
    # 读取元数据
    with open(metadata_path, 'r', encoding='utf-8') as f:
        books = json.load(f)
    
    print(f"读取到 {len(books)} 本书")
    
    # 批量评估
    assessor = QualityAssessor()
    results = assessor.batch_assess(books)
    
    # 打印统计
    stats = results['statistics']
    print(f"\n=== 质量评估统计 ===")
    print(f"总书籍数：{stats['total_books']}")
    print(f"平均分数：{stats['average_score']:.1f}/100")
    print(f"\n质量分级:")
    for grade in ['A', 'B', 'C', 'D']:
        count = stats['by_grade'][grade]['count']
        pct = stats['by_grade'][grade]['percentage']
        print(f"  {grade}级：{count} 本 ({pct:.1f}%)")
    
    # 导出报告
    assessor.export_report(results, output_path)
    
    # 获取建议
    recommendations = assessor.get_recommendations(results)
    print(f"\n=== 处理建议 ===")
    print(f"保留：{len(recommendations['keep'])} 本")
    print(f"优化：{len(recommendations['improve'])} 本")
    print(f"检查：{len(recommendations['notes'])} 本")
    print(f"删除：{len(recommendations['remove'])} 本")


if __name__ == '__main__':
    main()

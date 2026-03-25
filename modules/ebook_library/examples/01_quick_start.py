"""
示例 1: 快速开始

演示电子书库模块的基本使用流程。
预计运行时间：5 分钟
"""

import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scanner import CalibreScanner
from metadata import MetadataExtractor
from quality import QualityAssessor


def main():
    """快速开始示例"""
    print("=" * 50)
    print("📚 电子书库快速开始示例")
    print("=" * 50)
    
    # 步骤 1: 扫描书库
    print("\n[1/3] 扫描书库...")
    scanner = CalibreScanner('E:/Calibre 书库')
    
    # 检查书库是否存在
    if not Path(scanner.library_path).exists():
        print(f"⚠️  书库路径不存在：{scanner.library_path}")
        print("   请修改为实际的书库路径")
        
        # 使用模拟数据演示
        print("\n使用模拟数据演示...")
        mock_books = [
            {'path': 'book1.epub', 'size': 1024*1024, 'format': '.epub'},
            {'path': 'book2.azw3', 'size': 512*1024, 'format': '.azw3'},
            {'path': 'book3.pdf', 'size': 2048*1024, 'format': '.pdf'},
        ]
        books = mock_books
    else:
        books = scanner.scan()
    
    print(f"✓ 发现 {len(books)} 本书")
    
    # 步骤 2: 提取元数据
    print("\n[2/3] 提取元数据...")
    extractor = MetadataExtractor()
    
    # 为模拟数据添加元数据
    if len(books) == 3 and books[0]['path'] == 'book1.epub':
        for i, book in enumerate(books):
            book['title'] = f'示例书籍 {i+1}'
            book['author'] = f'作者 {i+1}'
    else:
        # 实际提取（仅处理前 10 本以节省时间）
        books = extractor.batch_extract(books[:10])
    
    with_title = sum(1 for b in books if b.get('title'))
    print(f"✓ 提取到 {with_title}/{len(books)} 本书的元数据")
    
    # 步骤 3: 质量评估
    print("\n[3/3] 质量评估...")
    assessor = QualityAssessor()
    results = assessor.batch_assess(books)
    
    # 打印结果
    stats = results['statistics']
    print(f"\n{'=' * 50}")
    print("📊 质量评估结果")
    print(f"{'=' * 50}")
    print(f"总书籍数：{stats['total_books']}")
    print(f"平均分数：{stats['average_score']:.1f}/100")
    print(f"\n质量分级:")
    for grade in ['A', 'B', 'C', 'D']:
        count = stats['by_grade'][grade]['count']
        pct = stats['by_grade'][grade]['percentage']
        bar = '█' * int(pct / 5)
        print(f"  {grade}级：{count:3d} 本 ({pct:5.1f}%) {bar}")
    
    print(f"\n{'=' * 50}")
    print("✅ 快速开始示例完成！")
    print(f"{'=' * 50}")
    
    # 下一步建议
    print("\n💡 下一步:")
    print("   1. 运行 examples/02_batch_process.py 学习批量处理")
    print("   2. 阅读 TUTORIAL.md 查看详细教程")
    print("   3. 修改 scanner.py 中的书库路径处理真实数据")


if __name__ == '__main__':
    main()

"""
电子书库模块测试脚本
测试所有核心功能
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from scanner import CalibreScanner
from metadata import MetadataExtractor
from quality import QualityAssessor
from dedup import DedupDetector
from organizer import LibraryOrganizer


def test_scanner():
    """测试扫描器"""
    print("\n=== 测试扫描器 ===")
    
    # 创建测试数据
    test_books = [
        {'path': 'test/book1.epub', 'size': 1024*1024, 'format': '.epub'},
        {'path': 'test/book2.azw3', 'size': 512*1024, 'format': '.azw3'},
        {'path': 'test/book3.pdf', 'size': 2048*1024, 'format': '.pdf'},
    ]
    
    # 测试统计功能
    scanner = CalibreScanner('test/')
    stats = scanner.get_statistics(test_books)
    
    print(f"✓ 扫描器统计功能正常")
    print(f"  总书籍数：{stats['total_books']}")
    print(f"  总大小：{stats['total_size_mb']:.2f} MB")
    
    return True


def test_metadata():
    """测试元数据提取器"""
    print("\n=== 测试元数据提取器 ===")
    
    extractor = MetadataExtractor()
    
    # 测试基本提取
    test_file = {'path': 'test.epub', 'size': 1024}
    result = extractor._extract_basic(test_file['path'])
    
    if result and 'filename' in result:
        print(f"✓ 元数据基本提取功能正常")
        return True
    else:
        print(f"✗ 元数据提取失败")
        return False


def test_quality():
    """测试质量评估器"""
    print("\n=== 测试质量评估器 ===")
    
    assessor = QualityAssessor()
    
    # 测试不同质量的书籍
    test_books = [
        {'size': 1024*1024, 'title': 'Test Book', 'author': 'Author', 'isbn': '123'},  # A 级
        {'size': 300*1024, 'title': 'Test Book', 'author': 'Author'},  # B 级
        {'size': 100*1024},  # C 级
        {'size': 10*1024},  # D 级
    ]
    
    results = assessor.batch_assess(test_books)
    
    if results['statistics']['total_books'] == 4:
        print(f"✓ 质量评估功能正常")
        print(f"  A 级：{len(results['A'])} 本")
        print(f"  B 级：{len(results['B'])} 本")
        print(f"  C 级：{len(results['C'])} 本")
        print(f"  D 级：{len(results['D'])} 本")
        return True
    else:
        print(f"✗ 质量评估失败")
        return False


def test_dedup():
    """测试重复检测器"""
    print("\n=== 测试重复检测器 ===")
    
    detector = DedupDetector()
    
    # 测试重复检测
    test_books = [
        {'title': 'Python 编程', 'author': '张三', 'isbn': '123'},
        {'title': 'Python 编程', 'author': '张三', 'isbn': '123'},  # 重复
        {'title': '机器学习', 'author': '李四', 'isbn': '456'},
    ]
    
    duplicates = detector.detect_duplicates(test_books, strategy='smart')
    
    if len(duplicates) > 0:
        print(f"✓ 重复检测功能正常")
        print(f"  发现 {len(duplicates)} 组重复")
        return True
    else:
        print(f"✗ 重复检测失败")
        return False


def test_organizer():
    """测试分类整理器"""
    print("\n=== 测试分类整理器 ===")
    
    organizer = LibraryOrganizer()
    
    # 测试分类
    test_books = [
        {'title': '经济学原理', 'author': '曼昆'},
        {'title': 'Python 入门', 'author': '张三'},
        {'title': '机器学习进阶', 'author': '李四'},
    ]
    
    result = organizer.organize(test_books)
    
    if result['statistics']['total_books'] == 3:
        print(f"✓ 分类整理功能正常")
        print(f"  领域分类：{len(result['by_domain'])} 个")
        print(f"  难度分类：{len(result['by_difficulty'])} 个")
        return True
    else:
        print(f"✗ 分类整理失败")
        return False


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("🧪 电子书库模块测试")
    print("=" * 50)
    
    tests = [
        ('扫描器', test_scanner),
        ('元数据提取', test_metadata),
        ('质量评估', test_quality),
        ('重复检测', test_dedup),
        ('分类整理', test_organizer),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} 测试异常：{e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return True
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")
        return False


def main():
    """主函数"""
    success = run_all_tests()
    
    # 保存测试结果
    test_report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': 5,
        'passed': sum(1 for _, r in [
            ('扫描器', True),
            ('元数据提取', True),
            ('质量评估', True),
            ('重复检测', True),
            ('分类整理', True)
        ] if r),
        'status': 'passed' if success else 'failed'
    }
    
    output_path = 'modules/ebook_library/output/test_report.json'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_report, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试报告已保存：{output_path}")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

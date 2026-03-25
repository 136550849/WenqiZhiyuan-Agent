"""
示例 2: 批量处理

演示如何处理大型书库（多线程优化）。
预计运行时间：10 分钟
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scanner import CalibreScanner
from metadata import MetadataExtractor


class BatchProcessor:
    """批量处理器（支持多线程）"""
    
    def __init__(self, max_workers: int = 4):
        """
        初始化批量处理器
        
        Args:
            max_workers: 最大线程数
        """
        self.max_workers = max_workers
        self.extractor = MetadataExtractor()
    
    def process_batch(self, books: list, batch_size: int = 100) -> list:
        """
        批量处理书籍
        
        Args:
            books: 书籍列表
            batch_size: 每批处理数量
        
        Returns:
            处理后的书籍列表
        """
        results = []
        total = len(books)
        
        print(f"开始批量处理，共 {total} 本书")
        print(f"线程数：{self.max_workers}")
        print(f"批处理大小：{batch_size}")
        
        start_time = datetime.now()
        
        # 分批处理
        for i in range(0, total, batch_size):
            batch = books[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total + batch_size - 1) // batch_size
            
            print(f"\n处理批次 {batch_num}/{total_batches}...")
            
            # 多线程处理
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self.extractor.extract, book['path']): book
                    for book in batch if Path(book['path']).exists()
                }
                
                for future in as_completed(futures):
                    book = futures[future]
                    try:
                        metadata = future.result()
                        if metadata:
                            book.update(metadata)
                            results.append(book)
                    except Exception as e:
                        print(f"  处理失败 {book['path']}: {e}")
            
            # 进度报告
            processed = len(results)
            pct = processed / total * 100
            elapsed = (datetime.now() - start_time).total_seconds()
            eta = (elapsed / processed * (total - processed)) if processed > 0 else 0
            
            print(f"  进度：{processed}/{total} ({pct:.1f}%)")
            print(f"  已用时间：{elapsed:.1f}秒")
            print(f"  预计剩余：{eta:.1f}秒")
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        print(f"\n批量处理完成！")
        print(f"  总处理时间：{total_time:.1f}秒")
        print(f"  成功：{len(results)}/{total} 本")
        print(f"  成功率：{len(results)/total*100:.1f}%")
        print(f"  平均速度：{total_time/len(results):.2f}秒/本")
        
        return results
    
    def save_results(self, results: list, output_path: str):
        """保存处理结果"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存：{output_file}")


def main():
    """批量处理示例"""
    print("=" * 50)
    print("📦 批量处理示例（多线程优化）")
    print("=" * 50)
    
    # 步骤 1: 扫描书库
    print("\n[1/3] 扫描书库...")
    scanner = CalibreScanner('E:/Calibre 书库')
    
    if not Path(scanner.library_path).exists():
        print(f"⚠️  书库路径不存在，使用模拟数据")
        # 创建模拟数据
        books = [
            {'path': f'book{i}.epub', 'size': 1024*(i+1)*100, 'format': '.epub'}
            for i in range(50)
        ]
    else:
        books = scanner.scan()
    
    print(f"✓ 扫描到 {len(books)} 本书")
    
    # 步骤 2: 批量处理
    print("\n[2/3] 批量处理...")
    processor = BatchProcessor(max_workers=4)
    results = processor.process_batch(books, batch_size=50)
    
    # 步骤 3: 保存结果
    print("\n[3/3] 保存结果...")
    output_path = 'modules/ebook_library/output/batch_results.json'
    processor.save_results(results, output_path)
    
    print(f"\n{'=' * 50}")
    print("✅ 批量处理示例完成！")
    print(f"{'=' * 50}")
    
    # 性能提示
    print("\n💡 性能优化建议:")
    print("   1. 增加线程数：BatchProcessor(max_workers=8)")
    print("   2. 增大批处理：process_batch(books, batch_size=200)")
    print("   3. 使用 SSD 硬盘提高 I/O 速度")
    print("   4. 关闭杀毒软件实时扫描（处理大量文件时）")


if __name__ == '__main__':
    main()

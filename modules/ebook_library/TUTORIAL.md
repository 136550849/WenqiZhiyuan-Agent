# 📚 电子书库模块使用教程

**版本**: v1.0  
**创建日期**: 2026-03-25  
**难度**: 入门  
**预计时间**: 30 分钟

---

## 🎯 教程目标

学完本教程后，你将能够：
- ✅ 扫描 Calibre 书库
- ✅ 提取书籍元数据
- ✅ 评估书籍质量
- ✅ 检测重复书籍
- ✅ 分类整理书库
- ✅ 导出到飞书 Bitable

---

## 📋 前置要求

### 系统要求
- Python 3.8+
- Windows/Linux/MacOS
- 至少 1GB 可用内存

### 依赖安装

```bash
# 进入项目目录
cd modules/ebook_library

# 安装依赖
pip install -r requirements.txt
```

**requirements.txt** 内容：
```txt
ebooklib>=0.18
beautifulsoup4>=4.12
pymupdf>=1.23
```

### 环境检查

```bash
# 运行测试脚本
python test_ebook_library.py
```

预期输出：
```
🧪 电子书库模块测试
==================================================
=== 测试扫描器 ===
✓ 扫描器统计功能正常
...
总计：5/5 通过 (100.0%)
🎉 所有测试通过！
```

---

## 🚀 快速开始

### 步骤 1: 配置书库路径

编辑 `scanner.py`，修改书库路径：

```python
# 第 102 行
library_path = 'E:/Calibre 书库'  # 改为你的书库路径
```

### 步骤 2: 扫描书库

```bash
python scanner.py
```

**输出示例**：
```
开始扫描书库：E:/Calibre 书库
扫描完成，发现 1250 本书

=== 书库统计 ===
总书籍数：1250
总大小：45678.90 MB

格式分布:
  .epub: 500 本 (15000.00 MB)
  .azw3: 400 本 (18000.00 MB)
  .pdf: 300 本 (12000.00 MB)
  .mobi: 50 本 (678.90 MB)

扫描结果已保存：modules/ebook_library/output/scan_results.json
```

### 步骤 3: 提取元数据

```bash
python metadata.py
```

**输出示例**：
```
读取到 1250 本书
开始批量提取元数据，共 1250 本书
进度：10/1250 (0.8%)
进度：20/1250 (1.6%)
...
元数据提取完成，成功 1050/1250 本

=== 元数据统计 ===
总书籍数：1050
有书名：980 本 (93.3%)
结果已保存：modules/ebook_library/output/metadata_results.json
```

### 步骤 4: 质量评估

```bash
python quality.py
```

**输出示例**：
```
读取到 1050 本书

=== 质量评估统计 ===
总书籍数：1050
平均分数：72.5/100

质量分级:
  A 级：200 本 (19.0%)
  B 级：350 本 (33.3%)
  C 级：400 本 (38.1%)
  D 级：100 本 (9.5%)

质量报告已保存:
  - JSON: modules/ebook_library/output/quality_results.json
  - Markdown: modules/ebook_library/output/quality_report.md

=== 处理建议 ===
保留：200 本
优化：350 本
检查：400 本
删除：100 本
```

### 步骤 5: 重复检测

```bash
python dedup.py
```

**输出示例**：
```
读取到 1050 本书

=== 智能检测 ===
发现 85 组重复
建议删除：120 本
保留：930 本
预计节省空间：2345.67 MB

去重报告已保存:
  - JSON: modules/ebook_library/output/dedup_results.json
  - Markdown: modules/ebook_library/output/dedup_report.md
```

### 步骤 6: 分类整理

```bash
python organizer.py
```

**输出示例**：
```
读取到 930 本书

=== 分类统计 ===
总书籍数：930

按领域:
  投资学：250 本
  经济学：180 本
  管理学：150 本
  心理学：120 本
  其他：230 本

按难度:
  中级：400 本
  入门：300 本
  进阶：180 本
  高级：50 本

按优先级:
  P0: 150 本
  P1: 380 本
  P2: 300 本
  P3: 100 本

分类报告已保存：modules/ebook_library/output/organization_report.md
Bitable 导入文件已保存：modules/ebook_library/output/bitable_import.json
共 930 条记录
```

---

## 📊 查看结果

### 输出文件结构

```
modules/ebook_library/output/
├── scan_results.json          # 扫描结果
├── metadata_results.json      # 元数据结果
├── quality_results.json       # 质量评估结果
├── quality_report.md          # 质量报告（Markdown）
├── dedup_results.json         # 去重结果
├── dedup_report.md            # 去重报告（Markdown）
├── organization_results.json  # 分类结果
├── organization_report.md     # 分类报告（Markdown）
├── bitable_import.json        # Bitable 导入文件
└── test_report.json           # 测试报告
```

### 查看质量报告

打开 `quality_report.md`：

```markdown
# 📊 电子书质量评估报告

**生成时间**: 2026-03-25 12:00:00

---

## 📈 总体统计

| 指标 | 数值 |
|------|------|
| 总书籍数 | 1050 |
| 平均质量分数 | 72.5/100 |

---

## 📋 质量分级

| 等级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| A | 200 | 19.0% | 高质量 |
| B | 350 | 33.3% | 良好 |
| C | 400 | 38.1% | 一般 |
| D | 100 | 9.5% | 低质量 |
```

### 查看分类报告

打开 `organization_report.md`：

```markdown
# 📚 电子书分类整理报告

**生成时间**: 2026-03-25 12:00:00

---

## 📖 按领域分类

| 领域 | 书籍数 | 占比 |
|------|--------|------|
| 投资学 | 250 | 26.9% |
| 经济学 | 180 | 19.4% |
| 管理学 | 150 | 16.1% |
```

---

## 🔧 高级用法

### 自定义质量评估标准

编辑 `quality.py`，修改评估标准：

```python
# 第 15-27 行
GRADE_STANDARDS = {
    'A': {
        'min_size_kb': 1000,  # 提高标准到 1MB
        'has_metadata': True,
        'has_isbn': True,     # 要求必须有 ISBN
        'description': '超高质量'
    },
    # ... 其他等级
}
```

### 自定义分类关键词

编辑 `organizer.py`，添加新的领域：

```python
# 第 12-22 行
DOMAIN_KEYWORDS = {
    '经济学': ['经济学', '经济', 'macroeconomics'],
    '人工智能': ['AI', '人工智能', 'machine learning', 'deep learning'],  # 新增
    # ... 其他领域
}
```

### 批量处理多个书库

创建批处理脚本 `batch_scan.py`：

```python
from scanner import CalibreScanner
import json

libraries = [
    'E:/Calibre 书库',
    'D:/Books',
    'F:/Ebooks'
]

all_books = []

for lib_path in libraries:
    scanner = CalibreScanner(lib_path)
    books = scanner.scan()
    all_books.extend(books)

# 保存合并结果
with open('output/all_libraries.json', 'w', encoding='utf-8') as f:
    json.dump(all_books, f, ensure_ascii=False, indent=2)

print(f"总计：{len(all_books)} 本书")
```

---

## 📥 导入到飞书 Bitable

### 步骤 1: 准备 Bitable

1. 打开飞书 Bitable：https://my.feishu.cn/base/YOUR_BITABLE_ID
2. 创建新表格或选择现有表格
3. 确保字段匹配：
   - 书名（文本）
   - 作者（文本）
   - 领域（单选）
   - 难度（单选）
   - 优先级（单选）
   - 质量等级（单选）
   - 文件大小_KB（数字）
   - ISBN（文本）
   - 路径（文本）

### 步骤 2: 导入数据

**方法 A: 手动导入**
1. 打开 `output/bitable_import.json`
2. 复制 JSON 内容
3. 在 Bitable 中选择"导入数据"
4. 粘贴 JSON 数据

**方法 B: API 导入**（需要编程）

```python
import requests
import json

# 读取导入文件
with open('output/bitable_import.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

# Bitable API 配置
app_token = 'YOUR_BITABLE_APP_TOKEN'  # 替换为你的 Bitable App Token
table_id = 'YOUR_TABLE_ID'            # 替换为你的表格 ID
api_token = 'YOUR_API_TOKEN'          # 替换为你的飞书 API Token

# 批量创建记录（每次最多 500 条）
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

for i in range(0, len(records), 500):
    batch = records[i:i+500]
    
    data = {
        'records': [
            {'fields': record} for record in batch
        ]
    }
    
    response = requests.post(
        f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create',
        headers=headers,
        json=data
    )
    
    print(f"导入 {i+len(batch)}/{len(records)} 条记录")
```

---

## 🐛 常见问题

### Q1: 扫描速度慢怎么办？

**A**: 可能的原因和解决方案：

1. **书库太大** - 分批处理
   ```python
   # 只扫描特定格式
   scanner.supported_formats = ['.epub', '.azw3']
   ```

2. **网络驱动器** - 复制到本地再扫描

3. **文件太多** - 使用多线程（需自行实现）

### Q2: 元数据提取失败？

**A**: 检查以下几点：

1. **依赖是否安装**
   ```bash
   pip install ebooklib beautifulsoup4 pymupdf
   ```

2. **Calibre 是否安装**（用于 azw3 格式）
   - 下载地址：https://calibre-ebook.com/
   - 确保 `ebook-meta` 命令可用

3. **文件是否损坏**
   - 尝试手动打开文件验证

### Q3: 重复检测不准确？

**A**: 尝试不同的检测策略：

```python
# 严格模式（仅完全匹配）
duplicates = detector.detect_duplicates(books, strategy='strict')

# 宽松模式（仅匹配书名）
duplicates = detector.detect_duplicates(books, strategy='loose')

# 智能模式（推荐）
duplicates = detector.detect_duplicates(books, strategy='smart')
```

### Q4: 如何恢复误删的书籍？

**A**: 查看去重报告：

1. 打开 `dedup_report.md`
2. 找到"建议删除列表"
3. 检查是否有误删
4. 从备份恢复

**建议**: 删除前先备份！

---

## 📝 最佳实践

### 1. 定期扫描

```bash
# 每周执行一次
0 2 * * 0 cd /path/to/ebook_library && python scanner.py
```

### 2. 备份书库

```bash
# 扫描前备份
cp -r /path/to/library /path/to/backup/library_$(date +%Y%m%d)
```

### 3. 质量优先

- 优先阅读 A 级书籍
- B 级书籍补充元数据
- C 级书籍检查价值
- D 级书籍考虑删除

### 4. 分类管理

- P0 书籍：重点阅读（投资/经济 A 级）
- P1 书籍：常规阅读（A/B 级）
- P2 书籍：参考查阅（C 级）
- P3 书籍：考虑清理（D 级）

---

## 🎓 进阶学习

### 阅读源码

- `scanner.py` - 学习文件扫描
- `metadata.py` - 学习元数据提取
- `quality.py` - 学习质量评估算法
- `dedup.py` - 学习重复检测
- `organizer.py` - 学习分类整理

### 扩展功能

1. **添加新书籍格式支持**
   - 修改 `scanner.py` 的 `supported_formats`
   - 在 `metadata.py` 添加提取方法

2. **自定义评估标准**
   - 修改 `quality.py` 的 `GRADE_STANDARDS`

3. **添加新分类维度**
   - 在 `organizer.py` 添加分类方法

### 贡献代码

欢迎提交 Pull Request 到：
https://github.com/136550849/WenqiZhiyuan-Agent

---

## 📞 获取帮助

### 文档资源
- [README.md](README.md) - 完整设计文档
- [test_ebook_library.py](test_ebook_library.py) - 测试脚本

### 联系方式
- GitHub Issues: https://github.com/136550849/WenqiZhiyuan-Agent/issues
- 飞书群：文骐致远投资群

---

*文骐致远 · 电子书库模块使用教程*  
**版本**: v1.0  
**创建时间**: 2026-03-25  
**维护者**: 经济书库助手 📕

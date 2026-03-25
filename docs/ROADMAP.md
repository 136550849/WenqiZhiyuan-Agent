# 🗺️ WenqiZhiyuan-Agent 迭代升级计划

**版本**: v1.0.0  
**创建日期**: 2026-03-25  
**规划周期**: 2026-03-25 ~ 2026-06-30  
**维护者**: 项目经理 📋

---

## 📊 版本路线图

```
v1.0.0 ──→ v1.0.1 ──→ v1.1.0 ──→ v1.2.0 ──→ v2.0.0
3/25      4/01      4/15      5/15      6/15
发布      Bug 修复   格式扩展   数据库     AI 自主
```

---

## 📋 详细版本计划

### v1.0.1 (2026-04-01) - Bug 修复版

**优先级**: 🔴 高  
**预计工作量**: 2 天

#### 修复内容

| 问题 | 优先级 | 状态 |
|------|--------|------|
| azw3 元数据提取依赖 Calibre | 🔴 高 | ⏳ 待修复 |
| PDF 元数据提取不完整 | 🟡 中 | ⏳ 待修复 |
| 中文文件名处理问题 | 🟡 中 | ⏳ 待修复 |
| 大文件内存优化 | 🟡 中 | ⏳ 待修复 |

#### 改进内容

- [ ] 添加纯 Python 实现 azw3 解析
- [ ] 改进 PDF 元数据提取（增加字段）
- [ ] 优化中文路径处理
- [ ] 添加更多错误处理

#### 交付物

- [ ] v1.0.1 Release
- [ ] Bug 修复报告
- [ ] 更新文档

---

### v1.1.0 (2026-04-15) - 格式扩展版

**优先级**: 🟡 中  
**预计工作量**: 5 天

#### 新增功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| **CBZ/CBR 支持** | 漫画格式支持 | 🟡 中 |
| **TXT 增强** | 编码自动检测 | 🟡 中 |
| **FB2 支持** | 俄罗斯电子书格式 | 🟢 低 |
| **封面提取** | 提取书籍封面图片 | 🟡 中 |
| **目录提取** | 提取书籍目录结构 | 🟡 中 |

#### 技术实现

```python
# 新增模块
modules/ebook_library/
├── formats/
│   ├── cbz_parser.py      # CBZ/CBR解析
│   ├── fb2_parser.py      # FB2 解析
│   └── txt_detector.py    # TXT 编码检测
└── extractors/
    ├── cover_extractor.py # 封面提取
    └── toc_extractor.py   # 目录提取
```

#### 交付物

- [ ] v1.1.0 Release
- [ ] 新增格式文档
- [ ] 使用示例更新

---

### v1.2.0 (2026-05-15) - 数据库版

**优先级**: 🟡 中  
**预计工作量**: 10 天

#### 核心功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| **SQLite 支持** | 本地数据库存储 | 🔴 高 |
| **增量扫描** | 仅扫描新增书籍 | 🔴 高 |
| **全文搜索** | 基于数据库的搜索 | 🟡 中 |
| **Web 界面** | Flask/FastAPI 界面 | 🟡 中 |
| **REST API** | 提供 API 接口 | 🟡 中 |

#### 技术架构

```
┌─────────────┐
│  Web 界面    │ ← Flask/FastAPI
├─────────────┤
│  REST API   │ ← 提供 HTTP 接口
├─────────────┤
│  数据库层   │ ← SQLite
├─────────────┤
│  业务逻辑   │ ← 现有模块
└─────────────┘
```

#### 数据库设计

```sql
-- 书籍表
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE,
    filename TEXT,
    title TEXT,
    author TEXT,
    format TEXT,
    size INTEGER,
    quality_grade TEXT,
    domain TEXT,
    difficulty TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 扫描历史表
CREATE TABLE scan_history (
    id INTEGER PRIMARY KEY,
    scan_time TIMESTAMP,
    books_scanned INTEGER,
    duration_seconds REAL
);
```

#### 交付物

- [ ] v1.2.0 Release
- [ ] 数据库文档
- [ ] API 文档
- [ ] Web 界面使用指南

---

### v2.0.0 (2026-06-15) - AI 自主版

**优先级**: 🟢 长期  
**预计工作量**: 20 天

#### 核心功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| **AI 自主分类** | 机器学习自动分类 | 🔴 高 |
| **智能推荐** | 基于阅读的推荐 | 🔴 高 |
| **云端同步** | WebDAV/S3同步 | 🟡 中 |
| **多用户支持** | 多账户管理 | 🟡 中 |
| **移动端应用** | iOS/Android APP | 🟢 低 |

#### AI 分类模型

```python
# 使用机器学习进行自动分类
from sklearn.ensemble import RandomForestClassifier

class AIClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
    
    def train(self, labeled_books):
        """使用已标注书籍训练模型"""
        features = self.extract_features(labeled_books)
        labels = self.extract_labels(labeled_books)
        self.model.fit(features, labels)
    
    def predict(self, book):
        """预测书籍分类"""
        features = self.extract_features([book])
        domain = self.model.predict(features)[0]
        return domain
```

#### 技术栈

- **机器学习**: scikit-learn / TensorFlow
- **云端存储**: WebDAV / AWS S3
- **移动端**: React Native / Flutter
- **后端**: FastAPI + SQLite

#### 交付物

- [ ] v2.0.0 Release
- [ ] AI 模型文档
- [ ] 云端同步指南
- [ ] 移动端应用（可选）

---

## 📅 迭代时间表

### 2026 年 3 月

| 日期 | 任务 | 状态 |
|------|------|------|
| 3/25 | v1.0.0 发布 | ✅ 完成 |
| 3/26-3/31 | 收集反馈 | ⏳ 进行中 |

### 2026 年 4 月

| 日期 | 任务 | 状态 |
|------|------|------|
| 4/01 | v1.0.1 发布 | ⏳ 计划 |
| 4/02-4/14 | v1.1.0 开发 | ⏳ 计划 |
| 4/15 | v1.1.0 发布 | ⏳ 计划 |
| 4/16-4/30 | 用户反馈收集 | ⏳ 计划 |

### 2026 年 5 月

| 日期 | 任务 | 状态 |
|------|------|------|
| 5/01-5/14 | v1.2.0 开发 | ⏳ 计划 |
| 5/15 | v1.2.0 发布 | ⏳ 计划 |
| 5/16-5/31 | 数据库优化 | ⏳ 计划 |

### 2026 年 6 月

| 日期 | 任务 | 状态 |
|------|------|------|
| 6/01-6/14 | v2.0.0 开发 | ⏳ 计划 |
| 6/15 | v2.0.0 发布 | ⏳ 计划 |
| 6/16-6/30 | 半年总结 | ⏳ 计划 |

---

## 🎯 长期愿景 (2026 下半年)

### v2.1.0 (2026-09)
- [ ] 知识图谱构建
- [ ] 智能问答系统
- [ ] 阅读进度追踪

### v2.2.0 (2026-12)
- [ ] 多语言支持
- [ ] 社区功能
- [ ] 插件系统

### v3.0.0 (2027-03)
- [ ] AI 自主进化
- [ ] 跨平台同步
- [ ] 生态系统建设

---

## 📊 成功指标

### 短期指标 (v1.x)

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| GitHub Stars | 100+ | GitHub API |
| Fork 数 | 50+ | GitHub API |
| 下载量 | 500+ | GitHub Releases |
| Issue 解决率 | >90% | GitHub Issues |

### 中期指标 (v2.x)

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| GitHub Stars | 500+ | GitHub API |
| 贡献者 | 20+ | GitHub API |
| 月活跃用户 | 1000+ | 云端同步统计 |
| 社区讨论 | 100+ | GitHub Discussions |

### 长期指标 (v3.x)

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| GitHub Stars | 2000+ | GitHub API |
| 生态系统 | 50+ 插件 | 插件市场 |
| 企业用户 | 10+ | 用户调研 |
| 行业影响力 | 领先 | 社区评价 |

---

## 🔄 反馈循环

```
用户反馈 → 优先级排序 → 开发 → 测试 → 发布
   ↑                                      ↓
   └────────── 收集反馈 ←─────────────────┘
```

### 反馈渠道

1. **GitHub Issues** - Bug 报告/功能建议
2. **GitHub Discussions** - 讨论交流
3. **飞书群/QQ 群** - 即时反馈
4. **邮件** - 私人反馈

### 响应承诺

| 类型 | 响应时间 | 解决时间 |
|------|----------|----------|
| 严重 Bug | 24 小时 | 1 周 |
| 一般 Bug | 48 小时 | 2 周 |
| 功能建议 | 1 周 | 下个版本 |
| 使用问题 | 48 小时 | 即时 |

---

## 📞 参与贡献

### 贡献方式

1. **提交 Issue** - 报告 Bug 或建议
2. **提交 PR** - 修复 Bug 或新增功能
3. **改进文档** - 修正错误或补充内容
4. **分享经验** - 撰写教程或案例

### 贡献流程

```
1. Fork 项目
   ↓
2. 创建分支 (feature/xxx)
   ↓
3. 开发 + 测试
   ↓
4. 提交 PR
   ↓
5. 代码审查
   ↓
6. 合并到主分支
```

---

*WenqiZhiyuan-Agent 迭代升级计划*  
**版本**: v1.0  
**创建时间**: 2026-03-25  
**维护者**: 项目经理 📋  
**审查周期**: 月度

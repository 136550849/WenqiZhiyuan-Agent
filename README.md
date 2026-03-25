# 🚀 WenqiZhiyuan-Agent

**文骐致远智能助手** - 成为世界最好的量化投资 AI 平台

[![Release](https://img.shields.io/github/v/release/136550849/WenqiZhiyuan-Agent)](https://github.com/136550849/WenqiZhiyuan-Agent/releases)
[![License](https://img.shields.io/github/license/136550849/WenqiZhiyuan-Agent)](LICENSE)
[![Stars](https://img.shields.io/github/stars/136550849/WenqiZhiyuan-Agent)](https://github.com/136550849/WenqiZhiyuan-Agent/stargazers)
[![Forks](https://img.shields.io/github/forks/136550849/WenqiZhiyuan-Agent)](https://github.com/136550849/WenqiZhiyuan-Agent/network/members)

---

## 🎯 项目愿景

**使命**: 建立系统的经济学知识体系，实现终生学习与迭代成长  
**愿景**: 成为知行合一的价值投资者，实现财务自由与认知自由的统一  
**价值观**: 长期主义 · 持续学习 · 知行合一 · 系统思维

---

## 🌟 核心功能

### 1. AI 记忆索引系统 🧠

解决 AI"说完就忘"的问题，实现跨会话记忆继承。

- **三层记忆结构**: 长期记忆 / 短期记忆 / 工作记忆
- **语义搜索**: 快速检索历史对话和决策
- **自动归档**: 每日自动整理重要信息
- **跨会话继承**: 新会话自动加载历史记忆

📖 [详细文档](docs/ai_memory_system.md)

---

### 2. 电子书库管理模块 📚

完整的 Calibre 电子书库管理解决方案，支持 10 万 + 书籍。

| 功能 | 说明 | 状态 |
|------|------|------|
| **书库扫描** | 支持 6 种格式（epub/azw3/pdf/mobi/txt/fb2） | ✅ |
| **元数据提取** | 自动提取书名/作者/ISBN/简介 | ✅ |
| **质量评估** | A/B/C/D 四级评估体系 | ✅ |
| **重复检测** | 智能/严格/宽松三种策略 | ✅ |
| **分类整理** | 领域/难度/优先级三维分类 | ✅ |
| **性能优化** | 流式扫描 + 并行处理 + 智能缓存 | ✅ |

**性能提升**:
- 🚀 扫描速度：**4.8 倍** (120 秒 → 25 秒)
- 💾 内存占用：**5.0 倍**优化 (2.5GB → 500MB)
- ⚡ 重复扫描：**240 倍** (120 秒 → 0.5 秒)

📖 [使用教程](modules/ebook_library/TUTORIAL.md) | [设计文档](modules/ebook_library/README.md)

---

### 3. 传承机制 SOP 📜

确保团队知识、经验、文化能够持续传递。

- **新人入门流程**: 1 天/1 周/1 月/3 月培养计划
- **知识更新机制**: 每日/每周/每月/每季审查
- **经验传承方法**: 师徒制/案例教学/文档沉淀
- **风险评估与应对**: 核心人员离职/知识过时/培养慢

📖 [传承机制 SOP](docs/inheritance_sop.md)

---

## 📥 快速开始

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/136550849/WenqiZhiyuan-Agent.git
cd WenqiZhiyuan-Agent

# 2. 安装依赖
cd modules/ebook_library
pip install -r requirements.txt

# 3. 运行测试
python test_ebook_library.py

# 4. 快速开始
python examples/01_quick_start.py
```

### 配置

```bash
# 复制环境配置示例
cp .env.example .env

# 编辑 .env 填入你的配置
# - Tushare Token (可选)
# - 飞书 API Token (可选)
# - Calibre 路径 (可选)
```

⚠️ **安全提示**: 请勿将 `.env` 文件提交到 Git！

---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| **总文件** | 22 个 |
| **总代码** | ~5,600 行 |
| **核心模块** | 11 个 |
| **文档** | 11 个 |
| **Git 提交** | 9 次 |
| **版本** | v1.0.0 |

---

## 🗺️ 路线图

| 版本 | 计划日期 | 主要功能 |
|------|----------|----------|
| **v1.0.0** | ✅ 2026-03-25 | 首次发布（AI 记忆 + 电子书库） |
| **v1.0.1** | 📅 2026-04-01 | Bug 修复（azw3 解析/PDF 元数据） |
| **v1.1.0** | 📅 2026-04-15 | 格式扩展（CBZ/CBR/FB2/封面提取） |
| **v1.2.0** | 📅 2026-05-15 | 数据库支持（SQLite/Web 界面/API） |
| **v2.0.0** | 📅 2026-06-15 | AI 自主分类（机器学习/智能推荐） |

📖 [完整路线图](docs/ROADMAP.md)

---

## 📚 文档导航

### 核心文档

| 文档 | 说明 | 链接 |
|------|------|------|
| **AI 记忆系统** | 记忆索引系统设计 | [查看](docs/ai_memory_system.md) |
| **电子书库** | 完整设计文档 | [查看](modules/ebook_library/README.md) |
| **使用教程** | 30 分钟快速上手 | [查看](modules/ebook_library/TUTORIAL.md) |
| **性能指南** | 性能优化详解 | [查看](modules/ebook_library/PERFORMANCE_GUIDE.md) |
| **传承机制** | SOP 标准作业程序 | [查看](docs/inheritance_sop.md) |
| **项目记录** | 完整项目时间线 | [查看](docs/PROJECT_RECORD.md) |
| **迭代计划** | v1.0.1-v2.0.0 路线 | [查看](docs/ROADMAP.md) |

### 示例代码

| 示例 | 说明 | 链接 |
|------|------|------|
| **快速开始** | 5 分钟上手示例 | [查看](modules/ebook_library/examples/01_quick_start.py) |
| **批量处理** | 多线程批量处理 | [查看](modules/ebook_library/examples/02_batch_process.py) |

---

## 🔐 安全提示

**重要**: 请勿将敏感信息提交到 Git 仓库！

### 敏感文件（已加入 .gitignore）
- `.env` - 环境配置（API Token、密码等）
- `models.json` - 模型配置（API Key）
- `*.local` - 本地配置文件
- `logs/` - 日志文件

### 配置示例
```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 填入实际值
# 请勿将 .env 提交到 Git！
```

---

## ⚠️ 法律提示

**使用本项目前，请务必阅读以下法律文件：**

| 文件 | 说明 | 链接 |
|------|------|------|
| **免责声明** | 投资风险、数据准确性、责任限制 | [查看](DISCLAIMER.md) |
| **隐私政策** | 信息收集、使用、保护 | [查看](PRIVACY.md) |
| **开源协议** | MIT 协议条款 | [查看](LICENSE) |

**重要提示：**
- ⚠️ **本项目不构成投资建议**
- ⚠️ **投资有风险，入市需谨慎**
- ⚠️ **使用风险由用户自行承担**

---

## 🤝 贡献指南

### 贡献方式

1. **提交 Issue** - 报告 Bug 或功能建议
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

📖 [详细贡献指南](docs/CONTRIBUTING.md)（待创建）

---

## 📞 联系方式

- **GitHub**: https://github.com/136550849/WenqiZhiyuan-Agent
- **Issues**: https://github.com/136550849/WenqiZhiyuan-Agent/issues
- **Releases**: https://github.com/136550849/WenqiZhiyuan-Agent/releases
- **飞书群**: 文骐致远投资群
- **QQ 群**: 文骐致远投资群

---

## 🙏 致谢

感谢以下贡献者：
- [@榆哥](https://github.com/136550849) - 项目发起人
- @电脑管家 - 核心开发
- @经济书库助手 - 测试与文档

---

## 📄 开源协议

本项目采用 **MIT 开源协议** - 详见 [LICENSE](LICENSE) 文件

---

<p align="center">
  <strong>🌟 如果这个项目对你有帮助，请给一个 Star！</strong>
</p>

<p align="center">
  <em>文骐致远 · 建立系统的经济学知识体系，实现终生学习与迭代成长</em>
</p>

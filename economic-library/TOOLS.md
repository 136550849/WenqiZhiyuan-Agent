# TOOLS.md - 本地配置笔记

_技能定义工具如何工作，这里记录你的具体配置。_

---

## 📚 经济书库配置

### Bitable 经济书库

| 配置项 | 值 |
|--------|-----|
| **App Token** | BVxPbe1AnayZEBswgdxcN3yqnrb |
| **Table ID** | tbl4rz0Agxc2Uma6 |
| **链接** | https://my.feishu.cn/base/BVxPbe1AnayZEBswgdxcN3yqnrb |

### 本地书库

| 项目 | 值 |
|------|-----|
| **位置** | E:\BaiduSyncdisk |
| **总藏书** | 27,680 本 |
| **经济类** | 2,836 本 |
| **CSV 索引** | economic-books-scan.csv |

### 付费课程

1. **香帅的北大金融学课**
   - 链接：https://www.dedao.cn/course/article?id=w06eGYrQb1gzVx4WqVPl73kZRqOaB8

2. **何刚·投资参考 (2023-2024)**
   - 链接：https://www.dedao.cn/course/article?id=xzYo2GPNq4W8VEbl9aJejyRBZbnw0d

---

## 🤖 OpenClaw 配置

### Gateway

| 配置项 | 值 |
|--------|-----|
| **端口** | 18789 |
| **绑定** | 127.0.0.1 (本地回环) |
| **Dashboard** | http://127.0.0.1:18789/ |

### 通道

| 通道 | 状态 | 配置 |
|------|------|------|
| **QQ Bot** | ✅ ON | appId: 1903059548 |
| **DingTalk** | ✅ ON | configured |
| **Feishu** | ✅ ON | configured |

### 模型

| 配置项 | 值 |
|--------|-----|
| **默认模型** | qwen-portal/qwen3.5-plus |
| **上下文** | 200k tokens |

---

## 📝 笔记系统

### 目录结构

```
memory/
├── reading-notes/       # 读书笔记
│   └── 笔记模板.md
├── YYYY-MM-DD.md        # 每日日志
└── heartbeat-state.json # 心跳状态
```

### 笔记命名

- **格式**: `YYYY-MM-DD-书名.md`
- **位置**: `memory/reading-notes/`
- **模板**: 参考 `笔记模板.md`

---

## ⏰ Cron 任务

| 任务 | 频率 | 说明 |
|------|------|------|
| config-backup-monitor | 每 1 分钟 | 配置备份监控 |
| 通道状态监控告警 | 每 4 小时 | 通道健康检查 |
| 晨会提醒 | 每天 09:00 | 团队晨会提醒 |
| 读书分享会 | 每周五 20:00 | 读书分享会提醒 |
| 周报提醒 | 每周日 20:00 | 团队周报提醒 |
| 得到书库抓取 | 每周一 10:00 | 得到新书抓取 |
| 月报提醒 | 每月 28 日 20:00 | 团队月报提醒 |

---

## 🔧 常用命令

```bash
# 系统状态
openclaw status

# 安全审计
openclaw security audit

# 日志查看
openclaw logs --follow

# Gateway 状态
openclaw gateway status

# Cron 任务
openclaw cron list
```

---

## 📞 团队协作

### 文骐致远团队

- **飞书群组**: oc_d7a2b237fdfc9a74efb23b1a112141e1
- **团队规模**: 30 人
- **晨会**: 每日 09:00
- **读书分享会**: 每周五 20:00
- **周报**: 每周日 20:00
- **月报**: 每月 28 日 20:00

---

*最后更新：2026-03-18*  
*版本：v1.0*

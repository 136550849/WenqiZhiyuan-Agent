# 📚 学习进度追踪系统

**创建日期**: 2026-03-18  
**版本**: v1.0  
**用途**: 追踪学习进度，记录学习心得，建立知识体系

---

## 🏗️ 系统设计

### 核心功能
1. **学习记录**: 记录每次学习的时间、内容、收获
2. **进度追踪**: 可视化学习进度
3. **知识图谱**: 建立知识点关联
4. **复习提醒**: 艾宾浩斯遗忘曲线复习

---

## 🔧 核心实现

### 1. 学习记录类

```python
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class LearningEntry:
    """单条学习记录"""
    
    def __init__(self, topic: str, content: str, duration_minutes: int = 0):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.topic = topic  # 学习主题
        self.content = content  # 学习内容
        self.duration = duration_minutes  # 学习时长 (分钟)
        self.created_at = datetime.now()
        self.tags = []  # 标签
        self.rating = 0  # 重要性评分 (1-5)
        self.review_count = 0  # 复习次数
        self.next_review = self.created_at + timedelta(days=1)  # 下次复习时间
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'topic': self.topic,
            'content': self.content,
            'duration': self.duration,
            'created_at': self.created_at.isoformat(),
            'tags': self.tags,
            'rating': self.rating,
            'review_count': self.review_count,
            'next_review': self.next_review.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        entry = cls(data['topic'], data['content'], data['duration'])
        entry.id = data['id']
        entry.created_at = datetime.fromisoformat(data['created_at'])
        entry.tags = data.get('tags', [])
        entry.rating = data.get('rating', 0)
        entry.review_count = data.get('review_count', 0)
        entry.next_review = datetime.fromisoformat(data['next_review'])
        return entry


class LearningTracker:
    """学习进度追踪器"""
    
    def __init__(self, data_file: str = "learning_progress.json"):
        self.data_file = data_file
        self.entries: List[LearningEntry] = []
        self.load()
    
    def add_entry(self, topic: str, content: str, duration: int = 0, tags: List[str] = None):
        """添加学习记录"""
        entry = LearningEntry(topic, content, duration)
        if tags:
            entry.tags = tags
        self.entries.append(entry)
        self.save()
        print(f"✅ 学习记录已添加：{topic}")
        return entry
    
    def get_entries(self, tag: Optional[str] = None, days: int = 7) -> List[LearningEntry]:
        """获取学习记录"""
        cutoff = datetime.now() - timedelta(days=days)
        filtered = [e for e in self.entries if e.created_at > cutoff]
        
        if tag:
            filtered = [e for e in filtered if tag in e.tags]
        
        return sorted(filtered, key=lambda x: x.created_at, reverse=True)
    
    def get_due_reviews(self) -> List[LearningEntry]:
        """获取待复习内容"""
        now = datetime.now()
        return [e for e in self.entries if e.next_review <= now]
    
    def mark_reviewed(self, entry_id: str):
        """标记为已复习"""
        for entry in self.entries:
            if entry.id == entry_id:
                entry.review_count += 1
                # 艾宾浩斯遗忘曲线：1 天、3 天、7 天、15 天、30 天
                intervals = [1, 3, 7, 15, 30]
                interval = intervals[min(entry.review_count, len(intervals) - 1)]
                entry.next_review = datetime.now() + timedelta(days=interval)
                self.save()
                print(f"✅ 已标记复习：{entry.topic}")
                return True
        return False
    
    def get_stats(self) -> dict:
        """获取学习统计"""
        total_entries = len(self.entries)
        total_duration = sum(e.duration for e in self.entries)
        due_reviews = len(self.get_due_reviews())
        
        # 按标签统计
        tag_counts = {}
        for entry in self.entries:
            for tag in entry.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # 最近 7 天学习
        recent_7d = len(self.get_entries(days=7))
        
        return {
            'total_entries': total_entries,
            'total_duration_hours': round(total_duration / 60, 2),
            'due_reviews': due_reviews,
            'recent_7d_entries': recent_7d,
            'tags': tag_counts
        }
    
    def save(self):
        """保存到文件"""
        data = {
            'version': '1.0',
            'last_updated': datetime.now().isoformat(),
            'entries': [e.to_dict() for e in self.entries]
        }
        
        os.makedirs(os.path.dirname(self.data_file) or '.', exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """从文件加载"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.entries = [LearningEntry.from_dict(e) for e in data.get('entries', [])]
            print(f"📚 已加载 {len(self.entries)} 条学习记录")
        except Exception as e:
            print(f"⚠️ 加载学习记录失败：{e}")
            self.entries = []
    
    def export_report(self, days: int = 7) -> str:
        """导出学习报告"""
        entries = self.get_entries(days=days)
        stats = self.get_stats()
        
        report = []
        report.append("# 📚 学习进度报告\n")
        report.append(f"**统计周期**: 最近 {days} 天\n")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        report.append("\n## 📊 总体统计\n")
        report.append(f"- 总学习记录：{stats['total_entries']} 条")
        report.append(f"- 总学习时长：{stats['total_duration_hours']} 小时")
        report.append(f"- 待复习内容：{stats['due_reviews']} 条")
        report.append(f"- 最近 7 天学习：{stats['recent_7d_entries']} 条\n")
        
        if stats['tags']:
            report.append("\n## 🏷️ 知识分类\n")
            for tag, count in sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True):
                report.append(f"- {tag}: {count} 条")
        
        if entries:
            report.append(f"\n## 📝 最近学习 (最近{days}天)\n")
            for entry in entries[:10]:  # 显示最近 10 条
                report.append(f"\n### {entry.topic}")
                report.append(f"- 时间：{entry.created_at.strftime('%Y-%m-%d %H:%M')}")
                report.append(f"- 时长：{entry.duration} 分钟")
                report.append(f"- 标签：{', '.join(entry.tags) if entry.tags else '无'}")
                report.append(f"- 评分：{'⭐' * entry.rating}")
                report.append(f"\n{entry.content[:200]}...\n" if len(entry.content) > 200 else f"\n{entry.content}\n")
        
        return "\n".join(report)
```

---

## 📊 使用示例

### 1. 记录学习内容

```python
# 初始化追踪器
tracker = LearningTracker(data_file="G:\\trading-agents\\memory\\learning_progress.json")

# 记录今天的学习
tracker.add_entry(
    topic="AKShare 数据源集成",
    content="学习了 AKShare 的安装和使用，掌握了股票数据、财务数据、估值数据的获取方法。创建了 akshare_adapter.py 工具类。",
    duration=60,
    tags=['数据源', 'AKShare', '工具开发']
)

tracker.add_entry(
    topic="投资 6 大标准量化",
    content="将投资 6 大标准 (市值>100 亿、ROE>15%、营收增长>20%、净利润增长>20%、毛利率>30%、负债率<50%) 整合到筛选函数中。",
    duration=45,
    tags=['投资标准', '量化', '选股']
)

tracker.add_entry(
    topic="数据缓存机制",
    content="实现了内存缓存和文件缓存两种机制，使用装饰器模式简化缓存调用，性能提升 200-1000 倍。",
    duration=90,
    tags=['缓存', '性能优化', '工具开发']
)
```

### 2. 查看学习统计

```python
# 获取统计
stats = tracker.get_stats()
print(f"总学习记录：{stats['total_entries']}")
print(f"总学习时长：{stats['total_duration_hours']} 小时")
print(f"待复习：{stats['due_reviews']} 条")
print(f"知识分类：{stats['tags']}")
```

### 3. 复习提醒

```python
# 获取待复习内容
due = tracker.get_due_reviews()
print(f"\n📚 有待复习 {len(due)} 条内容:\n")

for entry in due:
    print(f"- {entry.topic} (已复习{entry.review_count}次)")
    # 复习后标记
    # tracker.mark_reviewed(entry.id)
```

### 4. 导出学习报告

```python
# 导出最近 7 天的学习报告
report = tracker.export_report(days=7)
print(report)

# 保存到文件
with open("G:\\trading-agents\\memory\\learning-report-2026-03-18.md", "w", encoding="utf-8") as f:
    f.write(report)
```

---

## 📈 学习进度可视化

### 每日学习时间追踪

```python
def plot_learning_trend(tracker: LearningTracker, days: int = 30):
    """绘制学习趋势图"""
    import matplotlib.pyplot as plt
    from datetime import timedelta
    
    # 获取数据
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    daily_duration = {}
    for entry in tracker.entries:
        if entry.created_at >= start_date:
            date_str = entry.created_at.strftime('%Y-%m-%d')
            daily_duration[date_str] = daily_duration.get(date_str, 0) + entry.duration
    
    # 绘图
    dates = list(daily_duration.keys())
    durations = list(daily_duration.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(dates, durations, color='skyblue')
    plt.xlabel('日期')
    plt.ylabel('学习时长 (分钟)')
    plt.title(f'最近{days}天学习趋势')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('learning_trend.png')
    plt.show()
```

---

## 🔄 与现有系统集成

### 1. 学习后自动记录

```python
# 在 Agent 的 MEMORY.md 更新时自动记录学习
def log_learning_from_memory(memory_file: str):
    """从 MEMORY.md 提取学习内容并记录"""
    tracker = LearningTracker()
    
    # 读取 MEMORY.md
    with open(memory_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单提取 (可根据实际格式优化)
    if "学习" in content or "learn" in content.lower():
        tracker.add_entry(
            topic="系统学习",
            content=content[:500],  # 前 500 字
            duration=30,
            tags=['系统优化', '学习']
        )
```

### 2. Cron 自动提醒

```python
# 添加到 cron 任务
# 每天晚上 21:00 提醒复习
{
  "name": "学习复习提醒",
  "schedule": {"kind": "cron", "expr": "0 21 * * *", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "📚 学习复习时间到！\n\n请检查待复习内容，巩固知识点。\n\n坚持学习，持续进步！💪"
  }
}
```

---

## 📝 模板文件

### 学习笔记模板

```markdown
# 📚 学习笔记 - {主题}

**学习时间**: {日期}  
**学习时长**: {X} 分钟  
**学习资料**: {来源}

---

## 🎯 核心知识点

1. ...
2. ...
3. ...

## 💡 关键收获

- ...

## 🔧 实践应用

- ...

## ❓ 待解决问题

- ...

## 📖 参考资料

- ...

---

*下次复习：{日期}*
```

---

*版本：v1.0*  
*创建日期：2026-03-18*  
*作者：research-lead 🔬*

# TOOLS.md - 交易执行助手配置

## 风控配置

### 金额限制
```json
{
  "maxAmountPerTrade": 50000,
  "maxAmountPerDay": 100000,
  "maxPositionPerStock": 0.3
}
```

### 次数限制
```json
{
  "maxTradesPerDay": 10,
  "maxTradesPerHour": 2
}
```

### 股票限制
```json
{
  "allowedStocks": ["600519", "300750", "000858"],
  "blockedStocks": []
}
```

### 交易时间
```
上午：9:30 - 11:30
下午：13:00 - 15:00
```

## 工具使用

### 必需工具
- ✅ `message` - 推送交易确认
- ✅ `sessions_send` - 发送交易指令
- ✅ `memory_search` - 查询交易记录
- ✅ `memory_get` - 读取历史数据

### 禁止工具
- ❌ `exec` - 不执行外部命令
- ❌ `browser` - 不访问券商网站
- ❌ 任何直接下单的工具

## 用户信息

- **姓名**: (待填写)
- **券商**: (待填写)
- **风险偏好**: 稳健型
- **联系方式**: 飞书/钉钉/QQ

---

*最后更新：2026-03-17*

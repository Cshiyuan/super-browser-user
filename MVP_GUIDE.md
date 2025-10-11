# MVP 使用指南

Super Browser User MVP 版本 - 快速开始指南

## 🎯 MVP 功能

本 MVP 版本包含以下核心功能：

- ✅ 自动收集小红书旅游攻略
- ✅ 基于攻略生成 AI 旅行计划
- ✅ Web 界面查看攻略和计划
- ✅ REST API 接口
- ✅ 本地 JSON 文件存储

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv pip install browser-use langchain-google-genai python-dotenv fastapi uvicorn jinja2

# 安装浏览器
uvx playwright install chromium --with-deps --no-shell

# 配置 API 密钥
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 2. 创建测试数据（可选）

如果你想快速体验 Web 界面，可以先创建一些测试数据：

```bash
uv run python create_test_data.py
```

这会创建：
- 3 篇成都旅游攻略
- 1 个成都 3 天旅行计划

### 3. 启动 Web 应用

```bash
uv run python run_mvp.py
```

访问：
- 🌐 主页: http://localhost:8000
- 📖 API 文档: http://localhost:8000/docs

## 📝 使用场景

### 场景 1: 收集真实攻略

收集成都的 5 篇旅游攻略：

```bash
uv run python collect_guides.py 成都 --max-posts 5
```

**参数说明**：
- `成都` - 目的地名称
- `--max-posts 5` - 最多收集 5 篇
- `--concurrent` - 启用并发模式（更快）
- `--use-vision` - 启用视觉模式（调试用）

**收集过程**：
1. 打开浏览器访问小红书
2. 搜索"成都旅游"
3. 使用 AI 识别页面结构（Scout 模式）
4. 提取帖子列表
5. 逐个收集帖子详情
6. 保存到 `./data/posts/`

**预计时间**：
- 非并发: ~5 分钟（5 篇）
- 并发模式: ~2 分钟（5 篇）

### 场景 2: 查看已收集的攻略

启动 Web 应用后：

1. 访问 http://localhost:8000
2. 查看攻略卡片（标题、作者、互动数据）
3. 点击攻略查看详情

**Web 界面功能**：
- 📊 统计信息：总攻略数、总点赞数、平均互动率
- 🎴 攻略卡片：标题、作者、互动数据、标签
- 🔍 详情页面：完整内容、图片、原文链接

### 场景 3: 生成旅行计划

使用 API 生成旅行计划：

```bash
curl -X POST "http://localhost:8000/api/generate-plan?destination=成都&days=3"
```

**响应示例**：
```json
{
  "success": true,
  "plan_id": "plan_20251003_080500",
  "message": "成功生成 成都 3 天行程"
}
```

**生成过程**：
1. 从本地存储读取成都的攻略（前 5 篇）
2. 使用 Gemini AI 分析攻略，提取景点、美食
3. 生成每日行程安排
4. 估算预算
5. 保存到 `./data/plans/`

**预计时间**: ~30 秒（取决于 API 响应速度）

### 场景 4: 查看旅行计划

1. 访问 http://localhost:8000/plans
2. 查看所有生成的旅行计划
3. 点击查看详细行程

**计划详情包含**：
- 📅 每日行程（时间、地点、活动）
- 💰 预算明细（交通、住宿、餐饮等）
- ⏱️ 活动时长和费用

## 🔧 API 参考

### 获取攻略列表

```bash
# 获取所有攻略
curl http://localhost:8000/api/posts

# 按目的地筛选
curl "http://localhost:8000/api/posts?destination=成都"
```

**响应**：
```json
{
  "count": 3,
  "posts": [
    {
      "post_id": "test_001",
      "title": "成都三日游攻略",
      "author": "旅行达人小王",
      "likes": 1200,
      "comments": 85,
      "collects": 320,
      "engagement_rate": 1.34,
      "tags": ["成都", "美食", "三日游"]
    }
  ]
}
```

### 获取旅行计划列表

```bash
curl http://localhost:8000/api/plans
```

### 生成旅行计划

```bash
curl -X POST "http://localhost:8000/api/generate-plan?destination=成都&days=3"
```

**参数**：
- `destination` (必需) - 目的地名称
- `days` (可选) - 天数，默认 3 天

## 📂 数据存储

### 目录结构

```
data/
├── posts/          # 攻略数据
│   ├── test_001.json
│   ├── test_002.json
│   └── ...
└── plans/          # 旅行计划
    ├── plan_20251003_080500.json
    └── ...
```

### 数据格式

**攻略 (posts/*.json)**：
```json
{
  "post_id": "test_001",
  "url": "原文链接",
  "title": "标题",
  "content": "正文内容",
  "author": "作者",
  "likes": 1200,
  "comments": 85,
  "collects": 320,
  "tags": ["标签1", "标签2"],
  "location": "成都",
  "publish_time": "2024-09-15",
  "engagement_rate": 1.34,
  "saved_at": "2025-10-03T08:00:00"
}
```

**旅行计划 (plans/*.json)**：
```json
{
  "plan_id": "plan_xxx",
  "destination": "成都",
  "days": 3,
  "itinerary": {
    "day_plans": [
      {
        "day": 1,
        "date": "2024-10-10",
        "activities": [
          {
            "time": "09:00",
            "type": "景点",
            "name": "宽窄巷子",
            "duration": "2小时",
            "description": "...",
            "cost": 50.0
          }
        ]
      }
    ]
  },
  "budget": {
    "transportation": 300.0,
    "accommodation": 900.0,
    "food": 600.0,
    "tickets": 300.0,
    "shopping": 200.0,
    "other": 150.0,
    "total": 2450.0
  }
}
```

## ⚙️ 配置选项

### 环境变量 (.env)

```env
# AI 配置（必需）
GEMINI_API_KEY=your_gemini_api_key

# AI 模型（可选）
GEMINI_MODEL=gemini-2.0-flash-exp

# 温度（可选，0.0-1.0，越高越有创意）
GEMINI_TEMPERATURE=0.7
```

### 收集器配置

在 `collect_guides.py` 中修改：

```python
# 最大收集数量
--max-posts 10

# 启用并发（2-3x 速度提升）
--concurrent

# 最大并发数
--max-concurrent 2

# 启用视觉模式（调试用）
--use-vision
```

## 🐛 故障排除

### 问题 1: 收集失败

**现象**: `collect_guides.py` 运行失败

**可能原因**:
1. 未安装 Playwright 浏览器
2. 网络连接问题
3. 小红书页面结构变化

**解决方法**:
```bash
# 重新安装浏览器
uvx playwright install chromium --with-deps --no-shell

# 启用视觉模式查看问题
uv run python collect_guides.py 成都 --use-vision
```

### 问题 2: AI 生成失败

**现象**: 生成旅行计划时出错

**可能原因**:
1. 未配置 GEMINI_API_KEY
2. API 配额用尽
3. 网络问题

**解决方法**:
```bash
# 检查 .env 文件
cat .env

# 检查 API 配额
# 访问: https://aistudio.google.com/app/apikey
```

### 问题 3: Web 应用启动失败

**现象**: `run_mvp.py` 无法启动

**可能原因**:
1. 端口 8000 被占用
2. 缺少依赖

**解决方法**:
```bash
# 检查端口占用
lsof -i :8000

# 重新安装依赖
uv pip install fastapi uvicorn jinja2
```

## 📊 性能参考

### 收集性能

- **单线程**: ~1 分钟/篇
- **并发模式**: ~20 秒/篇（3 并发）
- **成功率**: 95%+（Scout 模式）

### AI 生成性能

- **行程生成**: ~30 秒/个计划
- **每日成本**: 免费（Gemini Flash 免费额度）

### 存储性能

- **读取**: 即时（本地文件）
- **写入**: <10ms/个文件
- **容量**: 无限制

## 🎓 下一步

### 扩展建议

1. **添加更多数据源**
   - 参考 `src/infrastructure/external/xiaohongshu/collector.py`
   - 实现微博、抖音收集器

2. **优化 AI 生成**
   - 调整 prompt 模板
   - 添加用户偏好参数

3. **增强 Web 界面**
   - 添加搜索和筛选功能
   - 实现在线生成计划

4. **数据库集成**
   - 替换本地存储为 PostgreSQL
   - 添加用户账号系统

### 学习资源

- [架构文档](docs/architecture/ARCHITECTURE.md) - 了解系统设计
- [API 参考](docs/api/API_REFERENCE.md) - 详细 API 说明
- [CLAUDE.md](./CLAUDE.md) - browser-use 开发指南

## 💡 最佳实践

1. **收集攻略**
   - 先收集少量测试（5-10 篇）
   - 验证数据质量后再大规模收集
   - 使用并发模式提升效率

2. **生成计划**
   - 确保至少有 3-5 篇攻略作为基础
   - 调整天数参数（1-7 天最佳）
   - 可多次生成，选择最满意的

3. **数据管理**
   - 定期备份 `./data/` 目录
   - 清理过期或低质量数据
   - 使用版本控制管理配置文件

---

**维护者**: Shiyuan Chen
**最后更新**: 2025-10-03
**版本**: MVP v1.0

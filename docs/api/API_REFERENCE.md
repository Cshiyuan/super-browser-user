# API 参考文档

本文档描述核心类和方法的使用方式。

## 核心服务 API

### GuideCollectorService

攻略收集服务。

```python
from src.core.services.guide_collector import GuideCollectorService

# 初始化
service = GuideCollectorService(
    output_dir="./collected_posts",
    use_vision=False,
    concurrent=False,
    max_concurrent=2
)

# 收集攻略
guides = await service.collect_guides(
    destination="成都",
    max_posts=10
)

# 筛选高质量攻略
high_quality = await service.filter_high_quality_guides(
    posts=guides,
    min_engagement_rate=0.1
)
```

### ItineraryGeneratorService

行程生成服务。

```python
from src.core.services.itinerary_generator import ItineraryGeneratorService
from src.infrastructure.external.ai.gemini_client import GeminiClient

# 初始化（可选 AI 客户端）
ai_client = GeminiClient()
service = ItineraryGeneratorService(ai_client=ai_client)

# 生成行程
itinerary = await service.generate_itinerary(
    destination="成都",
    days=3,
    guides=guides,
    preferences={"budget": "中等"}
)

# 计算成本
cost = service.calculate_total_cost(itinerary)
```

## 仓储 API

### PostRepository

帖子仓储。

```python
from src.core.repositories.post_repository import InMemoryPostRepository

# 初始化
repo = InMemoryPostRepository()

# 保存
await repo.save(post)

# 查询
post = await repo.find_by_id("post_001")
posts = await repo.find_by_destination("成都", limit=10)
high_quality = await repo.find_high_quality(min_engagement_rate=0.1)

# 删除
deleted = await repo.delete("post_001")
```

## AI 客户端 API

### GeminiClient

Google Gemini AI 客户端。

```python
from src.infrastructure.external.ai.gemini_client import GeminiClient

# 初始化
client = GeminiClient(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    api_key="your_key"
)

# 聊天
response = await client.chat(
    prompt="介绍成都",
    system_prompt="你是旅游助手"
)

# 提取结构化数据
data = await client.extract_structured_data(
    text="推荐景点：宽窄巷子、锦里",
    schema={"attractions": ["string"]}
)

# 提取景点
attractions = await client.extract_attractions(text)

# 提取餐厅
restaurants = await client.extract_restaurants(text)

# 总结攻略
summary = await client.summarize_guides(
    guides=["攻略1", "攻略2"],
    destination="成都"
)
```

## 领域模型

### PostDetail

帖子详情模型。

```python
from src.core.domain.models.post import PostDetail

post = PostDetail(
    post_id="1",
    url="https://example.com/1",
    title="成都攻略",
    content="...",
    author="作者",
    likes=1000,
    comments=50,
    collects=200,
    images=["img1.jpg"],
    tags=["成都", "旅游"]
)

# 计算属性
rate = post.engagement_rate  # 自动计算互动率
```

### TravelPlan

旅行计划模型。

```python
from src.core.domain.models.travel import (
    TravelPlan, Itinerary, DayPlan, Activity, Budget
)

# 创建活动
activity = Activity(
    time="09:00",
    type="景点",
    name="宽窄巷子",
    duration=120,
    description="游览宽窄巷子"
)

# 创建每日计划
day_plan = DayPlan(
    day=1,
    date="2025-01-01",
    activities=[activity]
)

# 创建行程
itinerary = Itinerary(
    destination="成都",
    days=3,
    day_plans=[day_plan, ...]
)

# 创建预算
budget = Budget(
    transportation=600.0,
    accommodation=900.0,
    food=600.0,
    tickets=300.0,
    shopping=300.0,
    other=150.0
)

# 创建旅行计划
plan = TravelPlan(
    plan_id="plan_001",
    user_id="user_001",
    destination="成都",
    days=3,
    itinerary=itinerary,
    budget=budget
)

# 计算属性
total = budget.total  # 自动计算总预算
activities = itinerary.total_activities  # 自动计算活动数
```

## 完整示例

查看 `examples/` 目录下的示例程序了解完整用法。

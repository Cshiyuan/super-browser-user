# API 设计文档

本文档描述 Super Browser User 项目的 REST API 设计。

## 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: Bearer Token (未来版本)
- **数据格式**: JSON
- **字符编码**: UTF-8

## 通用响应格式

### 成功响应

```json
{
  "data": { ... },
  "message": "Success"
}
```

### 错误响应

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": { ... }
  }
}
```

## API 端点

### 1. 健康检查

#### GET /health

检查服务健康状态

**响应示例**:

```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "0.1.0",
  "environment": "development"
}
```

### 2. 旅游攻略收集

#### POST /guides/collect

收集指定目的地的旅游攻略

**请求体**:

```json
{
  "destination": "成都",
  "max_posts": 10
}
```

**响应示例**:

```json
[
  {
    "post_id": "1",
    "url": "https://www.xiaohongshu.com/...",
    "title": "成都三日游攻略",
    "content": "详细内容...",
    "author": "旅行达人",
    "likes": 1250,
    "comments": 89,
    "collects": 456,
    "engagement_rate": 0.0856,
    "images": ["url1", "url2"],
    "tags": ["成都", "美食", "旅游"]
  }
]
```

**状态码**:
- `200 OK`: 成功
- `400 Bad Request`: 请求参数错误
- `500 Internal Server Error`: 服务器错误

#### GET /guides/high-quality

获取高质量攻略

**查询参数**:
- `destination` (required): 目的地名称
- `min_engagement_rate` (optional, default: 0.05): 最小互动率

**示例**: `/guides/high-quality?destination=成都&min_engagement_rate=0.08`

**响应**: 同 `/guides/collect`

### 3. 旅行计划生成

#### POST /travel/plans

创建旅行计划

**请求体**:

```json
{
  "destination": "成都",
  "days": 3,
  "preferences": {
    "budget": 3000,
    "interests": ["美食", "文化"],
    "pace": "relaxed"
  }
}
```

**响应示例**:

```json
{
  "destination": "成都",
  "days": 3,
  "day_plans": [
    {
      "day": 1,
      "date": "2025-01-20",
      "activities": [
        {
          "time": "09:00",
          "type": "景点",
          "name": "宽窄巷子",
          "duration": 120,
          "description": "游览宽窄巷子，体验成都老街文化"
        },
        {
          "time": "12:00",
          "type": "餐饮",
          "name": "龙抄手",
          "duration": 60,
          "description": "午餐 - 品尝成都特色小吃"
        }
      ]
    }
  ],
  "total_cost": 2850.0
}
```

**状态码**:
- `200 OK`: 成功
- `400 Bad Request`: 请求参数错误
- `500 Internal Server Error`: 生成失败

#### GET /travel/destinations/{destination}/summary

获取目的地攻略摘要

**路径参数**:
- `destination`: 目的地名称

**示例**: `/travel/destinations/成都/summary`

**响应示例**:

```json
{
  "destination": "成都",
  "guide_count": 5,
  "summary": "## 必游景点\n1. 宽窄巷子 - 体验老成都的韵味\n2. 武侯祠 - 三国文化圣地\n\n## 推荐美食\n1. 火锅 - 成都特色\n2. 串串香 - 街头小吃..."
}
```

## 数据模型

### PostDetail (帖子详情)

```typescript
interface PostDetail {
  post_id: string;
  url: string;
  title: string;
  content: string;
  author: string;
  likes: number;
  comments: number;
  collects: number;
  engagement_rate: number;  // 计算属性：(likes + comments + collects) / (likes + 1)
  images: string[];
  tags: string[];
  publish_time?: string;
  location?: string;
}
```

### Itinerary (行程)

```typescript
interface Itinerary {
  destination: string;
  days: number;
  day_plans: DayPlan[];
  total_cost?: number;
}

interface DayPlan {
  day: number;
  date: string;  // YYYY-MM-DD
  activities: Activity[];
}

interface Activity {
  time: string;  // HH:MM
  type: string;  // 景点 | 餐饮 | 交通 | 住宿 | 其他
  name: string;
  duration: number;  // 分钟
  description: string;
  cost?: number;
}
```

## 错误码

| 错误码 | 说明 |
|-------|------|
| `INVALID_PARAMS` | 请求参数无效 |
| `RESOURCE_NOT_FOUND` | 资源未找到 |
| `COLLECTION_FAILED` | 数据收集失败 |
| `GENERATION_FAILED` | 行程生成失败 |
| `AI_SERVICE_ERROR` | AI 服务错误 |
| `DATABASE_ERROR` | 数据库错误 |
| `RATE_LIMIT_EXCEEDED` | 请求频率超限 |

## 速率限制

- **匿名用户**: 10 请求/分钟
- **认证用户**: 100 请求/分钟
- **Premium 用户**: 1000 请求/分钟

## 版本控制

API 使用 URL 路径版本控制：
- `/api/v1/...` - 当前版本
- `/api/v2/...` - 未来版本

## WebSocket API (未来版本)

用于实时收集进度推送：

```javascript
ws://localhost:8000/ws/collection/{task_id}

// 消息格式
{
  "type": "progress",
  "data": {
    "total": 10,
    "completed": 3,
    "current": "正在收集第 4 篇攻略..."
  }
}
```

## 示例代码

### Python (httpx)

```python
import httpx

async def collect_guides(destination: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/guides/collect",
            json={"destination": destination, "max_posts": 10}
        )
        return response.json()
```

### cURL

```bash
# 收集攻略
curl -X POST http://localhost:8000/api/v1/guides/collect \
  -H "Content-Type: application/json" \
  -d '{"destination": "成都", "max_posts": 10}'

# 生成计划
curl -X POST http://localhost:8000/api/v1/travel/plans \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "成都",
    "days": 3,
    "preferences": {"budget": 3000}
  }'
```

## 测试

使用 Swagger UI 进行交互式测试：

http://localhost:8000/docs

使用 ReDoc 查看文档：

http://localhost:8000/redoc

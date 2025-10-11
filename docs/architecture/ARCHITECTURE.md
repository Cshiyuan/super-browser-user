# 架构设计文档

Super Browser User 采用领域驱动设计（DDD）和分层架构。

## 总体架构

```
应用层 (apps/)
   ├── FastAPI API
   └── CLI Tools
        ↓
核心层 (src/core/)
   ├── 服务层 (services/)
   ├── 仓储层 (repositories/)
   └── 领域层 (domain/)
        ↓
基础设施层 (src/infrastructure/)
   ├── 外部服务 (external/)
   ├── 数据库 (database/)
   └── 缓存 (cache/)
```

## 四层架构

### 1. 领域层 (Domain Layer)
- **位置**: `src/core/domain/`
- **职责**: 定义业务领域模型和规则
- **核心类**: `PostDetail`, `TravelPlan`, `Itinerary`, `Budget`

### 2. 仓储层 (Repository Layer)
- **位置**: `src/core/repositories/`
- **职责**: 数据持久化抽象层
- **核心类**: `PostRepository`, `TravelPlanRepository`

### 3. 服务层 (Service Layer)
- **位置**: `src/core/services/`
- **职责**: 封装业务逻辑
- **核心类**: `GuideCollectorService`, `ItineraryGeneratorService`

### 4. 基础设施层 (Infrastructure Layer)
- **位置**: `src/infrastructure/`
- **职责**: 外部服务集成
- **核心类**: `GeminiClient`, `XiaohongshuCollector`

## 设计模式

- **Repository Pattern**: 数据访问抽象
- **Dependency Injection**: 依赖注入
- **Strategy Pattern**: 多种提取策略（AI/关键词）

## 详细说明

查看源码中的详细注释了解更多信息。

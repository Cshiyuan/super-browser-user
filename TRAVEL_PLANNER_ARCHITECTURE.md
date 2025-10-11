# AI 旅游攻略规划助手 - 技术架构文档

## 📋 目录

1. [产品概述](#产品概述)
2. [核心功能](#核心功能)
3. [整体架构](#整体架构)
4. [数据源分析](#数据源分析)
5. [核心模块设计](#核心模块设计)
6. [AI 智能引擎](#ai-智能引擎)
7. [数据模型](#数据模型)
8. [技术栈](#技术栈)
9. [实现流程](#实现流程)
10. [可行性分析](#可行性分析)
11. [挑战与解决方案](#挑战与解决方案)
12. [开发路线图](#开发路线图)

---

## 产品概述

### 产品定位

**AI 旅游攻略规划助手** - 从小红书收集真实旅游攻略，结合携程等平台的实时价格信息，自动生成完整的旅游计划和预算方案。

### 核心价值

1. **攻略聚合**: 从小红书收集真实用户分享的旅游体验
2. **价格实时**: 从携程/去哪儿等平台获取最新机票酒店价格
3. **AI 整合**: 智能分析攻略，提取景点、美食、路线
4. **预算规划**: 自动计算总预算，提供多种方案
5. **一键生成**: 输出完整的可执行旅游计划

### 使用场景

**用户输入**:
```
目的地: 成都
出发地: 北京
旅行时间: 2025-05-01 ~ 2025-05-05 (5天)
预算: 5000元/人
人数: 2人
```

**系统输出**:
```
📋 成都5日游完整攻略

✈️ 交通方案
- 去程: 2025-05-01 北京→成都 CA1234 ¥650/人
- 返程: 2025-05-05 成都→北京 CA5678 ¥680/人

🏨 住宿方案
- 5月1-2日: 春熙路附近民宿 ¥280/晚
- 5月3-4日: 宽窄巷子酒店 ¥350/晚

📍 行程安排
Day 1: 宽窄巷子 → 锦里 → 春熙路
Day 2: 熊猫基地 → 太古里 → 九眼桥酒吧街
Day 3: 都江堰 → 青城山
Day 4: 武侯祠 → 人民公园 → 建设路美食街
Day 5: 成都博物馆 → 返程

🍜 美食推荐
- 火锅: 小龙坎、大龙燚 (人均¥100)
- 川菜: 马旺子、成都吃客 (人均¥80)
- 小吃: 钟水饺、韩包子 (人均¥30)

💰 预算明细
交通: ¥2,660 (2人往返机票)
住宿: ¥2,520 (4晚 × 2人)
餐饮: ¥1,200 (5天 × 2人 × ¥120/天)
门票: ¥500 (熊猫基地、都江堰等)
其他: ¥500 (交通、购物等)
━━━━━━━━━━━━━━━━━━━━━━━
总计: ¥7,380 (略超预算)

💡 省钱建议:
1. 提前15天订票可省¥200
2. 选择快捷酒店可省¥600
3. 优化后总预算: ¥6,580
```

---

## 核心功能

### 功能模块图

```
┌─────────────────────────────────────────────────────────┐
│                    用户输入层                           │
│  目的地 | 时间 | 预算 | 偏好                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 数据收集层（并行）                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │小红书攻略│  │携程机票  │  │携程酒店  │  │去哪儿  ││
│  │景点美食  │  │实时价格  │  │实时价格  │  │价格对比││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   AI 分析层                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Gemini AI 多模态分析                            │  │
│  │  - 提取攻略中的景点、美食、路线                 │  │
│  │  - 分析图片中的场景和体验                       │  │
│  │  - 理解用户偏好和评价                           │  │
│  │  - 生成合理的行程安排                           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  规划生成层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │行程规划  │  │预算计算  │  │方案优化  │  │报告生成││
│  │路线优化  │  │价格汇总  │  │多方案    │  │PDF/HTML││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   输出层                                 │
│  完整旅游计划 | 预算明细 | 预订链接 | 注意事项         │
└─────────────────────────────────────────────────────────┘
```

### 核心功能列表

#### 1. 智能攻略收集 ⭐⭐⭐⭐⭐
- 从小红书收集目的地相关攻略
- 提取景点、美食、住宿、路线信息
- 分析用户评价和推荐度
- 图片识别（景点、美食照片）

#### 2. 实时价格查询 ⭐⭐⭐⭐⭐
- 携程机票查询（出发地→目的地）
- 携程酒店查询（位置、价格、评分）
- 去哪儿价格对比
- 价格趋势预测

#### 3. AI 行程规划 ⭐⭐⭐⭐⭐
- 根据天数智能安排行程
- 景点路线优化（减少通勤时间）
- 时间分配合理化
- 考虑景点开放时间、排队情况

#### 4. 预算计算 ⭐⭐⭐⭐⭐
- 交通费用（机票、高铁、当地交通）
- 住宿费用（多种档次可选）
- 餐饮预算（根据攻略人均消费）
- 门票及其他费用
- 总预算控制和优化建议

#### 5. 多方案生成 ⭐⭐⭐⭐
- 经济方案（预算优先）
- 舒适方案（体验优先）
- 平衡方案（性价比）
- 自定义方案

#### 6. 报告生成 ⭐⭐⭐⭐
- 完整攻略 PDF/HTML
- 预算明细表格
- 预订链接一键跳转
- 地图导航集成

---

## 整体架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         前端层                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Web UI  │  │  小程序 │  │   APP   │  │   CLI   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       API 网关层                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI + GraphQL                                    │  │
│  │  - 请求路由  - 参数验证  - 限流控制                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      业务编排层                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  规划编排器 (Orchestrator)                           │  │
│  │  - 任务调度  - 并行执行  - 结果聚合                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    核心服务层（微服务）                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │攻略收集  │  │价格查询  │  │AI 分析   │  │规划生成  │   │
│  │服务      │  │服务      │  │服务      │  │服务      │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据采集层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │browser-  │  │携程 API/ │  │去哪儿    │  │高德地图  │   │
│  │use       │  │爬虫      │  │爬虫      │  │API       │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据存储层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │PostgreSQL│  │  Redis   │  │  S3/OSS  │  │Vector DB │   │
│  │关系数据  │  │  缓存    │  │  图片    │  │攻略向量  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 技术架构分层

| 层次 | 职责 | 技术选型 |
|-----|------|---------|
| **前端层** | 用户交互 | React/Vue + 微信小程序 + Flutter APP |
| **API层** | 接口服务 | FastAPI + GraphQL |
| **编排层** | 任务调度 | Celery + Redis |
| **服务层** | 业务逻辑 | Python 微服务 |
| **采集层** | 数据获取 | browser-use + API + 爬虫 |
| **存储层** | 数据持久化 | PostgreSQL + Redis + OSS + Qdrant |

---

## 数据源分析

### 1. 小红书（攻略来源）⭐⭐⭐⭐⭐

**可获取数据**:
- ✅ 旅游攻略帖子（标题、正文、图片）
- ✅ 景点推荐（位置、特色、门票）
- ✅ 美食推荐（餐厅名、人均消费、菜品）
- ✅ 住宿体验（酒店/民宿、价格、评价）
- ✅ 路线安排（行程规划、时间分配）
- ✅ 注意事项（天气、穿搭、避坑）

**实现方式**:
```python
# 复用现有的 xiaohongshu_collector.py
class TravelGuideCollector(XiaohongshuCollectorOptimized):
    """旅游攻略收集器"""

    async def collect_destination_guides(
        self,
        destination: str,
        max_posts: int = 20
    ) -> List[TravelGuide]:
        """收集目的地攻略"""

        # 1. 搜索关键词
        keywords = [
            f"{destination}旅游攻略",
            f"{destination}自由行",
            f"{destination}景点推荐",
            f"{destination}美食攻略"
        ]

        guides = []
        for keyword in keywords:
            # 2. 收集帖子
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
            posts = await self.collect_posts_from_search(search_url, max_posts)

            # 3. 提取攻略信息
            for post in posts:
                guide = self.extract_guide_info(post)
                guides.append(guide)

        return guides

    def extract_guide_info(self, post: Post) -> TravelGuide:
        """从帖子提取攻略信息（使用 AI）"""

        prompt = f"""
        分析这篇小红书旅游攻略，提取以下信息：

        标题: {post.title}
        内容: {post.content}

        请提取：
        1. 景点列表（名称、推荐理由、门票、开放时间）
        2. 美食推荐（餐厅、菜品、人均消费）
        3. 住宿信息（类型、位置、价格）
        4. 行程安排（天数、路线）
        5. 注意事项（交通、天气、避坑）

        返回 JSON 格式
        """

        # AI 提取
        result = gemini.generate(prompt)
        return TravelGuide(**result)
```

**技术可行性**: ✅ 完全可行（已有完整实现）

---

### 2. 携程（机票/酒店）⭐⭐⭐⭐

**可获取数据**:
- ✅ 机票信息（航班号、时间、价格、舱位）
- ✅ 酒店信息（名称、位置、价格、评分、设施）
- ⚠️ 需要处理反爬虫

**实现方式**:

#### 方式1: 官方 API（推荐）⭐⭐⭐⭐⭐
```python
# 携程有开放 API（需要申请）
# https://open.ctrip.com/

class CtripAPIClient:
    """携程 API 客户端"""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.ctrip.com/v1"

    async def search_flights(
        self,
        from_city: str,
        to_city: str,
        date: str
    ) -> List[Flight]:
        """搜索机票"""

        url = f"{self.base_url}/flights/search"
        params = {
            "from": from_city,
            "to": to_city,
            "date": date,
            "api_key": self.api_key
        }

        # 签名
        signature = self._generate_signature(params)
        params["signature"] = signature

        # 请求
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            data = resp.json()

        return [Flight(**item) for item in data["flights"]]

    async def search_hotels(
        self,
        city: str,
        checkin: str,
        checkout: str
    ) -> List[Hotel]:
        """搜索酒店"""
        # 类似实现
        pass
```

**优点**:
- ✅ 稳定可靠
- ✅ 数据准确
- ✅ 无反爬虫问题

**缺点**:
- ❌ 需要企业认证
- ❌ 可能有调用限制

#### 方式2: 浏览器自动化（备用）⭐⭐⭐
```python
class CtripScraper:
    """携程爬虫（browser-use）"""

    async def search_flights_by_browser(
        self,
        from_city: str,
        to_city: str,
        date: str
    ) -> List[Flight]:
        """通过浏览器搜索机票"""

        # 1. 访问携程机票搜索页
        url = f"https://flights.ctrip.com/..."

        # 2. 使用 browser-use Agent
        agent = Agent(
            task=f"""
            访问 {url}
            填写：
            - 出发地: {from_city}
            - 目的地: {to_city}
            - 日期: {date}

            点击搜索，使用 extract_structured_data 收集：
            - 航班号
            - 起飞/到达时间
            - 价格
            - 航空公司
            - 舱位
            返回 JSON 数组
            """,
            llm=self.llm,
            browser_context=self.context
        )

        result = await agent.run()
        flights = self.extract_flights(result)
        return flights
```

**优点**:
- ✅ 无需 API 密钥
- ✅ 灵活性高

**缺点**:
- ❌ 可能被反爬虫限制
- ❌ 不够稳定

#### 推荐方案: API 优先，浏览器备用

```python
class FlightSearchService:
    """机票搜索服务（混合模式）"""

    def __init__(self):
        self.api_client = CtripAPIClient(...)
        self.scraper = CtripScraper(...)

    async def search_flights(self, from_city, to_city, date):
        try:
            # 优先使用 API
            return await self.api_client.search_flights(...)
        except Exception as e:
            # API 失败，降级到浏览器
            logger.warning(f"API failed: {e}, fallback to browser")
            return await self.scraper.search_flights_by_browser(...)
```

**技术可行性**: ✅ 可行（API 或 浏览器自动化）

---

### 3. 去哪儿（价格对比）⭐⭐⭐

**可获取数据**:
- ✅ 机票比价
- ✅ 酒店比价

**实现方式**: 同携程（API 或 browser-use）

**技术可行性**: ✅ 可行

---

### 4. 高德地图（路线规划）⭐⭐⭐⭐⭐

**可获取数据**:
- ✅ 景点位置（经纬度）
- ✅ 路线规划（步行/驾车/公交）
- ✅ 距离和耗时
- ✅ 周边查询（餐厅、酒店）

**实现方式**: 官方 API

```python
class AmapAPIClient:
    """高德地图 API"""

    async def geocode(self, address: str) -> Location:
        """地址转坐标"""
        url = "https://restapi.amap.com/v3/geocode/geo"
        params = {
            "address": address,
            "key": self.api_key
        }
        # ...

    async def route_planning(
        self,
        origin: Location,
        destination: Location,
        mode: str = "walking"  # walking/driving/transit
    ) -> Route:
        """路线规划"""
        url = "https://restapi.amap.com/v3/direction/{mode}"
        # ...

    async def nearby_search(
        self,
        location: Location,
        keywords: str,  # "餐厅" | "酒店"
        radius: int = 1000
    ) -> List[POI]:
        """周边搜索"""
        # ...
```

**技术可行性**: ✅ 完全可行（官方 API 稳定）

---

## 核心模块设计

### 1. 攻略收集模块 (Guide Collector)

**职责**: 从小红书收集并分析旅游攻略

```python
class GuideCollectorService:
    """攻略收集服务"""

    async def collect_and_analyze(
        self,
        destination: str,
        days: int
    ) -> DestinationGuide:
        """收集并分析目的地攻略"""

        # 1. 收集攻略帖子
        posts = await self.collect_guides(destination, max_posts=30)

        # 2. AI 提取结构化信息
        attractions = []
        restaurants = []
        routes = []

        for post in posts:
            # 并发提取
            extracted = await self.ai_extract(post)
            attractions.extend(extracted.attractions)
            restaurants.extend(extracted.restaurants)
            routes.extend(extracted.routes)

        # 3. 去重和聚合
        attractions = self.deduplicate_attractions(attractions)
        restaurants = self.deduplicate_restaurants(restaurants)

        # 4. 评分排序
        attractions = self.rank_by_popularity(attractions)
        restaurants = self.rank_by_popularity(restaurants)

        return DestinationGuide(
            destination=destination,
            attractions=attractions[:20],  # Top 20
            restaurants=restaurants[:30],  # Top 30
            sample_routes=routes[:5]
        )

    async def ai_extract(self, post: Post) -> ExtractedInfo:
        """AI 提取攻略信息"""

        # 多模态分析（文字 + 图片）
        prompt = f"""
        分析这篇旅游攻略：

        标题: {post.title}
        内容: {post.content}
        图片: {len(post.images)}张

        提取：
        1. 景点信息
        {{
          "name": "景点名",
          "location": "具体位置",
          "ticket_price": "门票价格",
          "visit_duration": "建议游玩时间",
          "highlights": ["亮点1", "亮点2"],
          "tips": ["注意事项1", ...]
        }}

        2. 餐厅信息
        {{
          "name": "餐厅名",
          "cuisine": "菜系",
          "average_cost": 人均消费,
          "recommended_dishes": ["菜品1", ...],
          "location": "位置"
        }}

        3. 路线信息
        {{
          "day": 天数,
          "route": ["地点1", "地点2", ...],
          "notes": "注意事项"
        }}

        返回 JSON
        """

        result = await self.gemini.generate(
            prompt,
            images=post.images  # Gemini 支持多模态
        )

        return ExtractedInfo(**result)

    def deduplicate_attractions(self, attractions: List[Attraction]) -> List[Attraction]:
        """景点去重（基于名称相似度）"""

        from difflib import SequenceMatcher

        unique = []
        for attr in attractions:
            # 检查是否与已有景点重复
            is_duplicate = False
            for existing in unique:
                similarity = SequenceMatcher(
                    None,
                    attr.name,
                    existing.name
                ).ratio()

                if similarity > 0.8:  # 80% 相似视为重复
                    # 合并信息（保留更详细的）
                    existing.merge(attr)
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique.append(attr)

        return unique

    def rank_by_popularity(self, items: List) -> List:
        """按热度排序"""

        # 热度 = 提及次数 * 平均评分
        for item in items:
            item.popularity_score = item.mention_count * item.avg_rating

        return sorted(items, key=lambda x: x.popularity_score, reverse=True)
```

---

### 2. 价格查询模块 (Price Query Service)

**职责**: 查询机票、酒店等实时价格

```python
class PriceQueryService:
    """价格查询服务"""

    def __init__(self):
        self.ctrip = CtripAPIClient(...)
        self.qunar = QunarAPIClient(...)
        self.cache = RedisCache(...)

    async def search_flights(
        self,
        from_city: str,
        to_city: str,
        date: str,
        return_date: Optional[str] = None
    ) -> FlightSearchResult:
        """搜索机票（往返）"""

        # 1. 检查缓存
        cache_key = f"flight:{from_city}:{to_city}:{date}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # 2. 并发查询多个平台
        tasks = [
            self.ctrip.search_flights(from_city, to_city, date),
            self.qunar.search_flights(from_city, to_city, date)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 3. 聚合结果
        all_flights = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Query failed: {result}")
                continue
            all_flights.extend(result)

        # 4. 去重（相同航班号）
        unique_flights = self.deduplicate_flights(all_flights)

        # 5. 排序（价格优先）
        sorted_flights = sorted(unique_flights, key=lambda f: f.price)

        # 6. 缓存结果（1小时）
        result = FlightSearchResult(flights=sorted_flights[:20])
        await self.cache.set(cache_key, result, ttl=3600)

        return result

    async def search_hotels(
        self,
        city: str,
        location: str,  # "市中心" | "景区附近"
        checkin: str,
        checkout: str,
        budget: Optional[int] = None
    ) -> HotelSearchResult:
        """搜索酒店"""

        # 1. 获取位置坐标（高德地图）
        coords = await self.amap.geocode(f"{city}{location}")

        # 2. 并发查询
        tasks = [
            self.ctrip.search_hotels(coords, checkin, checkout),
            self.qunar.search_hotels(coords, checkin, checkout)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 3. 聚合和去重
        all_hotels = []
        for result in results:
            if not isinstance(result, Exception):
                all_hotels.extend(result)

        unique_hotels = self.deduplicate_hotels(all_hotels)

        # 4. 价格过滤
        if budget:
            unique_hotels = [h for h in unique_hotels if h.price <= budget]

        # 5. 排序（评分 × 性价比）
        sorted_hotels = sorted(
            unique_hotels,
            key=lambda h: h.rating * (1000 / h.price),  # 性价比指数
            reverse=True
        )

        return HotelSearchResult(hotels=sorted_hotels[:30])
```

---

### 3. AI 规划引擎 (Planning Engine)

**职责**: 智能生成旅游行程和预算方案

```python
class TravelPlanningEngine:
    """旅游规划引擎"""

    async def generate_plan(
        self,
        request: PlanRequest
    ) -> TravelPlan:
        """生成旅游计划"""

        # 1. 收集数据
        guide = await self.guide_collector.collect_and_analyze(
            request.destination,
            request.days
        )

        flights = await self.price_service.search_flights(
            request.from_city,
            request.destination,
            request.start_date,
            request.end_date
        )

        hotels = await self.price_service.search_hotels(
            request.destination,
            "市中心",
            request.start_date,
            request.end_date,
            budget=request.budget_per_night
        )

        # 2. AI 生成行程
        itinerary = await self.ai_generate_itinerary(
            guide=guide,
            days=request.days,
            preferences=request.preferences
        )

        # 3. 计算预算
        budget = self.calculate_budget(
            flights=flights.flights[0],  # 最优航班
            hotels=hotels.hotels[0],     # 最优酒店
            itinerary=itinerary,
            num_people=request.num_people,
            days=request.days
        )

        # 4. 优化方案
        if budget.total > request.total_budget:
            # 预算超了，优化
            optimized = await self.optimize_budget(
                flights, hotels, itinerary,
                target_budget=request.total_budget
            )
            return optimized

        # 5. 生成最终计划
        return TravelPlan(
            destination=request.destination,
            flights=flights.flights[0],
            hotels=hotels.hotels[0],
            itinerary=itinerary,
            budget=budget,
            tips=guide.tips
        )

    async def ai_generate_itinerary(
        self,
        guide: DestinationGuide,
        days: int,
        preferences: UserPreferences
    ) -> Itinerary:
        """AI 生成行程"""

        # 构建提示词
        prompt = f"""
        你是一个专业的旅游规划师，请根据以下信息生成 {days} 天的旅游行程：

        目的地: {guide.destination}

        热门景点 Top 10:
        {json.dumps([{"name": a.name, "亮点": a.highlights, "游玩时长": a.visit_duration} for a in guide.attractions[:10]], ensure_ascii=False, indent=2)}

        热门餐厅 Top 10:
        {json.dumps([{"name": r.name, "菜系": r.cuisine, "人均": r.average_cost} for r in guide.restaurants[:10]], ensure_ascii=False, indent=2)}

        用户偏好:
        - 兴趣: {preferences.interests}  # ["自然风光", "历史文化", "美食"]
        - 节奏: {preferences.pace}       # "relaxed" | "moderate" | "fast"
        - 预算: {preferences.budget}     # "budget" | "moderate" | "luxury"

        要求：
        1. 合理安排每天行程（上午、下午、晚上）
        2. 考虑景点开放时间和地理位置（减少通勤）
        3. 平衡观光和休闲（避免过度疲劳）
        4. 推荐每餐的餐厅
        5. 给出每个景点的预计游玩时间

        返回 JSON 格式：
        {{
          "days": [
            {{
              "day": 1,
              "morning": {{
                "attraction": "景点名",
                "duration": "2小时",
                "highlights": ["亮点1", "亮点2"],
                "tips": "注意事项"
              }},
              "lunch": {{
                "restaurant": "餐厅名",
                "cuisine": "菜系",
                "average_cost": 80
              }},
              "afternoon": {{...}},
              "dinner": {{...}},
              "notes": "今日总结"
            }},
            ...
          ]
        }}
        """

        # AI 生成
        result = await self.gemini.generate(prompt)
        itinerary = Itinerary(**result)

        # 优化路线（减少通勤时间）
        itinerary = await self.optimize_route(itinerary)

        return itinerary

    async def optimize_route(self, itinerary: Itinerary) -> Itinerary:
        """优化路线（减少通勤时间）"""

        for day in itinerary.days:
            # 获取当天所有景点的坐标
            attractions = [
                day.morning.attraction if day.morning else None,
                day.afternoon.attraction if day.afternoon else None,
                day.evening.attraction if day.evening else None
            ]
            attractions = [a for a in attractions if a]

            # 获取坐标
            locations = []
            for attr_name in attractions:
                loc = await self.amap.geocode(attr_name)
                locations.append(loc)

            # 使用 TSP 算法优化顺序（旅行商问题）
            optimized_order = self.solve_tsp(locations)

            # 重新排列行程
            day.reorder(optimized_order)

        return itinerary

    def solve_tsp(self, locations: List[Location]) -> List[int]:
        """解决旅行商问题（简化版：贪心算法）"""

        # 贪心算法：每次选择最近的下一个点
        n = len(locations)
        visited = [False] * n
        order = [0]
        visited[0] = True

        for _ in range(n - 1):
            current = order[-1]
            min_dist = float('inf')
            next_idx = -1

            for i in range(n):
                if not visited[i]:
                    dist = self.calculate_distance(
                        locations[current],
                        locations[i]
                    )
                    if dist < min_dist:
                        min_dist = dist
                        next_idx = i

            order.append(next_idx)
            visited[next_idx] = True

        return order

    def calculate_budget(
        self,
        flights: Flight,
        hotels: Hotel,
        itinerary: Itinerary,
        num_people: int,
        days: int
    ) -> Budget:
        """计算预算"""

        # 交通费用
        transport_cost = (flights.price * 2) * num_people  # 往返

        # 住宿费用
        accommodation_cost = hotels.price * (days - 1) * num_people  # N-1 晚

        # 餐饮费用
        food_cost = 0
        for day in itinerary.days:
            if day.lunch:
                food_cost += day.lunch.average_cost
            if day.dinner:
                food_cost += day.dinner.average_cost
        food_cost *= num_people

        # 门票费用
        ticket_cost = sum(
            day.morning.ticket_price if day.morning else 0
            for day in itinerary.days
        ) * num_people

        # 其他费用（预估 10%）
        other_cost = (transport_cost + accommodation_cost + food_cost + ticket_cost) * 0.1

        return Budget(
            transport=transport_cost,
            accommodation=accommodation_cost,
            food=food_cost,
            tickets=ticket_cost,
            other=other_cost,
            total=transport_cost + accommodation_cost + food_cost + ticket_cost + other_cost
        )

    async def optimize_budget(
        self,
        flights: FlightSearchResult,
        hotels: HotelSearchResult,
        itinerary: Itinerary,
        target_budget: float
    ) -> TravelPlan:
        """优化预算（在目标预算内）"""

        # 策略1: 选择更便宜的航班
        # 策略2: 选择更便宜的酒店
        # 策略3: 减少高消费餐厅
        # 策略4: 减少付费景点

        # AI 生成优化建议
        prompt = f"""
        当前预算超支，请给出优化建议：

        当前总预算: {self.calculate_total(flights, hotels, itinerary)}
        目标预算: {target_budget}
        超支: {self.calculate_total(flights, hotels, itinerary) - target_budget}

        可选航班（价格从低到高）:
        {[f.price for f in flights.flights[:5]]}

        可选酒店（价格从低到高）:
        {[h.price for h in hotels.hotels[:5]]}

        请给出：
        1. 推荐的航班（编号）
        2. 推荐的酒店（编号）
        3. 行程优化建议（减少哪些高消费项目）

        返回 JSON
        """

        optimization = await self.gemini.generate(prompt)

        # 应用优化
        optimized_flight = flights.flights[optimization.flight_index]
        optimized_hotel = hotels.hotels[optimization.hotel_index]
        optimized_itinerary = self.apply_itinerary_optimization(
            itinerary,
            optimization.itinerary_changes
        )

        # 重新计算预算
        budget = self.calculate_budget(
            optimized_flight,
            optimized_hotel,
            optimized_itinerary,
            ...
        )

        return TravelPlan(
            flights=optimized_flight,
            hotels=optimized_hotel,
            itinerary=optimized_itinerary,
            budget=budget,
            optimization_applied=True,
            savings=self.calculate_total(...) - budget.total
        )
```

---

### 4. 报告生成模块 (Report Generator)

**职责**: 生成美观的旅游计划报告

```python
class TravelReportGenerator:
    """旅游报告生成器"""

    def generate_full_report(self, plan: TravelPlan) -> Report:
        """生成完整报告"""

        report = Report()

        # 1. 封面
        report.add_cover(plan.destination, plan.days)

        # 2. 概览
        report.add_section("行程概览", self._render_overview(plan))

        # 3. 交通方案
        report.add_section("✈️ 交通安排", self._render_flights(plan.flights))

        # 4. 住宿方案
        report.add_section("🏨 住宿安排", self._render_hotels(plan.hotels))

        # 5. 详细行程
        for day in plan.itinerary.days:
            report.add_section(
                f"Day {day.day}",
                self._render_day_itinerary(day)
            )

        # 6. 美食推荐
        report.add_section("🍜 美食推荐", self._render_food(plan))

        # 7. 预算明细
        report.add_section("💰 预算明细", self._render_budget(plan.budget))

        # 8. 实用信息
        report.add_section("📝 注意事项", self._render_tips(plan.tips))

        # 9. 预订链接
        report.add_section("🔗 快捷预订", self._render_booking_links(plan))

        return report

    def _render_overview(self, plan: TravelPlan) -> str:
        """渲染概览"""
        return f"""
## 行程概览

**目的地**: {plan.destination}
**旅行天数**: {plan.days}天{plan.days-1}夜
**总预算**: ¥{plan.budget.total:,.0f} ({plan.num_people}人)
**人均**: ¥{plan.budget.total/plan.num_people:,.0f}

**行程亮点**:
{chr(10).join(f"- {h}" for h in plan.highlights[:5])}
"""

    def _render_day_itinerary(self, day: DayItinerary) -> str:
        """渲染单日行程"""

        return f"""
### Day {day.day}: {day.theme}

**上午** ({day.morning.time})
📍 **{day.morning.attraction}**
- 游玩时长: {day.morning.duration}
- 门票: ¥{day.morning.ticket_price}
- 亮点: {', '.join(day.morning.highlights)}
- 💡 {day.morning.tips}

**午餐** ({day.lunch.time})
🍽️ **{day.lunch.restaurant}**
- 菜系: {day.lunch.cuisine}
- 人均: ¥{day.lunch.average_cost}
- 推荐: {', '.join(day.lunch.recommended_dishes)}

**下午** ({day.afternoon.time})
📍 **{day.afternoon.attraction}**
...

**晚餐** ({day.dinner.time})
🍽️ **{day.dinner.restaurant}**
...

---
**今日预算**: ¥{day.total_cost}
**今日步数**: 约 {day.estimated_steps} 步
"""

    def export_to_pdf(self, report: Report) -> bytes:
        """导出 PDF"""

        # 使用 WeasyPrint
        html = report.to_html()
        pdf = weasyprint.HTML(string=html).write_pdf()
        return pdf

    def export_to_html(self, report: Report) -> str:
        """导出 HTML（带交互地图）"""

        template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ plan.destination }}旅游攻略</title>
    <style>
        body { font-family: -apple-system, sans-serif; }
        .day { border-left: 3px solid #FF2442; padding-left: 20px; margin: 20px 0; }
        .budget { background: #f5f5f5; padding: 20px; border-radius: 8px; }
    </style>
    <script src="https://webapi.amap.com/maps?v=2.0&key=YOUR_KEY"></script>
</head>
<body>
    {{ report.content }}

    <!-- 地图 -->
    <div id="map" style="width:100%; height:400px;"></div>
    <script>
        // 初始化地图
        var map = new AMap.Map('map');

        // 标注景点
        var markers = {{ plan.attractions_coords }};
        markers.forEach(m => {
            new AMap.Marker({ position: m.coords, map: map });
        });
    </script>
</body>
</html>
        """

        return jinja2.Template(template).render(report=report, plan=plan)
```

---

## AI 智能引擎

### Gemini 多模态应用

```python
class GeminiTravelAssistant:
    """Gemini 旅游助手"""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash-exp',
            temperature=0.3
        )

    async def analyze_guide_with_images(
        self,
        post: Post
    ) -> GuideAnalysis:
        """多模态分析攻略（文字+图片）"""

        # Gemini 支持图片输入
        prompt = f"""
        分析这篇旅游攻略：

        标题: {post.title}
        正文: {post.content}
        图片数量: {len(post.images)}

        请从图片中识别：
        1. 景点场景（自然风光/历史建筑/现代都市）
        2. 美食照片（菜品类型）
        3. 住宿环境（酒店/民宿风格）

        从文字中提取：
        1. 行程安排
        2. 预算信息
        3. 注意事项

        返回 JSON
        """

        # 多模态输入
        messages = [
            {"role": "user", "content": prompt}
        ]

        # 添加图片
        for img_url in post.images[:5]:  # 最多5张
            messages.append({
                "role": "user",
                "content": {
                    "type": "image_url",
                    "image_url": img_url
                }
            })

        result = await self.llm.ainvoke(messages)
        return GuideAnalysis(**json.loads(result.content))

    async def generate_personalized_plan(
        self,
        guide: DestinationGuide,
        user_profile: UserProfile
    ) -> PersonalizedPlan:
        """生成个性化计划"""

        prompt = f"""
        根据用户画像定制旅游计划：

        用户画像:
        - 年龄: {user_profile.age}
        - 兴趣: {user_profile.interests}
        - 旅行经验: {user_profile.experience}
        - 身体状况: {user_profile.physical_condition}
        - 预算偏好: {user_profile.budget_preference}

        目的地信息:
        {json.dumps(guide.dict(), ensure_ascii=False)}

        请生成个性化建议：
        1. 推荐景点（符合兴趣和体能）
        2. 行程节奏（考虑年龄和体力）
        3. 餐饮建议（考虑饮食偏好）
        4. 特别提示（健康、安全）
        """

        result = await self.llm.ainvoke(prompt)
        return PersonalizedPlan(**json.loads(result.content))
```

---

## 数据模型

### 核心数据结构

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional
from enum import Enum

# ============================================================
# 请求模型
# ============================================================

@dataclass
class PlanRequest:
    """规划请求"""
    destination: str           # 目的地
    from_city: str            # 出发城市
    start_date: date          # 开始日期
    end_date: date            # 结束日期
    days: int                 # 天数
    num_people: int           # 人数
    total_budget: float       # 总预算
    preferences: UserPreferences  # 偏好

@dataclass
class UserPreferences:
    """用户偏好"""
    interests: List[str]      # 兴趣: ["自然", "历史", "美食"]
    pace: str                 # 节奏: "relaxed" | "moderate" | "fast"
    budget_level: str         # 预算: "budget" | "moderate" | "luxury"
    accommodation_type: str   # 住宿: "hotel" | "hostel" | "airbnb"

# ============================================================
# 攻略数据
# ============================================================

@dataclass
class Attraction:
    """景点"""
    name: str
    location: str
    ticket_price: float
    visit_duration: str       # "2小时"
    highlights: List[str]
    tips: List[str]
    rating: float             # 评分
    mention_count: int        # 提及次数
    popularity_score: float   # 热度分数

@dataclass
class Restaurant:
    """餐厅"""
    name: str
    cuisine: str              # 菜系
    average_cost: float       # 人均消费
    recommended_dishes: List[str]
    location: str
    rating: float
    mention_count: int

@dataclass
class DestinationGuide:
    """目的地攻略汇总"""
    destination: str
    attractions: List[Attraction]
    restaurants: List[Restaurant]
    sample_routes: List[dict]
    tips: List[str]

# ============================================================
# 价格数据
# ============================================================

@dataclass
class Flight:
    """航班"""
    flight_no: str
    airline: str
    departure_time: datetime
    arrival_time: datetime
    duration: str             # "2h30m"
    price: float
    cabin_class: str          # "经济舱" | "商务舱"
    source: str               # "携程" | "去哪儿"

@dataclass
class Hotel:
    """酒店"""
    name: str
    location: str
    coords: dict              # {"lat": ..., "lng": ...}
    price: float              # 每晚价格
    rating: float
    facilities: List[str]
    distance_to_center: float # 距离市中心 km
    source: str

# ============================================================
# 行程数据
# ============================================================

@dataclass
class TimeSlot:
    """时间段活动"""
    time: str                 # "09:00-11:00"
    attraction: Optional[str]
    duration: str
    ticket_price: float
    highlights: List[str]
    tips: str

@dataclass
class Meal:
    """餐饮"""
    time: str
    restaurant: str
    cuisine: str
    average_cost: float
    recommended_dishes: List[str]

@dataclass
class DayItinerary:
    """单日行程"""
    day: int
    theme: str                # "古城文化之旅"
    morning: TimeSlot
    lunch: Meal
    afternoon: TimeSlot
    dinner: Meal
    evening: Optional[TimeSlot]
    notes: str
    total_cost: float
    estimated_steps: int      # 预计步数

@dataclass
class Itinerary:
    """完整行程"""
    days: List[DayItinerary]

# ============================================================
# 预算数据
# ============================================================

@dataclass
class Budget:
    """预算明细"""
    transport: float          # 交通
    accommodation: float      # 住宿
    food: float              # 餐饮
    tickets: float           # 门票
    other: float             # 其他
    total: float             # 总计

# ============================================================
# 最终计划
# ============================================================

@dataclass
class TravelPlan:
    """旅游计划"""
    destination: str
    days: int
    num_people: int
    flights: Flight
    hotels: Hotel
    itinerary: Itinerary
    budget: Budget
    highlights: List[str]
    tips: List[str]
    booking_links: dict       # 预订链接
    created_at: datetime
```

---

## 技术栈

### 完整技术栈

| 层次 | 技术选型 | 说明 |
|-----|---------|------|
| **前端** | React + TypeScript | Web UI |
| | 微信小程序 | 小程序端 |
| | Flutter | APP 端（可选） |
| **API** | FastAPI + GraphQL | REST + GraphQL |
| **业务层** | Python 3.11+ | 核心业务逻辑 |
| **AI** | Google Gemini 2.0 | 多模态 AI 分析 |
| | LangChain | LLM 应用框架 |
| **数据采集** | browser-use | 浏览器自动化 |
| | 携程/去哪儿 API | 官方 API（优先） |
| | 高德地图 API | 地图服务 |
| **数据库** | PostgreSQL | 主数据库 |
| | Redis | 缓存 + 队列 |
| | Qdrant | 向量数据库（攻略相似度） |
| | OSS/S3 | 图片存储 |
| **任务队列** | Celery + Redis | 异步任务 |
| **部署** | Docker + K8s | 容器化部署 |
| **监控** | Prometheus + Grafana | 性能监控 |

### 依赖清单

```txt
# requirements.txt

# Web 框架
fastapi==0.109.0
uvicorn[standard]==0.27.0
graphene==3.3
strawberry-graphql==0.219.0

# 数据采集
browser-use>=0.1.0
playwright==1.40.0
httpx==0.26.0

# AI
langchain-google-genai==1.0.0
google-generativeai==0.3.0

# 数据库
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
redis==5.0.1
qdrant-client==1.7.0

# 任务队列
celery==5.3.6

# 数据处理
pandas==2.1.4
numpy==1.26.3

# 地图和路线
aiohttp==3.9.1  # 高德地图 API

# 报告生成
jinja2==3.1.3
weasyprint==60.2
pillow==10.2.0

# 工具
python-dotenv==1.0.0
pydantic==2.5.0
```

---

## 实现流程

### 完整流程图

```
用户输入
  ↓
┌─────────────────────────────────────────┐
│ 1. 参数验证                             │
│ - 日期合法性                            │
│ - 预算合理性                            │
│ - 城市代码转换                          │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 2. 数据收集（并行）                     │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│ │小红书   │ │携程机票 │ │携程酒店 │   │
│ │攻略收集 │ │价格查询 │ │价格查询 │   │
│ └─────────┘ └─────────┘ └─────────┘   │
│      ↓           ↓           ↓         │
│ AI提取信息   排序筛选   排序筛选       │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 3. 数据聚合                             │
│ - 景点去重和排序                        │
│ - 餐厅去重和排序                        │
│ - 航班价格对比                          │
│ - 酒店性价比计算                        │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 4. AI 行程规划                          │
│ - 根据天数分配景点                      │
│ - 优化路线顺序（TSP）                   │
│ - 安排餐饮                              │
│ - 计算时间和距离                        │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 5. 预算计算                             │
│ - 交通费用                              │
│ - 住宿费用                              │
│ - 餐饮费用                              │
│ - 门票费用                              │
│ - 其他费用                              │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 6. 预算优化（如超支）                   │
│ - 调整航班/酒店档次                     │
│ - 优化餐饮安排                          │
│ - 减少付费景点                          │
│ - 给出多种方案                          │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 7. 报告生成                             │
│ - HTML 交互版（含地图）                 │
│ - PDF 打印版                            │
│ - JSON 数据版                           │
│ - 小程序分享版                          │
└─────────────────────────────────────────┘
  ↓
返回给用户
```

### API 调用示例

```python
# API 请求
POST /api/v1/travel/plan

{
  "destination": "成都",
  "from_city": "北京",
  "start_date": "2025-05-01",
  "end_date": "2025-05-05",
  "num_people": 2,
  "total_budget": 10000,
  "preferences": {
    "interests": ["美食", "文化", "自然"],
    "pace": "moderate",
    "budget_level": "moderate",
    "accommodation_type": "hotel"
  }
}

# API 响应
{
  "plan_id": "uuid",
  "status": "completed",
  "plan": {
    "destination": "成都",
    "days": 5,
    "flights": {...},
    "hotels": {...},
    "itinerary": {
      "days": [...]
    },
    "budget": {
      "transport": 2660,
      "accommodation": 2800,
      "food": 1200,
      "tickets": 500,
      "other": 500,
      "total": 7660
    },
    "highlights": [...],
    "tips": [...]
  },
  "report_urls": {
    "html": "https://example.com/report/uuid.html",
    "pdf": "https://example.com/report/uuid.pdf"
  }
}
```

---

## 可行性分析

### 技术可行性 ⭐⭐⭐⭐⭐

| 模块 | 可行性 | 说明 |
|-----|--------|------|
| **小红书攻略收集** | ✅ 完全可行 | 已有成熟实现（xiaohongshu_collector.py） |
| **携程价格查询** | ✅ 可行 | 官方 API（需申请）或浏览器自动化 |
| **AI 分析** | ✅ 完全可行 | Gemini 2.0 多模态能力强大 |
| **行程规划** | ✅ 完全可行 | AI 生成 + 算法优化 |
| **预算计算** | ✅ 完全可行 | 简单数学计算 |
| **报告生成** | ✅ 完全可行 | Jinja2 + WeasyPrint |

**总体评估**: 技术上完全可行，核心模块都有成熟方案

---

### 商业可行性 ⭐⭐⭐⭐⭐

**市场需求**:
- ✅ 旅游规划是刚需
- ✅ 用户痛点明确（信息分散、规划麻烦）
- ✅ 愿意为便利性付费

**竞品分析**:

| 产品 | 优势 | 劣势 |
|-----|------|------|
| **马蜂窝** | 内容丰富 | 需要手动整理 |
| **穷游** | 路线多 | 价格不实时 |
| **携程** | 预订方便 | 攻略质量一般 |
| **我们的产品** | AI 自动化 + 实时价格 + 完整规划 | 新产品需要推广 |

**差异化**:
1. 🔥 **AI 自动化**: 一键生成完整计划
2. 🔥 **实时价格**: 携程等平台实时查询
3. 🔥 **真实攻略**: 小红书用户真实分享
4. 🔥 **预算优化**: 自动控制和优化预算
5. 🔥 **一站式**: 从攻略到预订全流程

**商业模式**:
1. **免费版**: 基础规划（有广告）
2. **会员版**: ¥19.9/月 或 ¥99/年
   - 无限次规划
   - 无广告
   - PDF 导出
   - 价格预警
3. **企业版**: 定制化服务
4. **佣金模式**: 携程/去哪儿返佣

**估算收益**:
- 用户规模: 10万（第一年）
- 转化率: 5% → 5000 付费用户
- 客单价: ¥100/年
- 年收入: ¥50万
- 加上佣金: ¥80-100万

---

### 开发成本 ⭐⭐⭐

**人力成本**:
- 后端开发: 1人 × 2个月
- 前端开发: 1人 × 1个月
- UI设计: 0.5人 × 1个月
- 测试: 0.5人 × 1个月

**总计**: 约 3-4 人月

**技术成本**:
- Gemini API: ¥1000/月（初期）
- 服务器: ¥500/月
- 数据库: ¥300/月
- 携程 API: 看调用量
- **总计**: ¥2000-3000/月

**开发周期**: 2-3个月 MVP

---

## 挑战与解决方案

### 挑战1: 携程反爬虫 ⚠️

**问题**: 携程有严格的反爬虫机制

**解决方案**:
1. **优先使用官方 API**（需要申请企业账号）
2. **Browser Use Cloud**（官方云浏览器，绕过反爬虫）
3. **IP 轮换 + 请求限速**（降级方案）
4. **缓存策略**（减少请求频率）

```python
# 多策略获取价格
async def get_flight_price(self, ...):
    try:
        # 策略1: 官方 API
        return await self.ctrip_api.search_flights(...)
    except:
        try:
            # 策略2: Browser Use Cloud
            return await self.browser_cloud.search_flights(...)
        except:
            # 策略3: 缓存数据（可能不是最新）
            return await self.cache.get_cached_flights(...)
```

---

### 挑战2: AI 理解准确性 ⚠️

**问题**: AI 提取的信息可能不准确

**解决方案**:
1. **多帖子验证**（同一景点出现在多篇攻略中）
2. **置信度评分**（AI 给出置信度）
3. **人工校验**（重要信息人工审核）
4. **用户反馈**（用户纠错）

```python
# 景点信息验证
def verify_attraction(self, attr: Attraction, all_posts: List[Post]) -> Attraction:
    # 统计提及次数
    mentions = sum(1 for p in all_posts if attr.name in p.content)

    # 置信度 = 提及次数 / 总帖子数
    attr.confidence = mentions / len(all_posts)

    # 低于阈值标记为"需要验证"
    if attr.confidence < 0.3:
        attr.need_verify = True

    return attr
```

---

### 挑战3: 实时性要求 ⚠️

**问题**: 价格变化快，需要实时查询

**解决方案**:
1. **智能缓存**（不同时段不同缓存时长）
2. **价格预警**（价格变化时通知用户）
3. **异步更新**（后台更新缓存）

```python
# 智能缓存策略
def get_cache_ttl(self, query_date: date) -> int:
    days_until = (query_date - date.today()).days

    if days_until < 7:
        return 1800   # 30分钟（临近出发，频繁更新）
    elif days_until < 30:
        return 3600   # 1小时
    else:
        return 7200   # 2小时（提前很久，不常更新）
```

---

### 挑战4: 路线优化复杂度 ⚠️

**问题**: TSP 问题是 NP-hard，景点多时计算慢

**解决方案**:
1. **限制景点数量**（每天最多 3-4 个景点）
2. **贪心算法**（近似解，速度快）
3. **预计算**（常见路线预计算）

```python
# 贪心 TSP（O(n²)）
def optimize_route(self, attractions: List[Attraction]) -> List[Attraction]:
    if len(attractions) <= 3:
        # 少于3个，暴力枚举
        return self.brute_force_tsp(attractions)
    else:
        # 贪心算法
        return self.greedy_tsp(attractions)
```

---

## 开发路线图

### MVP 版本（1个月）⭐

**核心功能**:
- ✅ 小红书攻略收集
- ✅ AI 信息提取
- ✅ 携程价格查询（浏览器自动化）
- ✅ 简单行程生成
- ✅ 预算计算
- ✅ HTML 报告导出

**技术栈**:
- Python FastAPI
- browser-use
- Gemini AI
- SQLite（简化）

**产品形态**: CLI 工具 + 简单 Web UI

---

### V1.0 版本（2个月）⭐⭐

**新增功能**:
- ✅ 携程官方 API 集成
- ✅ 去哪儿价格对比
- ✅ 高德地图路线优化
- ✅ PDF 报告导出
- ✅ 多方案生成
- ✅ Web UI 完整版
- ✅ 用户系统（登录、保存计划）

**技术升级**:
- PostgreSQL
- Redis 缓存
- Celery 异步任务

---

### V2.0 版本（3-4个月）⭐⭐⭐

**新增功能**:
- ✅ 微信小程序
- ✅ 价格预警
- ✅ 行程分享
- ✅ 智能推荐（基于历史）
- ✅ 多人协作规划
- ✅ 预订跳转（携程/去哪儿）

**技术升级**:
- 向量数据库（相似攻略推荐）
- 用户画像系统
- 推荐算法

---

### V3.0 版本（长期）⭐⭐⭐⭐

**新增功能**:
- ✅ APP 版本（Flutter）
- ✅ 国际版（境外旅游）
- ✅ AI 语音助手
- ✅ AR 导览
- ✅ 社区分享（用户攻略）

---

## 项目结构

```
travel-ai-planner/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   │   ├── travel.py          # 旅游规划 API
│   │   │   ├── guides.py          # 攻略 API
│   │   │   └── prices.py          # 价格 API
│   │   ├── services/
│   │   │   ├── guide_collector.py # 攻略收集
│   │   │   ├── price_query.py     # 价格查询
│   │   │   ├── ai_planner.py      # AI 规划
│   │   │   └── report_gen.py      # 报告生成
│   │   ├── models/
│   │   ├── utils/
│   │   └── tasks.py               # Celery 任务
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── web/                        # Web UI
│   ├── miniapp/                    # 微信小程序
│   └── app/                        # Flutter APP
├── docs/
│   ├── ARCHITECTURE.md             # 本文档
│   ├── API.md
│   └── DEPLOYMENT.md
├── docker-compose.yml
└── README.md
```

---

## 总结

### 核心优势

1. ✅ **技术可行**: 80% 代码可复用现有项目
2. ✅ **AI 驱动**: Gemini 多模态分析能力强
3. ✅ **用户价值**: 解决真实痛点（信息分散、规划麻烦）
4. ✅ **差异化**: AI 自动化 + 实时价格 + 完整规划
5. ✅ **商业潜力**: 刚需市场，变现路径清晰

### 关键指标

| 指标 | 评估 |
|-----|------|
| 技术可行性 | ⭐⭐⭐⭐⭐ |
| 商业价值 | ⭐⭐⭐⭐⭐ |
| 开发难度 | ⭐⭐⭐ |
| 开发周期 | 1个月 MVP，2-3个月完整版 |
| 投入成本 | 中等（3-4人月 + ¥2-3k/月运营） |
| 市场潜力 | ⭐⭐⭐⭐⭐ |

### 下一步行动

1. **MVP 验证**（1个月）
   - 实现核心功能
   - 小范围测试
   - 收集用户反馈

2. **产品迭代**（2-3个月）
   - 完善功能
   - 优化体验
   - 扩大用户

3. **商业化**（3个月后）
   - 会员体系
   - 佣金合作
   - 企业服务

---

**这是一个非常有潜力的项目！** 🚀

需要我帮你开始搭建 MVP 吗？

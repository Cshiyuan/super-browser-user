#!/usr/bin/env python3
"""
基础使用示例

演示如何使用项目的核心功能：
1. 创建和操作领域模型
2. 使用仓储存储数据
3. 使用 AI 客户端（需要 API 密钥）

运行方式：
    uv run python examples/basic_usage.py
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入领域模型
from src.core.domain.models.post import PostDetail
from src.core.domain.models.user import UserProfile
from src.core.domain.models.travel import TravelPlan, Itinerary, DayPlan, Activity, Budget

# 导入仓储
from src.core.repositories.post_repository import InMemoryPostRepository

# 导入 AI 客户端
from src.infrastructure.external.ai.gemini_client import GeminiClient


def example_1_domain_models():
    """
    示例 1: 使用领域模型

    演示如何创建和使用帖子、用户、旅行计划等模型。
    """
    print("=" * 60)
    print("示例 1: 领域模型使用")
    print("=" * 60)

    # 创建帖子
    post = PostDetail(
        post_id="demo_001",
        url="https://example.com/demo",
        title="成都三日游攻略",
        content="详细的成都旅游攻略，包含宽窄巷子、锦里、熊猫基地等景点。推荐美食：火锅、串串、龙抄手。",
        author="旅行达人小王",
        likes=1500,
        comments=89,
        collects=320,
        images=["img1.jpg", "img2.jpg"],
        tags=["成都", "旅游", "美食", "四川"],
        publish_time="2025-01-01",
        location="成都"
    )

    print(f"\n📝 帖子信息:")
    print(f"  标题: {post.title}")
    print(f"  作者: {post.author}")
    print(f"  点赞: {post.likes}, 评论: {post.comments}, 收藏: {post.collects}")
    print(f"  互动率: {post.engagement_rate:.2%}")
    print(f"  标签: {', '.join(post.tags)}")

    # 创建用户资料
    user = UserProfile(
        user_id="user_001",
        username="旅行达人小王",
        bio="专注旅游攻略分享，已走过30+城市",
        followers=15000,
        following=500,
        posts_count=180,
        likes_count=85000,
        verified=True
    )

    print(f"\n👤 用户信息:")
    print(f"  用户名: {user.username}")
    print(f"  粉丝数: {user.followers:,}")
    print(f"  发帖数: {user.posts_count}")
    print(f"  认证: {'是' if user.verified else '否'}")
    print(f"  影响力评分: {user.influence_score:,.2f}")

    # 创建旅行计划
    activities = [
        Activity(
            time="09:00",
            type="景点",
            name="宽窄巷子",
            duration=120,
            description="游览成都老街，体验悠闲的成都生活"
        ),
        Activity(
            time="12:00",
            type="餐饮",
            name="龙抄手总店",
            duration=60,
            description="品尝成都经典小吃"
        ),
        Activity(
            time="14:00",
            type="景点",
            name="锦里古街",
            duration=180,
            description="探索三国文化，购买特色纪念品"
        )
    ]

    day1 = DayPlan(
        day=1,
        date="2025-01-20",
        activities=activities
    )

    itinerary = Itinerary(
        destination="成都",
        days=1,
        day_plans=[day1]
    )

    budget = Budget(
        transportation=300.0,
        accommodation=400.0,
        food=200.0,
        tickets=100.0,
        shopping=150.0,
        other=50.0
    )

    travel_plan = TravelPlan(
        plan_id="plan_001",
        user_id="user_001",
        destination="成都",
        days=1,
        itinerary=itinerary,
        budget=budget
    )

    print(f"\n✈️ 旅行计划:")
    print(f"  目的地: {travel_plan.destination}")
    print(f"  天数: {travel_plan.days} 天")
    print(f"  活动总数: {travel_plan.itinerary.total_activities}")
    print(f"  预算总额: ¥{travel_plan.budget.total:,.2f}")
    print(f"  状态: {travel_plan.status}")

    print(f"\n  第 {day1.day} 天行程 ({day1.date}):")
    for activity in day1.activities:
        print(f"    {activity.time} | {activity.type:4s} | {activity.name} ({activity.duration}分钟)")


async def example_2_repository():
    """
    示例 2: 使用仓储存储和查询数据

    演示如何使用 Repository 模式管理数据。
    """
    print("\n" + "=" * 60)
    print("示例 2: 数据仓储使用")
    print("=" * 60)

    # 创建仓储实例
    repo = InMemoryPostRepository()

    # 创建一些测试帖子
    posts_data = [
        ("成都三日游攻略", "成都", 1500, 89, 320),
        ("北京故宫深度游", "北京", 2800, 156, 540),
        ("上海外滩夜景", "上海", 1200, 67, 210),
        ("成都美食地图", "成都", 3200, 234, 890),
        ("杭州西湖散步", "杭州", 980, 45, 167),
    ]

    print("\n💾 保存帖子到仓储...")
    for i, (title, location, likes, comments, collects) in enumerate(posts_data, 1):
        post = PostDetail(
            post_id=f"post_{i:03d}",
            url=f"https://example.com/post/{i}",
            title=title,
            content=f"这是一篇关于{location}的精彩攻略...",
            author=f"作者{i}",
            likes=likes,
            comments=comments,
            collects=collects,
            images=[],
            tags=[location, "旅游"]
        )
        await repo.save(post)
        print(f"  ✓ 已保存: {title} (ID: {post.post_id})")

    # 按目的地查询
    print("\n🔍 查询成都相关的帖子:")
    chengdu_posts = await repo.find_by_destination("成都", limit=10)
    for post in chengdu_posts:
        print(f"  • {post.title} - 互动率: {post.engagement_rate:.2%}")

    # 查询高质量帖子
    print("\n⭐ 查询高质量帖子 (互动率 >= 1.2):")
    high_quality = await repo.find_high_quality(min_engagement_rate=1.2)
    for post in high_quality:
        print(f"  • {post.title} - 互动率: {post.engagement_rate:.2%}")

    # 删除帖子
    print("\n🗑️  删除帖子:")
    deleted = await repo.delete("post_001")
    print(f"  删除 post_001: {'成功' if deleted else '失败'}")

    # 验证删除
    found = await repo.find_by_id("post_001")
    print(f"  查找 post_001: {'存在' if found else '不存在'}")


async def example_3_ai_client():
    """
    示例 3: 使用 AI 客户端

    演示如何使用 Gemini AI 进行文本处理。
    需要设置 GEMINI_API_KEY 环境变量。
    """
    print("\n" + "=" * 60)
    print("示例 3: AI 客户端使用")
    print("=" * 60)

    # 检查 API 密钥
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n⚠️  未设置 GEMINI_API_KEY 环境变量")
        print("  跳过 AI 客户端示例")
        print("\n  如需运行此示例，请设置环境变量：")
        print("  export GEMINI_API_KEY='your_api_key_here'")
        return

    print("\n🤖 初始化 AI 客户端...")
    client = GeminiClient()

    # 示例 1: 简单聊天
    print("\n💬 简单聊天测试:")
    print("  问题: 用一句话介绍成都")
    response = await client.chat("用一句话介绍成都")
    print(f"  回答: {response}")

    # 示例 2: 提取结构化数据
    print("\n📊 提取结构化数据:")
    攻略文本 = """
    成都三日游推荐：
    第一天去宽窄巷子和锦里，感受老成都的韵味。
    第二天前往熊猫基地看可爱的大熊猫，下午逛春熙路购物。
    第三天去青城山或都江堰，享受自然风光。

    美食推荐：火锅、串串、龙抄手、钟水饺、夫妻肺片。
    """

    print("  原文本:", 攻略文本[:50] + "...")
    attractions = await client.extract_attractions(攻略文本)
    print(f"  提取的景点: {attractions}")

    restaurants = await client.extract_restaurants(攻略文本)
    print(f"  提取的美食: {restaurants}")


async def main():
    """主函数"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          Super Browser User - 基础使用示例                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # 运行示例
    example_1_domain_models()
    await example_2_repository()
    await example_3_ai_client()

    print("\n" + "=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)
    print("\n📚 更多信息:")
    print("  - API 文档: docs/api/API_DESIGN.md")
    print("  - 开发指南: docs/development/SETUP.md")
    print("  - 架构文档: docs/architecture/ARCHITECTURE.md")
    print()


if __name__ == "__main__":
    asyncio.run(main())

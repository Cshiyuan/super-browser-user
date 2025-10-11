#!/usr/bin/env python3
"""
完整工作流示例

演示从攻略收集到行程生成的完整流程：
1. 收集旅游攻略（模拟数据）
2. 使用 AI 提取信息
3. 生成旅行计划
4. 保存到仓储

运行方式：
    uv run python examples/complete_workflow.py
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
from src.core.domain.models.travel import TravelPlan, Budget

# 导入服务
from src.core.services.guide_collector import GuideCollectorService
from src.core.services.itinerary_generator import ItineraryGeneratorService

# 导入仓储
from src.core.repositories.post_repository import InMemoryPostRepository
from src.core.repositories.travel_repository import InMemoryTravelPlanRepository

# 导入 AI 客户端
from src.infrastructure.external.ai.gemini_client import GeminiClient


def print_header(title: str):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def create_mock_guides() -> list[PostDetail]:
    """创建模拟攻略数据（用于演示）"""
    return [
        PostDetail(
            post_id="guide_001",
            url="https://example.com/chengdu/1",
            title="成都三日游完整攻略",
            content="""
            成都必去景点推荐：
            1. 宽窄巷子：感受老成都的韵味，建议游玩2小时
            2. 锦里古街：三国文化主题，晚上最美，3小时
            3. 熊猫基地：看可爱的大熊猫，上午最佳，3小时
            4. 都江堰：世界文化遗产，半天行程

            美食推荐：
            - 龙抄手总店：经典成都小吃
            - 陈麻婆豆腐：百年老店
            - 小龙坎火锅：地道成都火锅

            交通：地铁很方便，建议购买天府通卡
            住宿：春熙路附近交通便利
            """,
            author="旅行达人小王",
            likes=5800,
            comments=342,
            collects=1200,
            images=["img1.jpg", "img2.jpg", "img3.jpg"],
            tags=["成都", "旅游", "攻略", "美食"],
            publish_time="2025-01-15",
            location="成都"
        ),
        PostDetail(
            post_id="guide_002",
            url="https://example.com/chengdu/2",
            title="成都美食地图",
            content="""
            成都美食推荐：

            火锅类：
            - 大龙燚火锅：排队神店
            - 蜀大侠火锅：环境好味道赞

            小吃类：
            - 钟水饺：百年老字号
            - 夫妻肺片：必尝名菜
            - 担担面：成都特色

            茶馆：
            - 人民公园茶馆：最地道的成都生活
            """,
            author="美食探店君",
            likes=3200,
            comments=189,
            collects=850,
            images=["food1.jpg", "food2.jpg"],
            tags=["成都", "美食", "小吃", "火锅"],
            publish_time="2025-01-18",
            location="成都"
        ),
        PostDetail(
            post_id="guide_003",
            url="https://example.com/chengdu/3",
            title="成都周边一日游",
            content="""
            成都周边景点：

            都江堰：
            - 距离成都1小时车程
            - 世界文化遗产
            - 建议游玩4小时

            青城山：
            - 道教名山
            - 可以和都江堰一起游玩
            - 建议预留一整天

            乐山大佛：
            - 距离成都2小时车程
            - 需要爬山，准备好体力
            """,
            author="周边游专家",
            likes=2100,
            comments=98,
            collects=420,
            images=["dujiangyan.jpg"],
            tags=["成都", "周边游", "都江堰", "青城山"],
            publish_time="2025-01-20",
            location="成都"
        )
    ]


async def example_1_collect_guides():
    """
    示例 1: 收集攻略（使用模拟数据）

    在实际应用中，这里会调用 GuideCollectorService
    使用 browser-use 从小红书收集真实攻略。
    """
    print_header("步骤 1: 收集旅游攻略")

    # 创建模拟攻略数据
    guides = create_mock_guides()

    print(f"✓ 成功收集 {len(guides)} 篇攻略\n")

    for guide in guides:
        print(f"📝 {guide.title}")
        print(f"   作者: {guide.author}")
        print(f"   互动: 👍 {guide.likes}  💬 {guide.comments}  ⭐ {guide.collects}")
        print(f"   互动率: {guide.engagement_rate:.2%}")
        print()

    return guides


async def example_2_save_to_repository(guides: list[PostDetail]):
    """
    示例 2: 保存到仓储
    """
    print_header("步骤 2: 保存攻略到仓储")

    repo = InMemoryPostRepository()

    for guide in guides:
        await repo.save(guide)
        print(f"✓ 已保存: {guide.title}")

    # 查询高质量攻略
    high_quality = await repo.find_high_quality(min_engagement_rate=0.08)
    print(f"\n筛选出 {len(high_quality)} 篇高质量攻略")

    return repo


async def example_3_generate_itinerary(guides: list[PostDetail]):
    """
    示例 3: 生成旅行计划
    """
    print_header("步骤 3: 生成旅行计划")

    # 检查是否有 AI 客户端
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✓ 检测到 GEMINI_API_KEY，将使用 AI 提取信息")
        ai_client = GeminiClient()
    else:
        print("⚠️  未设置 GEMINI_API_KEY，将使用关键词提取")
        ai_client = None

    # 创建行程生成服务
    generator = ItineraryGeneratorService(ai_client=ai_client)

    # 生成3天行程
    print("\n正在生成成都 3 天行程...")
    itinerary = await generator.generate_itinerary(
        destination="成都",
        days=3,
        guides=guides,
        preferences={
            "budget": "中等",
            "interests": ["文化", "美食", "自然"]
        }
    )

    print(f"✓ 行程生成完成\n")

    # 显示行程详情
    print(f"目的地: {itinerary.destination}")
    print(f"天数: {itinerary.days} 天")
    print(f"活动总数: {itinerary.total_activities}\n")

    for day_plan in itinerary.day_plans:
        print(f"第 {day_plan.day} 天 ({day_plan.date}):")
        for activity in day_plan.activities:
            print(f"  {activity.time} | {activity.type:4s} | {activity.name} ({activity.duration}分钟)")
            if activity.description:
                print(f"           └─ {activity.description}")
        print()

    # 计算总成本
    total_cost = generator.calculate_total_cost(itinerary)
    print(f"预估总成本: ¥{total_cost:,.2f}")

    return itinerary


async def example_4_create_travel_plan(itinerary):
    """
    示例 4: 创建完整的旅行计划
    """
    print_header("步骤 4: 创建完整旅行计划")

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
    travel_plan = TravelPlan(
        plan_id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        user_id="demo_user",
        destination=itinerary.destination,
        days=itinerary.days,
        itinerary=itinerary,
        budget=budget
    )

    print(f"✓ 旅行计划创建完成\n")
    print(f"计划 ID: {travel_plan.plan_id}")
    print(f"用户 ID: {travel_plan.user_id}")
    print(f"状态: {travel_plan.status}")
    print(f"创建时间: {travel_plan.created_at}")

    print(f"\n预算明细:")
    print(f"  交通: ¥{budget.transportation:,.2f}")
    print(f"  住宿: ¥{budget.accommodation:,.2f}")
    print(f"  餐饮: ¥{budget.food:,.2f}")
    print(f"  门票: ¥{budget.tickets:,.2f}")
    print(f"  购物: ¥{budget.shopping:,.2f}")
    print(f"  其他: ¥{budget.other:,.2f}")
    print(f"  ────────────────")
    print(f"  总计: ¥{budget.total:,.2f}")

    return travel_plan


async def example_5_save_travel_plan(travel_plan: TravelPlan):
    """
    示例 5: 保存旅行计划
    """
    print_header("步骤 5: 保存旅行计划")

    repo = InMemoryTravelPlanRepository()

    await repo.save(travel_plan)
    print(f"✓ 旅行计划已保存到仓储")

    # 验证保存
    saved_plan = await repo.find_by_id(travel_plan.plan_id)
    if saved_plan:
        print(f"✓ 验证成功: 可以通过 ID {travel_plan.plan_id} 查询到计划")

    # 按目的地查询
    plans_by_dest = await repo.find_by_destination(travel_plan.destination)
    print(f"✓ 成都相关的旅行计划: {len(plans_by_dest)} 个")

    return repo


async def main():
    """主函数"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     Super Browser User - 完整工作流演示                      ║")
    print("║     从攻略收集到旅行计划生成                                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    try:
        # 步骤 1: 收集攻略
        guides = await example_1_collect_guides()

        # 步骤 2: 保存到仓储
        post_repo = await example_2_save_to_repository(guides)

        # 步骤 3: 生成行程
        itinerary = await example_3_generate_itinerary(guides)

        # 步骤 4: 创建旅行计划
        travel_plan = await example_4_create_travel_plan(itinerary)

        # 步骤 5: 保存旅行计划
        plan_repo = await example_5_save_travel_plan(travel_plan)

        # 完成
        print_header("✅ 完整工作流执行成功")

        print("📊 总结:")
        print(f"  • 收集攻略: {len(guides)} 篇")
        print(f"  • 生成行程: {itinerary.days} 天，{itinerary.total_activities} 个活动")
        print(f"  • 预算总额: ¥{travel_plan.budget.total:,.2f}")
        print(f"  • 计划状态: {travel_plan.status}")

        print("\n💡 提示:")
        print("  1. 设置 GEMINI_API_KEY 可以使用 AI 提取更准确的信息")
        print("  2. 修改 create_mock_guides() 可以自定义攻略内容")
        print("  3. 查看 examples/basic_usage.py 了解各模块的详细用法")

    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

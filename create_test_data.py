#!/usr/bin/env python3
"""
创建测试数据

快速生成一些测试数据，方便测试 Web 界面。
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.core.domain.models.post import PostDetail
from src.core.domain.models.travel import TravelPlan, Itinerary, DayPlan, Activity, Budget
from src.storage.local_storage import LocalStorage


def create_test_posts():
    """创建测试攻略"""
    posts = [
        PostDetail(
            post_id="test_001",
            url="https://www.xiaohongshu.com/test/001",
            title="成都三日游攻略 - 美食与文化之旅",
            content="成都是一座充满魅力的城市，这里有美味的火锅、可爱的大熊猫，还有悠闲的生活节奏。\n\n第一天：宽窄巷子 → 人民公园 → 锦里\n第二天：大熊猫基地 → 春熙路购物\n第三天：武侯祠 → 杜甫草堂",
            author="旅行达人小王",
            likes=1200,
            comments=85,
            collects=320,
            tags=["成都", "美食", "三日游", "熊猫"],
            location="成都",
            publish_time="2024-09-15"
        ),
        PostDetail(
            post_id="test_002",
            url="https://www.xiaohongshu.com/test/002",
            title="成都美食探店 - 10家必吃餐厅",
            content="作为美食之都，成都有太多好吃的了！整理了10家必去的餐厅：\n\n1. 小龙坎火锅\n2. 陈麻婆豆腐\n3. 龙抄手\n4. 钟水饺\n5. 廖记棒棒鸡",
            author="美食博主Lisa",
            likes=2300,
            comments=156,
            collects=680,
            tags=["成都", "美食", "火锅", "探店"],
            location="成都",
            publish_time="2024-09-20"
        ),
        PostDetail(
            post_id="test_003",
            url="https://www.xiaohongshu.com/test/003",
            title="周末去成都看熊猫 - 一日游攻略",
            content="周末去了趟成都大熊猫基地，太可爱了！\n\n最佳时间：早上8-10点，熊猫最活跃\n门票：55元/人\n交通：地铁3号线到熊猫大道站",
            author="户外达人Mike",
            likes=890,
            comments=45,
            collects=210,
            tags=["成都", "熊猫", "一日游", "周末"],
            location="成都",
            publish_time="2024-09-25"
        )
    ]
    return posts


def create_test_plan():
    """创建测试旅行计划"""
    # 创建活动
    day1_activities = [
        Activity(
            time="09:00",
            type="景点",
            name="宽窄巷子",
            duration="2小时",
            description="感受成都传统建筑风格，品尝当地小吃",
            cost=50.0
        ),
        Activity(
            time="12:00",
            type="美食",
            name="小龙坎火锅",
            duration="1.5小时",
            description="品尝正宗成都火锅",
            cost=120.0
        ),
        Activity(
            time="14:30",
            type="景点",
            name="人民公园",
            duration="2小时",
            description="体验成都慢生活，喝盖碗茶",
            cost=30.0
        ),
        Activity(
            time="18:00",
            type="美食",
            name="锦里小吃街",
            duration="2小时",
            description="品尝各种成都小吃",
            cost=80.0
        )
    ]

    day2_activities = [
        Activity(
            time="08:00",
            type="景点",
            name="成都大熊猫基地",
            duration="3小时",
            description="观看可爱的大熊猫，最佳时间是早上",
            cost=55.0
        ),
        Activity(
            time="12:00",
            type="美食",
            name="陈麻婆豆腐",
            duration="1小时",
            description="品尝百年老店",
            cost=80.0
        ),
        Activity(
            time="14:00",
            type="购物",
            name="春熙路",
            duration="3小时",
            description="成都最繁华的商业街",
            cost=200.0
        )
    ]

    day3_activities = [
        Activity(
            time="09:00",
            type="景点",
            name="武侯祠",
            duration="2小时",
            description="三国文化圣地",
            cost=50.0
        ),
        Activity(
            time="12:00",
            type="美食",
            name="龙抄手",
            duration="1小时",
            description="品尝成都传统小吃",
            cost=60.0
        ),
        Activity(
            time="14:00",
            type="景点",
            name="杜甫草堂",
            duration="2小时",
            description="诗圣杜甫的故居",
            cost=50.0
        )
    ]

    # 创建日计划
    day_plans = [
        DayPlan(day=1, date="2024-10-10", activities=day1_activities),
        DayPlan(day=2, date="2024-10-11", activities=day2_activities),
        DayPlan(day=3, date="2024-10-12", activities=day3_activities)
    ]

    # 创建行程
    itinerary = Itinerary(
        destination="成都",
        days=3,
        day_plans=day_plans
    )

    # 创建预算
    budget = Budget(
        transportation=300.0,
        accommodation=900.0,
        food=600.0,
        tickets=300.0,
        shopping=200.0,
        other=150.0
    )

    # 创建旅行计划
    plan = TravelPlan(
        plan_id="test_plan_001",
        user_id="test_user",
        destination="成都",
        days=3,
        itinerary=itinerary,
        budget=budget,
        status="draft",
        created_at=datetime.now()
    )

    return plan


def main():
    print("=" * 60)
    print("🎨 创建测试数据")
    print("=" * 60)
    print()

    storage = LocalStorage()

    # 创建测试攻略
    print("📝 创建测试攻略...")
    posts = create_test_posts()
    for post in posts:
        storage.save_post(post)
        print(f"  ✓ {post.title}")

    # 创建测试旅行计划
    print()
    print("🗺️ 创建测试旅行计划...")
    plan = create_test_plan()
    storage.save_plan(plan)
    print(f"  ✓ {plan.destination} {plan.days} 天行程")

    print()
    print("=" * 60)
    print("✅ 测试数据创建完成！")
    print("=" * 60)
    print()
    print(f"攻略数量: {len(posts)}")
    print(f"旅行计划: 1 个")
    print()
    print("下一步:")
    print("  运行 'uv run python run_mvp.py' 启动 Web 应用")
    print("  访问 http://localhost:8000 查看数据")
    print()


if __name__ == "__main__":
    main()

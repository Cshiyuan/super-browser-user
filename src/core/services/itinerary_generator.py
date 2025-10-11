"""
行程生成服务
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from ...core.domain.models.travel import (
    TravelPlan, Itinerary, DayPlan, Activity, Budget
)
from ...core.domain.models.post import PostDetail
from ...infrastructure.utils.logger import setup_logger


logger = setup_logger(__name__)


class ItineraryGeneratorService:
    """AI 驱动的行程生成服务"""

    def __init__(self, ai_client: Optional[Any] = None):
        """
        初始化服务

        Args:
            ai_client: AI 客户端实例（Gemini）
        """
        self.ai_client = ai_client

    async def generate_itinerary(
        self,
        destination: str,
        days: int,
        guides: List[PostDetail],
        preferences: Optional[Dict[str, Any]] = None
    ) -> Itinerary:
        """
        基于攻略生成行程

        Args:
            destination: 目的地
            days: 天数
            guides: 参考攻略列表
            preferences: 用户偏好（预算、兴趣等）

        Returns:
            生成的行程
        """
        logger.info(f"开始生成 {destination} {days} 天行程")

        # 提取景点和餐厅信息
        attractions = await self._extract_attractions(guides)
        restaurants = await self._extract_restaurants(guides)

        # 生成每日计划
        day_plans = []
        start_date = datetime.now()

        for day_num in range(1, days + 1):
            current_date = start_date + timedelta(days=day_num - 1)

            # 为每一天安排活动
            activities = await self._plan_daily_activities(
                day_num=day_num,
                attractions=attractions,
                restaurants=restaurants,
                preferences=preferences
            )

            day_plan = DayPlan(
                day=day_num,
                date=current_date.strftime("%Y-%m-%d"),
                activities=activities
            )
            day_plans.append(day_plan)

        # 创建行程对象
        itinerary = Itinerary(
            destination=destination,
            days=days,
            day_plans=day_plans
        )

        logger.info(f"行程生成完成，共 {len(day_plans)} 天")
        return itinerary

    async def _extract_attractions(
        self,
        guides: List[PostDetail]
    ) -> List[str]:
        """从攻略中提取景点信息"""
        attractions = set()

        for guide in guides:
            # 使用 AI 提取景点
            if self.ai_client:
                extracted = await self._ai_extract_attractions(guide.content)
                attractions.update(extracted)
            else:
                # 简单的关键词提取
                if '景点' in guide.content or '必去' in guide.content:
                    attractions.add(guide.title)

        logger.info(f"提取到 {len(attractions)} 个景点")
        return list(attractions)

    async def _extract_restaurants(
        self,
        guides: List[PostDetail]
    ) -> List[str]:
        """从攻略中提取餐厅信息"""
        restaurants = set()

        for guide in guides:
            # 使用 AI 提取餐厅
            if self.ai_client:
                extracted = await self._ai_extract_restaurants(guide.content)
                restaurants.update(extracted)
            else:
                # 简单的关键词提取
                if '美食' in guide.content or '餐厅' in guide.content:
                    restaurants.add(guide.title)

        logger.info(f"提取到 {len(restaurants)} 个餐厅")
        return list(restaurants)

    async def _plan_daily_activities(
        self,
        day_num: int,
        attractions: List[str],
        restaurants: List[str],
        preferences: Optional[Dict[str, Any]] = None
    ) -> List[Activity]:
        """规划每日活动"""
        activities = []

        # 简单的规划逻辑：上午景点 + 午餐 + 下午景点 + 晚餐
        if len(attractions) >= (day_num * 2 - 1):
            # 上午景点
            morning_attraction = attractions[day_num * 2 - 2]
            activities.append(Activity(
                time="09:00",
                type="景点",
                name=morning_attraction,
                duration=120,  # 2小时
                description=f"游览{morning_attraction}"
            ))

        # 午餐
        if restaurants:
            lunch_restaurant = restaurants[(day_num - 1) % len(restaurants)]
            activities.append(Activity(
                time="12:00",
                type="餐饮",
                name=lunch_restaurant,
                duration=60,
                description="午餐"
            ))

        # 下午景点
        if len(attractions) >= day_num * 2:
            afternoon_attraction = attractions[day_num * 2 - 1]
            activities.append(Activity(
                time="14:00",
                type="景点",
                name=afternoon_attraction,
                duration=180,  # 3小时
                description=f"游览{afternoon_attraction}"
            ))

        # 晚餐
        if restaurants:
            dinner_restaurant = restaurants[day_num % len(restaurants)]
            activities.append(Activity(
                time="18:00",
                type="餐饮",
                name=dinner_restaurant,
                duration=90,
                description="晚餐"
            ))

        return activities

    async def _ai_extract_attractions(self, content: str) -> List[str]:
        """使用 AI 提取景点（占位实现）"""
        # TODO: 实现 AI 提取逻辑
        return []

    async def _ai_extract_restaurants(self, content: str) -> List[str]:
        """使用 AI 提取餐厅（占位实现）"""
        # TODO: 实现 AI 提取逻辑
        return []

    def calculate_total_cost(self, itinerary: Itinerary) -> float:
        """计算行程总成本"""
        # 简单的成本估算
        # TODO: 集成实时价格查询
        base_cost_per_day = 500.0  # 每天基础消费
        total = base_cost_per_day * itinerary.days

        logger.info(f"预估总成本: ¥{total}")
        return total

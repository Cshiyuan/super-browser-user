"""
旅游相关数据模型

本模块定义旅行计划相关的所有领域模型：
- Activity: 单个活动
- DayPlan: 单日行程计划
- Itinerary: 完整行程
- Attraction/Restaurant: 景点和餐厅信息
- Budget: 预算明细
- TravelPlan: 完整旅行计划
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Activity:
    """
    单个活动

    代表行程中的一个具体活动，可以是景点游览、用餐、交通等。

    Attributes:
        time: 开始时间（HH:MM 格式）
        type: 活动类型（景点/餐饮/交通/住宿/其他）
        name: 活动名称
        duration: 持续时间（分钟）
        description: 活动描述
        cost: 活动费用（可选）
    """

    time: str
    type: str
    name: str
    duration: int
    description: str
    cost: Optional[float] = None


@dataclass
class DayPlan:
    """
    单日行程计划

    包含一天内的所有活动安排。

    Attributes:
        day: 第几天（1, 2, 3...）
        date: 日期（YYYY-MM-DD 格式）
        activities: 活动列表

    Example:
        >>> day1 = DayPlan(
        ...     day=1,
        ...     date="2025-01-20",
        ...     activities=[
        ...         Activity(time="09:00", type="景点", ...)
        ...     ]
        ... )
    """

    day: int
    date: str
    activities: List[Activity] = field(default_factory=list)

    @property
    def total_duration(self) -> int:
        """返回当天活动总时长（分钟）"""
        return sum(activity.duration for activity in self.activities)


@dataclass
class Itinerary:
    """
    完整行程

    包含整个旅行的每日计划。

    Attributes:
        destination: 目的地
        days: 总天数
        day_plans: 每日计划列表
    """

    destination: str
    days: int
    day_plans: List[DayPlan] = field(default_factory=list)

    @property
    def total_activities(self) -> int:
        """返回行程中所有活动的总数"""
        return sum(len(day.activities) for day in self.day_plans)


@dataclass
class Attraction:
    """
    景点信息

    Attributes:
        name: 景点名称
        location: 位置
        ticket_price: 门票价格
        visit_duration: 建议游览时长
        highlights: 亮点列表
        tips: 游览建议
        rating: 评分（0-5）
        mention_count: 提及次数（在攻略中）
    """

    name: str
    location: str
    ticket_price: float
    visit_duration: str
    highlights: List[str] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)
    rating: float = 0.0
    mention_count: int = 0

    @property
    def popularity_score(self) -> float:
        """
        热度分数

        基于提及次数和评分的综合热度指标。
        公式：提及次数 × 评分
        """
        return self.mention_count * self.rating


@dataclass
class Restaurant:
    """
    餐厅信息

    Attributes:
        name: 餐厅名称
        cuisine: 菜系类型
        average_cost: 人均消费
        recommended_dishes: 推荐菜品
        location: 位置
        rating: 评分（0-5）
        mention_count: 提及次数
    """

    name: str
    cuisine: str
    average_cost: float
    recommended_dishes: List[str] = field(default_factory=list)
    location: str = ""
    rating: float = 0.0
    mention_count: int = 0


@dataclass
class Budget:
    """
    预算明细

    详细记录旅行各项开支预算。

    Attributes:
        transportation: 交通费用
        accommodation: 住宿费用
        food: 餐饮费用
        tickets: 门票费用
        shopping: 购物费用
        other: 其他费用
    """

    transportation: float = 0.0
    accommodation: float = 0.0
    food: float = 0.0
    tickets: float = 0.0
    shopping: float = 0.0
    other: float = 0.0

    @property
    def total(self) -> float:
        """
        总预算

        Returns:
            float: 所有类别费用之和
        """
        return (
            self.transportation +
            self.accommodation +
            self.food +
            self.tickets +
            self.shopping +
            self.other
        )


@dataclass
class TravelPlan:
    """
    旅行计划

    整合所有旅行信息的完整计划对象。

    Attributes:
        plan_id: 计划唯一标识
        user_id: 创建用户 ID
        destination: 目的地
        days: 天数
        itinerary: 行程安排
        budget: 预算明细
        status: 计划状态（draft/confirmed/completed）
        created_at: 创建时间
        updated_at: 更新时间
    """

    plan_id: str
    user_id: str
    destination: str
    days: int
    itinerary: Itinerary
    budget: Budget
    status: str = "draft"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def is_draft(self) -> bool:
        """是否为草稿状态"""
        return self.status == "draft"

    @property
    def is_confirmed(self) -> bool:
        """是否已确认"""
        return self.status == "confirmed"

    @property
    def total_cost(self) -> float:
        """总费用（预算总额）"""
        return self.budget.total

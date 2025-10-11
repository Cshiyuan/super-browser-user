"""
旅行计划仓储接口和实现
"""

from typing import List, Optional, Protocol, Dict
from datetime import datetime

from ..domain.models.travel import TravelPlan, Itinerary


class TravelPlanRepository(Protocol):
    """旅行计划仓储接口"""

    async def save(self, plan: TravelPlan) -> TravelPlan:
        """保存旅行计划"""
        ...

    async def find_by_id(self, plan_id: str) -> Optional[TravelPlan]:
        """根据 ID 查找计划"""
        ...

    async def find_by_user(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[TravelPlan]:
        """根据用户查找计划"""
        ...

    async def find_by_destination(
        self,
        destination: str,
        limit: int = 10
    ) -> List[TravelPlan]:
        """根据目的地查找计划"""
        ...

    async def delete(self, plan_id: str) -> bool:
        """删除计划"""
        ...


class InMemoryTravelPlanRepository:
    """内存版旅行计划仓储（用于开发测试）"""

    def __init__(self):
        self._plans: Dict[str, TravelPlan] = {}

    async def save(self, plan: TravelPlan) -> TravelPlan:
        """保存旅行计划"""
        self._plans[plan.plan_id] = plan
        return plan

    async def find_by_id(self, plan_id: str) -> Optional[TravelPlan]:
        """根据 ID 查找计划"""
        return self._plans.get(plan_id)

    async def find_by_user(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[TravelPlan]:
        """根据用户查找计划"""
        results = [
            plan for plan in self._plans.values()
            if plan.user_id == user_id
        ]
        # 按创建时间倒序
        results.sort(
            key=lambda p: datetime.fromisoformat(p.created_at),
            reverse=True
        )
        return results[:limit]

    async def find_by_destination(
        self,
        destination: str,
        limit: int = 10
    ) -> List[TravelPlan]:
        """根据目的地查找计划"""
        results = [
            plan for plan in self._plans.values()
            if plan.destination == destination
        ]
        results.sort(
            key=lambda p: datetime.fromisoformat(p.created_at),
            reverse=True
        )
        return results[:limit]

    async def delete(self, plan_id: str) -> bool:
        """删除计划"""
        if plan_id in self._plans:
            del self._plans[plan_id]
            return True
        return False

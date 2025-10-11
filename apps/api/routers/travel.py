"""
旅行计划路由
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.core.services.guide_collector import GuideCollectorService
from src.core.services.itinerary_generator import ItineraryGeneratorService
from src.core.domain.models.travel import Itinerary, DayPlan, Activity
from src.infrastructure.external.ai.gemini_client import GeminiClient
from src.infrastructure.utils.logger import setup_logger


logger = setup_logger(__name__)
router = APIRouter()


# 请求/响应模型   ·
class CreatePlanRequest(BaseModel):
    """创建旅行计划请求"""
    destination: str
    days: int
    preferences: Optional[Dict[str, Any]] = None


class ActivityResponse(BaseModel):
    """活动响应"""
    time: str
    type: str
    name: str
    duration: int
    description: str


class DayPlanResponse(BaseModel):
    """日计划响应"""
    day: int
    date: str
    activities: List[ActivityResponse]


class ItineraryResponse(BaseModel):
    """行程响应"""
    destination: str
    days: int
    day_plans: List[DayPlanResponse]
    total_cost: Optional[float] = None


@router.post("/plans", response_model=ItineraryResponse)
async def create_travel_plan(request: CreatePlanRequest):
    """
    创建旅行计划

    Args:
        request: 创建请求

    Returns:
        生成的旅行计划
    """
    try:
        logger.info(f"开始创建 {request.destination} {request.days} 天旅行计划")

        # 1. 收集旅游攻略
        guide_service = GuideCollectorService(
            use_vision=False,
            concurrent=True
        )
        guides = await guide_service.collect_guides(
            destination=request.destination,
            max_posts=10
        )

        logger.info(f"收集到 {len(guides)} 篇攻略")

        # 2. 生成行程
        ai_client = GeminiClient()
        itinerary_service = ItineraryGeneratorService(ai_client=ai_client)

        itinerary = await itinerary_service.generate_itinerary(
            destination=request.destination,
            days=request.days,
            guides=guides,
            preferences=request.preferences
        )

        # 3. 计算成本
        total_cost = itinerary_service.calculate_total_cost(itinerary)

        # 4. 转换为响应格式
        return ItineraryResponse(
            destination=itinerary.destination,
            days=itinerary.days,
            day_plans=[
                DayPlanResponse(
                    day=day_plan.day,
                    date=day_plan.date,
                    activities=[
                        ActivityResponse(
                            time=activity.time,
                            type=activity.type,
                            name=activity.name,
                            duration=activity.duration,
                            description=activity.description
                        )
                        for activity in day_plan.activities
                    ]
                )
                for day_plan in itinerary.day_plans
            ],
            total_cost=total_cost
        )

    except Exception as e:
        logger.error(f"创建旅行计划失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/destinations/{destination}/summary")
async def get_destination_summary(destination: str):
    """
    获取目的地攻略摘要

    Args:
        destination: 目的地名称

    Returns:
        攻略摘要
    """
    try:
        # 收集攻略
        guide_service = GuideCollectorService()
        guides = await guide_service.collect_guides(
            destination=destination,
            max_posts=5
        )

        # 使用 AI 生成摘要
        ai_client = GeminiClient()
        guide_texts = [g.content for g in guides]
        summary = await ai_client.summarize_guides(
            guides=guide_texts,
            destination=destination
        )

        return {
            "destination": destination,
            "guide_count": len(guides),
            "summary": summary
        }

    except Exception as e:
        logger.error(f"获取目的地摘要失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

"""
数据仓储模块
"""

from .post_repository import PostRepository, InMemoryPostRepository
from .travel_repository import TravelPlanRepository, InMemoryTravelPlanRepository

__all__ = [
    "PostRepository",
    "InMemoryPostRepository",
    "TravelPlanRepository",
    "InMemoryTravelPlanRepository",
]

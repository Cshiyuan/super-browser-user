"""
数据模型
========

核心业务数据模型
"""

from .post import Post, PostDetail
from .user import UserProfile
from .travel import TravelPlan, Attraction, Restaurant, Itinerary

__all__ = [
    'Post',
    'PostDetail',
    'UserProfile',
    'TravelPlan',
    'Attraction',
    'Restaurant',
    'Itinerary',
]

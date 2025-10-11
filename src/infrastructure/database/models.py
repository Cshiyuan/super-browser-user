"""
数据库模型定义
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, JSON, Text, Boolean
)
from sqlalchemy.dialects.postgresql import ARRAY

from .connection import Base


class PostModel(Base):
    """帖子数据库模型"""

    __tablename__ = "posts"

    post_id = Column(String(100), primary_key=True)
    url = Column(String(500), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(200))
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    collects = Column(Integer, default=0)
    images = Column(JSON)  # List[str]
    tags = Column(JSON)  # List[str]
    publish_time = Column(String(100))
    location = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserProfileModel(Base):
    """用户资料数据库模型"""

    __tablename__ = "user_profiles"

    user_id = Column(String(100), primary_key=True)
    username = Column(String(200), nullable=False)
    bio = Column(Text)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    avatar_url = Column(String(500))
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TravelPlanModel(Base):
    """旅行计划数据库模型"""

    __tablename__ = "travel_plans"

    plan_id = Column(String(100), primary_key=True)
    user_id = Column(String(100), nullable=False)
    destination = Column(String(200), nullable=False)
    days = Column(Integer, nullable=False)
    itinerary = Column(JSON)  # Itinerary 对象的 JSON 表示
    budget = Column(JSON)  # Budget 对象的 JSON 表示
    status = Column(String(50), default="draft")  # draft, confirmed, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CollectionTaskModel(Base):
    """收集任务数据库模型"""

    __tablename__ = "collection_tasks"

    task_id = Column(String(100), primary_key=True)
    task_type = Column(String(50), nullable=False)  # guide, profile, etc.
    parameters = Column(JSON)  # 任务参数
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    result = Column(JSON)  # 任务结果
    error = Column(Text)  # 错误信息
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

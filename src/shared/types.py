"""
共享类型定义
"""

from typing import TypeVar, Generic, List, Optional
from enum import Enum


# 泛型类型
T = TypeVar('T')


class PaginatedResponse(Generic[T]):
    """分页响应"""

    def __init__(
        self,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size

    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ContentType(str, Enum):
    """内容类型"""
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"
    MIXED = "mixed"

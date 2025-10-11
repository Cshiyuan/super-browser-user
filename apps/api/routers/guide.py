"""
旅游攻略路由
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.core.services.guide_collector import GuideCollectorService
from src.core.domain.models.post import PostDetail
from src.infrastructure.utils.logger import setup_logger


logger = setup_logger(__name__)
router = APIRouter()


# 请求/响应模型
class CollectGuidesRequest(BaseModel):
    """收集攻略请求"""
    destination: str
    max_posts: int = 10


class PostResponse(BaseModel):
    """帖子响应"""
    post_id: str
    url: str
    title: str
    content: str
    author: str
    likes: int
    comments: int
    collects: int
    engagement_rate: float
    images: List[str]
    tags: List[str]


@router.post("/collect", response_model=List[PostResponse])
async def collect_guides(request: CollectGuidesRequest):
    """
    收集旅游攻略

    Args:
        request: 收集请求

    Returns:
        收集到的攻略列表
    """
    try:
        # 创建服务实例
        service = GuideCollectorService(
            use_vision=False,
            concurrent=True,
            max_concurrent=2
        )

        # 执行收集
        posts = await service.collect_guides(
            destination=request.destination,
            max_posts=request.max_posts
        )

        # 转换为响应格式
        return [
            PostResponse(
                post_id=post.post_id,
                url=post.url,
                title=post.title,
                content=post.content,
                author=post.author,
                likes=post.likes,
                comments=post.comments,
                collects=post.collects,
                engagement_rate=post.engagement_rate,
                images=post.images,
                tags=post.tags
            )
            for post in posts
        ]

    except Exception as e:
        logger.error(f"收集攻略失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-quality", response_model=List[PostResponse])
async def get_high_quality_guides(
    destination: str = Query(..., description="目的地"),
    min_engagement_rate: float = Query(0.05, description="最小互动率")
):
    """
    获取高质量攻略

    Args:
        destination: 目的地
        min_engagement_rate: 最小互动率

    Returns:
        高质量攻略列表
    """
    try:
        # 先收集攻略
        service = GuideCollectorService()
        posts = await service.collect_guides(destination=destination, max_posts=20)

        # 筛选高质量
        high_quality = await service.filter_high_quality_guides(
            posts=posts,
            min_engagement_rate=min_engagement_rate
        )

        return [
            PostResponse(
                post_id=post.post_id,
                url=post.url,
                title=post.title,
                content=post.content,
                author=post.author,
                likes=post.likes,
                comments=post.comments,
                collects=post.collects,
                engagement_rate=post.engagement_rate,
                images=post.images,
                tags=post.tags
            )
            for post in high_quality
        ]

    except Exception as e:
        logger.error(f"获取高质量攻略失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

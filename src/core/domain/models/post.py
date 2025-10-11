"""
帖子数据模型

本模块定义小红书帖子相关的领域模型：
- Post: 帖子基本信息
- PostDetail: 帖子详细信息（包含作者、图片、标签等）

互动率计算公式：
engagement_rate = (likes + comments + collects) / (likes + 1)

使用 likes + 1 作为分母避免除零错误，同时使得新帖子（0赞）也有合理的初始互动率。
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Post:
    """
    帖子基本信息

    包含帖子的核心数据，用于列表展示和基础查询。

    Attributes:
        post_id: 帖子唯一标识符
        url: 帖子链接
        title: 标题
        content: 内容正文
        likes: 点赞数
        comments: 评论数
        collects: 收藏数
    """

    post_id: str
    url: str
    title: str
    content: str
    likes: int
    comments: int
    collects: int


@dataclass
class PostDetail:
    """
    帖子详细信息

    扩展帖子基本信息，包含作者、图片、标签等详细数据。
    主要用于详情页展示和深度分析。

    Attributes:
        post_id: 帖子唯一标识符
        url: 帖子链接
        title: 标题
        content: 内容正文
        author: 作者昵称
        likes: 点赞数
        comments: 评论数
        collects: 收藏数
        images: 图片 URL 列表
        tags: 标签列表
        publish_time: 发布时间（可选）
        location: 地理位置（可选）

    Properties:
        engagement_rate: 互动率（计算属性）

    Example:
        >>> post = PostDetail(
        ...     post_id="123",
        ...     url="https://...",
        ...     title="成都三日游",
        ...     content="详细攻略...",
        ...     author="旅行达人",
        ...     likes=1000,
        ...     comments=100,
        ...     collects=200,
        ...     images=["img1.jpg"],
        ...     tags=["成都", "旅游"]
        ... )
        >>> print(post.engagement_rate)  # 自动计算
    """

    post_id: str
    url: str
    title: str
    content: str
    author: str
    likes: int
    comments: int
    collects: int
    images: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    publish_time: Optional[str] = None
    location: Optional[str] = None

    @property
    def engagement_rate(self) -> float:
        """
        互动率（计算属性）

        公式: (likes + comments + collects) / (likes + 1)

        为什么使用 (likes + 1) 而不是 likes？
        1. 避免除零错误：新帖子（0赞）不会导致程序崩溃
        2. 合理的初始值：0赞但有评论/收藏的帖子仍有互动率
        3. 平滑处理：避免低赞数帖子的互动率过高

        Returns:
            float: 互动率（0.0-无上限）

        Example:
            >>> post = PostDetail(..., likes=100, comments=10, collects=20, ...)
            >>> post.engagement_rate  # (100+10+20)/(100+1) = 1.287...
        """
        total_engagement = self.likes + self.comments + self.collects
        return total_engagement / (self.likes + 1)

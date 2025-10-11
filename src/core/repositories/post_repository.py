"""
帖子仓储接口和实现

本模块实现了 Repository 模式，提供帖子数据的抽象访问层。
使用 Protocol 定义接口，支持依赖注入和单元测试。

设计模式：
- Repository Pattern: 封装数据访问逻辑
- Dependency Inversion: 依赖接口而非实现
- Protocol-based Interface: Python 3.8+ 结构化类型
"""

from typing import List, Optional, Protocol, Dict
from datetime import datetime

from ..domain.models.post import Post, PostDetail


class PostRepository(Protocol):
    """
    帖子仓储接口（Protocol）

    定义了帖子数据访问的标准接口，任何实现此接口的类
    都可以作为依赖注入到服务层。

    使用 Protocol 的好处：
    1. 不需要显式继承
    2. 支持鸭子类型
    3. 更好的类型检查
    """

    async def save(self, post: PostDetail) -> PostDetail:
        """
        保存帖子

        Args:
            post: 帖子详情对象

        Returns:
            PostDetail: 保存后的帖子对象（可能包含生成的 ID）

        Raises:
            DatabaseError: 数据库操作失败
        """
        ...

    async def find_by_id(self, post_id: str) -> Optional[PostDetail]:
        """
        根据 ID 查找帖子

        Args:
            post_id: 帖子唯一标识符

        Returns:
            Optional[PostDetail]: 找到返回帖子对象，否则返回 None
        """
        ...

    async def find_by_destination(
        self,
        destination: str,
        limit: int = 10
    ) -> List[PostDetail]:
        """
        根据目的地查找帖子

        在标题或内容中搜索包含目的地关键词的帖子。

        Args:
            destination: 目的地名称（如"成都"、"北京"）
            limit: 返回结果的最大数量，默认 10

        Returns:
            List[PostDetail]: 匹配的帖子列表（按相关性排序）

        Example:
            >>> posts = await repo.find_by_destination("成都", limit=5)
            >>> print(f"找到 {len(posts)} 篇关于成都的攻略")
        """
        ...

    async def find_high_quality(
        self,
        min_engagement_rate: float = 0.05,
        limit: int = 10
    ) -> List[PostDetail]:
        """
        查找高质量帖子

        基于互动率筛选高质量内容。互动率 = (点赞 + 评论 + 收藏) / (点赞 + 1)

        Args:
            min_engagement_rate: 最小互动率阈值（0.0-1.0），默认 0.05 (5%)
            limit: 返回结果的最大数量

        Returns:
            List[PostDetail]: 高质量帖子列表（按互动率降序）

        Note:
            互动率 >= 0.08 通常被认为是高质量内容
        """
        ...

    async def delete(self, post_id: str) -> bool:
        """
        删除帖子

        Args:
            post_id: 要删除的帖子 ID

        Returns:
            bool: 删除成功返回 True，帖子不存在返回 False
        """
        ...


class InMemoryPostRepository:
    """
    内存版帖子仓储实现

    用于开发和测试环境，将数据存储在内存中。
    不依赖外部数据库，启动快速，易于测试。

    特点：
    - 无需数据库配置
    - 数据在进程重启后丢失
    - 适合单元测试和快速原型开发

    Attributes:
        _posts: 内存中的帖子存储（字典）

    Example:
        >>> repo = InMemoryPostRepository()
        >>> post = PostDetail(post_id="1", title="测试", ...)
        >>> await repo.save(post)
        >>> found = await repo.find_by_id("1")
        >>> assert found.title == "测试"
    """

    def __init__(self):
        """初始化内存存储"""
        self._posts: Dict[str, PostDetail] = {}

    async def save(self, post: PostDetail) -> PostDetail:
        """
        保存帖子到内存

        Args:
            post: 帖子详情对象

        Returns:
            PostDetail: 保存的帖子对象
        """
        self._posts[post.post_id] = post
        return post

    async def find_by_id(self, post_id: str) -> Optional[PostDetail]:
        """
        根据 ID 查找帖子

        时间复杂度: O(1)

        Args:
            post_id: 帖子 ID

        Returns:
            Optional[PostDetail]: 帖子对象或 None
        """
        return self._posts.get(post_id)

    async def find_by_destination(
        self,
        destination: str,
        limit: int = 10
    ) -> List[PostDetail]:
        """
        根据目的地查找帖子

        实现简单的关键词匹配（不区分大小写）。
        生产环境建议使用全文搜索引擎（如 Elasticsearch）。

        时间复杂度: O(n)，n 为帖子总数

        Args:
            destination: 目的地名称
            limit: 最大返回数量

        Returns:
            List[PostDetail]: 匹配的帖子列表
        """
        results = [
            post for post in self._posts.values()
            if destination in post.title or destination in post.content
        ]
        return results[:limit]

    async def find_high_quality(
        self,
        min_engagement_rate: float = 0.05,
        limit: int = 10
    ) -> List[PostDetail]:
        """
        查找高质量帖子

        筛选互动率高于阈值的帖子，并按互动率降序排序。

        时间复杂度: O(n log n)，n 为帖子总数（排序开销）

        Args:
            min_engagement_rate: 最小互动率
            limit: 最大返回数量

        Returns:
            List[PostDetail]: 高质量帖子列表（按互动率降序）
        """
        # 筛选符合条件的帖子
        results = [
            post for post in self._posts.values()
            if post.engagement_rate >= min_engagement_rate
        ]

        # 按互动率降序排序
        results.sort(key=lambda p: p.engagement_rate, reverse=True)

        return results[:limit]

    async def delete(self, post_id: str) -> bool:
        """
        删除帖子

        时间复杂度: O(1)

        Args:
            post_id: 帖子 ID

        Returns:
            bool: 删除成功返回 True，不存在返回 False
        """
        if post_id in self._posts:
            del self._posts[post_id]
            return True
        return False

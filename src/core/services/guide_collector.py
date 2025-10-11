"""
旅游攻略收集服务
"""

from typing import List, Optional
from datetime import datetime
from pathlib import Path
import json
import asyncio

from ...core.domain.models.post import Post, PostDetail
from ...infrastructure.external.xiaohongshu.collector import XiaohongshuCollector
from ...infrastructure.utils.logger import setup_logger


logger = setup_logger(__name__)


class GuideCollectorService:
    """旅游攻略收集服务"""

    def __init__(
        self,
        output_dir: str = "./collected_posts",
        use_vision: bool = False,
        concurrent: bool = False,
        max_concurrent: int = 2
    ):
        """
        初始化服务

        Args:
            output_dir: 输出目录
            use_vision: 是否启用视觉模式
            concurrent: 是否并发收集
            max_concurrent: 最大并发数
        """
        self.output_dir = Path(output_dir)
        self.use_vision = use_vision
        self.concurrent = concurrent
        self.max_concurrent = max_concurrent

    async def collect_guides(
        self,
        destination: str,
        max_posts: int = 10
    ) -> List[PostDetail]:
        """
        收集指定目的地的旅游攻略

        Args:
            destination: 目的地名称
            max_posts: 收集数量

        Returns:
            帖子详情列表
        """
        logger.info(f"开始收集 {destination} 的旅游攻略，目标数量: {max_posts}")

        # 构建搜索 URL
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={destination}+旅游攻略"

        # 创建收集器实例
        collector = XiaohongshuCollector(
            xiaohongshu_url=search_url,
            max_posts=max_posts,
            use_vision=self.use_vision,
            concurrent=self.concurrent,
            max_concurrent=self.max_concurrent
        )

        # 执行收集
        try:
            await collector.collect_posts()

            # 读取收集结果
            posts = await self._load_collected_posts(collector.batch_dir)

            logger.info(f"成功收集 {len(posts)} 篇攻略")
            return posts

        except Exception as e:
            logger.error(f"收集攻略失败: {e}")
            raise

    async def _load_collected_posts(self, batch_dir: Path) -> List[PostDetail]:
        """从收集目录加载帖子数据"""
        posts = []

        # 读取 posts_list.json
        posts_list_file = batch_dir / "posts_list.json"
        if not posts_list_file.exists():
            return posts

        with open(posts_list_file, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)

        # 读取每个帖子的详细信息
        for i, post_data in enumerate(posts_data, 1):
            post_file = batch_dir / f"post_{i}.json"
            if post_file.exists():
                with open(post_file, 'r', encoding='utf-8') as f:
                    detail_data = json.load(f)

                # 转换为 PostDetail 对象
                post_detail = PostDetail(
                    post_id=str(i),  # 使用序号作为 ID
                    url=post_data.get('url', ''),
                    title=post_data.get('title', ''),
                    content=detail_data.get('content', ''),
                    author=detail_data.get('author', ''),
                    likes=detail_data.get('likes', 0),
                    comments=detail_data.get('comments', 0),
                    collects=detail_data.get('collects', 0),
                    images=detail_data.get('images', []),
                    tags=detail_data.get('tags', []),
                    publish_time=detail_data.get('publish_time'),
                    location=detail_data.get('location')
                )
                posts.append(post_detail)

        return posts

    async def filter_high_quality_guides(
        self,
        posts: List[PostDetail],
        min_engagement_rate: float = 0.05
    ) -> List[PostDetail]:
        """
        筛选高质量攻略

        Args:
            posts: 帖子列表
            min_engagement_rate: 最小互动率阈值

        Returns:
            高质量帖子列表
        """
        high_quality = [
            post for post in posts
            if post.engagement_rate >= min_engagement_rate
        ]

        # 按互动率排序
        high_quality.sort(key=lambda p: p.engagement_rate, reverse=True)

        logger.info(
            f"筛选出 {len(high_quality)} 篇高质量攻略 "
            f"(互动率 >= {min_engagement_rate})"
        )

        return high_quality

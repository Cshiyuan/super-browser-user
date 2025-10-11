"""
用户数据模型

本模块定义小红书用户相关的领域模型。

影响力评分算法：
- 基础评分 = (粉丝数 × 0.4) + (点赞数 / 100 × 0.3) + (发帖数 × 2 × 0.3)
- 认证加成 = 基础评分 × 1.5
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UserProfile:
    """
    用户资料

    包含用户的基本信息和社交数据，用于评估用户影响力。

    Attributes:
        user_id: 用户唯一标识符
        username: 用户名（昵称）
        bio: 个人简介
        followers: 粉丝数
        following: 关注数
        posts_count: 发帖数
        likes_count: 获赞总数
        avatar_url: 头像 URL（可选）
        verified: 是否为认证用户

    Properties:
        influence_score: 影响力评分（计算属性）

    Example:
        >>> user = UserProfile(
        ...     user_id="user123",
        ...     username="旅行达人",
        ...     bio="专注旅游攻略",
        ...     followers=10000,
        ...     following=500,
        ...     posts_count=200,
        ...     likes_count=50000,
        ...     verified=True
        ... )
        >>> print(user.influence_score)
    """

    user_id: str
    username: str
    bio: Optional[str] = None
    followers: int = 0
    following: int = 0
    posts_count: int = 0
    likes_count: int = 0
    avatar_url: Optional[str] = None
    verified: bool = False

    @property
    def influence_score(self) -> float:
        """
        影响力评分（计算属性）

        综合考虑粉丝数、点赞数、发帖数来评估用户影响力。
        认证用户获得 1.5 倍加成。

        算法：
        1. 基础评分 = (粉丝数 × 0.4) + (点赞数/100 × 0.3) + (发帖数×2 × 0.3)
        2. 如果认证：最终评分 = 基础评分 × 1.5

        权重说明：
        - 粉丝数（40%）：最重要指标，反映用户受欢迎程度
        - 点赞数（30%）：内容质量指标，除以100归一化
        - 发帖数（30%）：活跃度指标，乘以2增加权重

        Returns:
            float: 影响力评分（0-无上限）

        Example:
            >>> user = UserProfile(
            ...     user_id="1",
            ...     username="测试",
            ...     followers=1000,
            ...     likes_count=5000,
            ...     posts_count=50,
            ...     verified=False
            ... )
            >>> # 基础评分 = (1000*0.4) + (5000/100*0.3) + (50*2*0.3)
            >>> # = 400 + 15 + 30 = 445
            >>> assert abs(user.influence_score - 445.0) < 0.1
        """
        base_score = (
            self.followers * 0.4 +
            (self.likes_count / 100) * 0.3 +
            (self.posts_count * 2) * 0.3
        )

        # 认证用户加成
        if self.verified:
            return base_score * 1.5

        return base_score

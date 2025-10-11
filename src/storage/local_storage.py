"""
本地文件存储 - 简单的 JSON 文件存储

使用文件系统作为存储，避免数据库依赖。
"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from ..core.domain.models.post import PostDetail
from ..core.domain.models.travel import TravelPlan


class LocalStorage:
    """本地文件存储"""

    def __init__(self, data_dir: str = "./data"):
        """
        初始化本地存储

        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir)
        self.posts_dir = self.data_dir / "posts"
        self.plans_dir = self.data_dir / "plans"

        # 创建目录
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        self.plans_dir.mkdir(parents=True, exist_ok=True)

    # ==================== 攻略存储 ====================

    def save_post(self, post: PostDetail) -> None:
        """保存攻略"""
        file_path = self.posts_dir / f"{post.post_id}.json"

        # 转换为字典
        data = {
            "post_id": post.post_id,
            "url": post.url,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "likes": post.likes,
            "comments": post.comments,
            "collects": post.collects,
            "images": post.images,
            "tags": post.tags,
            "publish_time": post.publish_time,
            "location": post.location,
            "engagement_rate": post.engagement_rate,
            "saved_at": datetime.now().isoformat()
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_post(self, post_id: str) -> Optional[PostDetail]:
        """获取单个攻略"""
        file_path = self.posts_dir / f"{post_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return PostDetail(
            post_id=data["post_id"],
            url=data["url"],
            title=data["title"],
            content=data["content"],
            author=data["author"],
            likes=data["likes"],
            comments=data["comments"],
            collects=data["collects"],
            images=data.get("images", []),
            tags=data.get("tags", []),
            publish_time=data.get("publish_time"),
            location=data.get("location")
        )

    def get_all_posts(self) -> List[PostDetail]:
        """获取所有攻略"""
        posts = []
        for file_path in self.posts_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                post = PostDetail(
                    post_id=data["post_id"],
                    url=data["url"],
                    title=data["title"],
                    content=data["content"],
                    author=data["author"],
                    likes=data["likes"],
                    comments=data["comments"],
                    collects=data["collects"],
                    images=data.get("images", []),
                    tags=data.get("tags", []),
                    publish_time=data.get("publish_time"),
                    location=data.get("location")
                )
                posts.append(post)
            except Exception as e:
                print(f"读取文件失败 {file_path}: {e}")
                continue

        # 按互动率排序
        posts.sort(key=lambda p: p.engagement_rate, reverse=True)
        return posts

    def get_posts_by_destination(self, destination: str) -> List[PostDetail]:
        """按目的地获取攻略"""
        all_posts = self.get_all_posts()
        return [
            p for p in all_posts
            if destination in p.title or destination in p.content or destination in p.tags
        ]

    # ==================== 旅行计划存储 ====================

    def save_plan(self, plan: TravelPlan) -> None:
        """保存旅行计划"""
        file_path = self.plans_dir / f"{plan.plan_id}.json"

        # 转换为字典（简化版）
        data = {
            "plan_id": plan.plan_id,
            "user_id": plan.user_id,
            "destination": plan.destination,
            "days": plan.days,
            "status": plan.status,
            "created_at": plan.created_at.isoformat() if plan.created_at else None,
            "itinerary": {
                "destination": plan.itinerary.destination,
                "days": plan.itinerary.days,
                "day_plans": [
                    {
                        "day": day.day,
                        "date": day.date,
                        "activities": [
                            {
                                "time": act.time,
                                "type": act.type,
                                "name": act.name,
                                "duration": act.duration,
                                "description": act.description,
                                "cost": act.cost
                            }
                            for act in day.activities
                        ]
                    }
                    for day in plan.itinerary.day_plans
                ]
            },
            "budget": {
                "transportation": plan.budget.transportation,
                "accommodation": plan.budget.accommodation,
                "food": plan.budget.food,
                "tickets": plan.budget.tickets,
                "shopping": plan.budget.shopping,
                "other": plan.budget.other,
                "total": plan.budget.total
            }
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_plan(self, plan_id: str) -> Optional[dict]:
        """获取旅行计划（返回字典，简化）"""
        file_path = self.plans_dir / f"{plan_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_plans(self) -> List[dict]:
        """获取所有旅行计划"""
        plans = []
        for file_path in self.plans_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                plans.append(data)
            except Exception as e:
                print(f"读取文件失败 {file_path}: {e}")
                continue

        # 按创建时间排序
        plans.sort(key=lambda p: p.get("created_at", ""), reverse=True)
        return plans

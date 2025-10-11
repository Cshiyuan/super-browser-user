#!/usr/bin/env python3
"""
攻略收集脚本

使用 browser-use 收集小红书旅游攻略。
"""

import sys
import asyncio
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.core.services.guide_collector import GuideCollectorService
from src.storage.local_storage import LocalStorage


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="收集旅游攻略")
    parser.add_argument("destination", help="目的地名称，如：成都、北京")
    parser.add_argument("--max-posts", type=int, default=5, help="最大收集数量（默认 5）")
    parser.add_argument("--use-vision", action="store_true", help="启用视觉模式（显示元素标识）")
    parser.add_argument("--concurrent", action="store_true", help="启用并发收集")
    parser.add_argument("--max-concurrent", type=int, default=2, help="最大并发数（默认 2）")

    args = parser.parse_args()

    print("=" * 60)
    print(f"🔍 开始收集 {args.destination} 的旅游攻略")
    print("=" * 60)
    print(f"最大收集数量: {args.max_posts}")
    print(f"视觉模式: {'开启' if args.use_vision else '关闭'}")
    print(f"并发收集: {'开启' if args.concurrent else '关闭'}")
    if args.concurrent:
        print(f"最大并发数: {args.max_concurrent}")
    print()

    # 初始化服务
    collector = GuideCollectorService(
        use_vision=args.use_vision,
        concurrent=args.concurrent,
        max_concurrent=args.max_concurrent
    )

    storage = LocalStorage()

    try:
        # 收集攻略
        print("🌐 正在收集攻略...")
        posts = await collector.collect_guides(
            destination=args.destination,
            max_posts=args.max_posts
        )

        if not posts:
            print("❌ 未收集到任何攻略")
            return

        print(f"✅ 成功收集 {len(posts)} 篇攻略")
        print()

        # 保存到本地存储
        print("💾 保存攻略到本地存储...")
        for post in posts:
            storage.save_post(post)
            print(f"  ✓ {post.title}")

        print()
        print("=" * 60)
        print("✅ 完成！")
        print("=" * 60)
        print(f"收集数量: {len(posts)}")
        print(f"存储位置: ./data/posts/")
        print()
        print("下一步:")
        print("  1. 运行 'uv run python run_mvp.py' 启动 Web 应用")
        print("  2. 访问 http://localhost:8000 查看攻略")
        print()

    except Exception as e:
        print(f"❌ 收集失败: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

"""
小红书帖子收集器 - 优化版

结合了原版和 vibetest 的优点：
1. 性能优化的浏览器配置
2. Scout 机制：先探测后收集
3. 并发收集（可选）
4. 更好的资源管理
5. 更详细的错误处理
6. 始终显示浏览器窗口（不使用无头模式）
"""

from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio
import json
from datetime import datetime
import os
import re
from typing import List, Dict, Optional

load_dotenv()


class XiaohongshuCollectorOptimized:
    """
    小红书帖子收集器 - 优化版

    新功能：
    - Scout 模式：先探测页面结构
    - 性能优化的浏览器配置
    - 支持并发收集
    - 更好的错误处理和重试机制
    - 始终显示浏览器（便于观察和调试）
    """

    def __init__(
        self,
        xiaohongshu_url: str,
        max_posts: int = 5,
        use_vision: bool = False,
        concurrent: bool = False,
        max_concurrent: int = 3
    ):
        """
        初始化优化版收集器

        Args:
            xiaohongshu_url: 小红书页面 URL
            max_posts: 收集帖子数量
            use_vision: 是否启用视觉模式（显示元素标识）
            concurrent: 是否并发收集
            max_concurrent: 最大并发数
        """
        self.xiaohongshu_url = xiaohongshu_url
        self.max_posts = max_posts
        self.use_vision = use_vision
        self.concurrent = concurrent
        self.max_concurrent = max_concurrent

        # 创建 LLM
        self.llm = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash-exp',
            temperature=0.7
        )

        # 创建浏览器配置（借鉴 vibetest 的性能优化，但不使用无头模式）
        self.browser_config = BrowserConfig(
            headless=False,  # 始终显示浏览器
            highlight_elements=use_vision,
            disable_security=True,
            extra_chromium_args=[
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--no-first-run',
                '--no-default-browser-check',
            ]
        )

        self.browser = Browser(config=self.browser_config)
        self.context = None

        # 输出目录
        self.output_dir = "collected_posts_optimized"
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_json_from_text(self, text: str, is_array: bool = False) -> Optional[Dict]:
        """从文本中提取 JSON"""
        # 模式1: <result>```json ... ```</result>
        pattern = r'<result>\s*```json\s*(\[.*?\]|\{.*?\})\s*```\s*</result>' if is_array else r'<result>\s*```json\s*(\{.*?\})\s*```\s*</result>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # 模式2: ```json ... ```
        pattern = r'```json\s*(\[.*?\]|\{.*?\})\s*```' if is_array else r'```json\s*(\{.*?\})\s*```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        return None

    async def scout_posts(self) -> Dict:
        """
        Scout 模式：先探测页面上的帖子元素

        这是借鉴 vibetest 的核心优化：
        先用一个 Agent 识别所有帖子元素，再分配收集任务
        """
        print("🔍 步骤0: Scout - 探测页面结构...")

        scout_task = f"""
        访问 {self.xiaohongshu_url}

        请识别页面上的所有帖子卡片元素。
        观察并记录：
        - 总共有多少个帖子
        - 每个帖子的位置和标识
        - 帖子的排列方式

        不要点击任何内容，只需要观察和报告。
        """

        scout_agent = Agent(
            task=scout_task,
            llm=self.llm,
            browser_context=self.context,
            use_vision=self.use_vision
        )

        scout_result = await scout_agent.run()
        scout_report = str(scout_result.final_result()) if hasattr(scout_result, 'final_result') else str(scout_result)

        print(f"✅ Scout 完成，页面结构已识别")
        print(f"📋 Scout 报告摘要: {scout_report[:200]}...\n")

        # 返回 scout 报告，供后续使用
        return {"report": scout_report, "timestamp": datetime.now().isoformat()}

    async def collect_post_list(self) -> List[Dict]:
        """收集帖子列表"""
        print("📋 步骤1: 收集帖子列表...")

        list_task = f"""
        访问 {self.xiaohongshu_url}

        使用 extract_structured_data 收集页面前 {self.max_posts} 个帖子的信息：
        - position: 序号（1, 2, 3...）
        - title: 标题
        - author: 作者
        - likes: 点赞数
        - url: 链接（如果可见）

        返回 JSON 数组格式
        """

        list_agent = Agent(
            task=list_task,
            llm=self.llm,
            browser_context=self.context,
            use_vision=self.use_vision
        )

        list_result = await list_agent.run()

        # 提取帖子列表
        posts_list = []
        for content in list_result.extracted_content():
            extracted = self.extract_json_from_text(str(content), is_array=True)
            if extracted:
                posts_list = extracted
                break

        print(f"✅ 收集到 {len(posts_list)} 个帖子\n")
        return posts_list

    async def collect_single_post(
        self,
        post_index: int,
        batch_dir: str,
        retry_count: int = 2
    ) -> Dict:
        """
        收集单个帖子详情（带重试机制）

        Args:
            post_index: 帖子序号
            batch_dir: 保存目录
            retry_count: 重试次数
        """
        for attempt in range(retry_count + 1):
            try:
                detail_task = f"""
                点击第 {post_index} 个帖子，使用 extract_structured_data 收集：

                帖子信息：
                - title: 标题
                - author: 作者
                - publish_time: 发布时间
                - likes: 点赞
                - collections: 收藏
                - comments_count: 评论数
                - content: 内容
                - tags: 标签数组

                评论信息（前10条）：
                - top_comments 数组，每条包含：
                  - nickname: 昵称
                  - content: 内容
                  - likes: 点赞
                  - time: 时间

                完成后返回列表页
                """

                detail_agent = Agent(
                    task=detail_task,
                    llm=self.llm,
                    browser_context=self.context,
                    use_vision=self.use_vision
                )

                detail_result = await detail_agent.run()

                # 提取数据
                post_data = None
                for content in detail_result.extracted_content():
                    extracted = self.extract_json_from_text(str(content))
                    if extracted:
                        post_data = extracted
                        break

                if not post_data:
                    if attempt < retry_count:
                        print(f"  ⚠️  第 {post_index} 个帖子数据提取失败，重试 {attempt + 1}/{retry_count}...")
                        await asyncio.sleep(2)
                        continue
                    else:
                        post_data = {"error": "未提取到数据", "attempts": attempt + 1}

                # 保存数据
                detail_file = f"{batch_dir}/post_{post_index}.json"
                with open(detail_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "post_index": post_index,
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data": post_data,
                        "attempts": attempt + 1
                    }, f, ensure_ascii=False, indent=2)

                return post_data

            except Exception as e:
                if attempt < retry_count:
                    print(f"  ⚠️  第 {post_index} 个帖子收集出错，重试 {attempt + 1}/{retry_count}: {str(e)}")
                    await asyncio.sleep(2)
                else:
                    print(f"  ❌ 第 {post_index} 个帖子收集失败: {str(e)}")
                    # 保存错误信息
                    detail_file = f"{batch_dir}/post_{post_index}.json"
                    with open(detail_file, 'w', encoding='utf-8') as f:
                        json.dump({
                            "post_index": post_index,
                            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "error": str(e),
                            "attempts": attempt + 1
                        }, f, ensure_ascii=False, indent=2)
                    return {"error": str(e)}

        return {"error": "未知错误"}

    async def collect_posts_sequential(self, posts_list: List[Dict], batch_dir: str):
        """顺序收集帖子详情"""
        print(f"📝 步骤2: 顺序收集帖子详情...\n")

        for i in range(1, min(self.max_posts, len(posts_list)) + 1):
            print(f"  [{i}/{self.max_posts}] 收集第 {i} 个帖子...")
            await self.collect_single_post(i, batch_dir)
            print(f"  ✅ 第 {i} 个帖子收集完成\n")
            await asyncio.sleep(1)

    async def collect_posts_concurrent(self, posts_list: List[Dict], batch_dir: str):
        """
        并发收集帖子详情
        借鉴 vibetest 的并发模式，但使用共享 context
        """
        print(f"📝 步骤2: 并发收集帖子详情（最大并发数: {self.max_concurrent}）...\n")

        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def collect_with_semaphore(post_index: int):
            async with semaphore:
                print(f"  🔄 开始收集第 {post_index} 个帖子...")
                result = await self.collect_single_post(post_index, batch_dir)
                print(f"  ✅ 第 {post_index} 个帖子收集完成")
                return result

        # 并发收集
        tasks = [
            collect_with_semaphore(i)
            for i in range(1, min(self.max_posts, len(posts_list)) + 1)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)
        print()

    async def collect_posts(self):
        """主收集流程"""
        # 创建浏览器上下文（始终可见）
        if self.context is None:
            self.context = await self.browser.new_context(
                config=BrowserContextConfig(
                    headless=False,  # 始终显示浏览器
                )
            )

        # 创建批次目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_dir = f"{self.output_dir}/batch_{timestamp}"
        os.makedirs(batch_dir, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"小红书帖子收集器 - 优化版")
        print(f"{'='*60}")
        print(f"目标页面: {self.xiaohongshu_url}")
        print(f"收集数量: {self.max_posts} 个帖子")
        print(f"保存目录: {batch_dir}")
        print(f"模式: {'并发' if self.concurrent else '顺序'}")
        print(f"视觉模式: {'开启' if self.use_vision else '关闭'}")
        print(f"浏览器: 可见窗口")
        print(f"{'='*60}\n")

        try:
            # Scout 探测
            scout_data = await self.scout_posts()

            # 保存 Scout 报告
            scout_file = f"{batch_dir}/scout_report.json"
            with open(scout_file, 'w', encoding='utf-8') as f:
                json.dump(scout_data, f, ensure_ascii=False, indent=2)

            # 收集帖子列表
            posts_list = await self.collect_post_list()

            # 保存帖子列表
            list_file = f"{batch_dir}/posts_list.json"
            with open(list_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total": len(posts_list),
                    "posts": posts_list
                }, f, ensure_ascii=False, indent=2)

            # 收集详情（顺序或并发）
            if self.concurrent:
                await self.collect_posts_concurrent(posts_list, batch_dir)
            else:
                await self.collect_posts_sequential(posts_list, batch_dir)

            # 保存汇总信息
            summary_file = f"{batch_dir}/summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "url": self.xiaohongshu_url,
                    "total_posts": self.max_posts,
                    "output_dir": batch_dir,
                    "mode": "concurrent" if self.concurrent else "sequential",
                    "use_vision": self.use_vision,
                    "headless": False
                }, f, ensure_ascii=False, indent=2)

            print(f"\n{'='*60}")
            print(f"✅ 收集完成！")
            print(f"📁 数据保存在: {batch_dir}")
            print(f"{'='*60}\n")

        except Exception as e:
            print(f"\n❌ 收集过程出错: {str(e)}")
            raise

        finally:
            # 清理资源（借鉴 vibetest 的严格资源管理）
            if self.context:
                try:
                    await self.context.close()
                except Exception:
                    pass

            try:
                await self.browser.close()
            except Exception:
                pass

            # 等待资源完全释放
            await asyncio.sleep(1)


async def main():
    """
    主函数

    新功能：
    1. Scout 模式自动探测页面
    2. 可选并发收集（提高速度）
    3. 性能优化的浏览器配置
    4. 更好的错误处理
    5. 始终显示浏览器窗口
    """

    # ============================================================
    # 配置区域
    # ============================================================

    xiaohongshu_url = "https://www.xiaohongshu.com/explore"
    max_posts = 3

    # 配置选项
    use_vision = False        # 是否启用视觉模式（显示元素标识）
    concurrent = False        # 是否并发收集（True = 更快但占用更多资源）
    max_concurrent = 2        # 最大并发数（仅在 concurrent=True 时有效）

    # ============================================================
    # 创建并运行收集器
    # ============================================================

    collector = XiaohongshuCollectorOptimized(
        xiaohongshu_url=xiaohongshu_url,
        max_posts=max_posts,
        use_vision=use_vision,
        concurrent=concurrent,
        max_concurrent=max_concurrent
    )

    await collector.collect_posts()


if __name__ == "__main__":
    asyncio.run(main())

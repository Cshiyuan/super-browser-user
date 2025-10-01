"""
测试脚本 - 根据官方 Quickstart 文档

这是一个简单的测试，用于验证 browser-use 安装是否正确
"""

from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio

# 加载环境变量
load_dotenv()

async def main():
    """
    官方示例：查找 Show HN 排名第一的帖子

    这个任务会：
    1. 打开浏览器
    2. 访问 Hacker News
    3. 找到 Show HN 分类
    4. 返回排名第一的帖子
    """
    print("🚀 开始测试 browser-use...")
    print("📋 任务：Find the number 1 post on Show HN")
    print("-" * 60)

    # 创建 LLM（使用 Google Gemini Flash）
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

    # 定义任务
    task = "Find the number 1 post on Show HN"

    # 创建 Agent
    agent = Agent(task=task, llm=llm)

    # 运行 Agent
    result = await agent.run()

    print("-" * 60)
    print("✅ 测试完成！")
    print(f"📊 结果: {result}")

if __name__ == "__main__":
    asyncio.run(main())

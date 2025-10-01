# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个使用 `browser-use` 库和 Google Gemini 模型的小红书帖子收集器，可以定期访问指定页面并自动收集帖子信息。

## 重要提示：API 参考文档

⚠️ **当需要使用或查询 browser-use API 时**，必须先读取 `llms-full.txt` 文件作为上下文补充。

该文件包含：
- browser-use API 的完整参考文档（4445 行）
- 所有可用的 API 端点和参数说明
- 账户管理、任务执行、浏览器配置等功能的详细说明

使用场景：
- 需要调用 browser-use API 时
- 需要了解 API 参数和返回值时
- 需要查询特定功能的实现方式时

文件位置：`./llms-full.txt`

## 核心架构

- **主程序**: `xiaohongshu_collector.py` - 小红书帖子收集器
- **AI 模型**: 通过 `langchain_google_genai` 的 `ChatGoogleGenerativeAI` 类调用 Google Gemini Flash
- **浏览器自动化**: 使用 `browser-use` 库的 Agent 架构
- **运行环境**: Python 虚拟环境 (`.venv/`)
- **包管理**: 使用 `uv` 进行依赖管理和沙箱环境隔离

## 开发命令

### 环境配置

项目使用 `uv` 进行 Python 依赖管理和沙箱环境隔离。

**系统要求**：Python >= 3.11

```bash
# 1. 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建虚拟环境（如果不存在）
uv venv

# 3. 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# 4. 安装 browser-use（我们每天都在更新，请使用最新版本！）
uv pip install browser-use

# 5. 安装 langchain-google-genai（用于 Gemini）
uv pip install langchain-google-genai python-dotenv

# 6. 下载 Chromium 浏览器（使用 Playwright）
uvx playwright install chromium --with-deps --no-shell
```

### 运行脚本

使用 `uv run` 可以自动在沙箱环境中运行脚本（推荐）：

```bash
# 运行收集器
uv run python xiaohongshu_collector.py

# 或者先激活虚拟环境后直接运行
source .venv/bin/activate
python xiaohongshu_collector.py
```

### 环境变量

创建 `.env` 文件并配置 API 密钥：

```bash
# Google Gemini API 密钥（推荐 - 免费）
# 获取地址: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# 或者使用 Google API Key（兼容）
GOOGLE_API_KEY=your_google_api_key_here

# 可选：Browser Use Cloud API 密钥（用于云浏览器服务）
# 获取地址: https://cloud.browser-use.com
BROWSER_USE_API_KEY=your_browser_use_api_key_here
```

**推荐**：使用免费的 [Gemini API 密钥](https://aistudio.google.com/app/apikey) 开始

## Agent 实现模式

### 方式 1：快速开始（推荐）

使用 browser-use 推荐的简化方式：

```python
from browser_use import Agent, ChatGoogle
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    task="Find the number of stars of the browser-use repo",
    llm=ChatGoogle(model="gemini-flash-latest"),
)
agent.run_sync()  # 同步运行
```

### 方式 2：异步模式（更灵活）

适用于需要更多控制的场景：

```python
from browser_use import Agent, Browser, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')
    browser = Browser()
    context = await browser.new_context(
        config=BrowserContextConfig(headless=False)
    )

    agent = Agent(
        task="你的任务描述",
        llm=llm,
        browser_context=context
    )
    await agent.run()

    await context.close()
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 方式 3：使用云浏览器（绕过反爬虫）

适用于需要绕过 Cloudflare 等反爬虫保护：

```python
from browser_use import Agent, Browser, ChatGoogle

# 使用 Browser Use Cloud 云浏览器服务
browser = Browser(
    use_cloud=True,  # 自动使用云浏览器
)

agent = Agent(
    task="你的任务描述",
    llm=ChatGoogle(model='gemini-flash-latest'),
    browser=browser,
)
agent.run_sync()
```

**注意**：使用云浏览器需要在 `.env` 中配置 `BROWSER_USE_API_KEY`

## 重要文件

**代码文件**：
- `xiaohongshu_collector.py` - 小红书帖子收集器

**文档文件**：
- `README.md` - 收集器详细说明文档
- `llms-full.txt` - **browser-use API 完整参考文档（重要）**

**配置文件**：
- `.env` - 环境变量配置文件（不在代码仓库中）

**数据目录**：
- `collected_posts/` - 数据存储目录

## 小红书收集器使用说明

### 功能特点

**核心功能**：
- ✅ **Scout 探测模式**：先识别页面结构，再执行收集
- ✅ **性能优化**：浏览器启动参数优化，减少资源占用
- ✅ **并发收集**：可选的并发模式，大幅提升收集速度
- ✅ **重试机制**：失败自动重试，提高成功率
- ✅ **灵活配置**：支持无头模式、视觉模式切换
- ✅ **资源管理**：严格的资源清理，避免内存泄漏

### 配置方式

在 `xiaohongshu_collector.py` 的 `main()` 函数中修改：

```python
xiaohongshu_url = "https://www.xiaohongshu.com/explore"  # 目标页面
max_posts = 3  # 收集数量

# 高级配置
use_vision = False        # 是否启用视觉模式（显示元素标识）
concurrent = False        # 是否并发收集（True = 更快）
max_concurrent = 2        # 最大并发数（仅在 concurrent=True 时有效）
```

**配置建议**：
- **开发调试**：`use_vision=True, concurrent=False`
- **快速收集**：`use_vision=False, concurrent=True, max_concurrent=3`
- **稳定收集**：`use_vision=False, concurrent=False`

### 输出数据

输出目录：`collected_posts/batch_YYYYMMDD_HHMMSS/`

包含文件：
- `scout_report.json` - Scout 探测报告
- `posts_list.json` - 帖子列表汇总
- `post_1.json`, `post_2.json`, ... - 各个帖子的详细信息
- `summary.json` - 本次收集的汇总信息（包含模式信息）
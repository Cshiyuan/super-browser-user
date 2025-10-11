# 快速参考手册

这是一个精简的参考文档，帮助你快速查找常用信息。

---

## 🚀 快速命令

### 环境设置
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
uv venv

# 激活环境
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 安装依赖
uv pip install browser-use langchain-google-genai python-dotenv

# 下载浏览器
uvx playwright install chromium --with-deps --no-shell
```

### 运行程序
```bash
# 直接运行
uv run python xiaohongshu_collector.py

# 或先激活环境
source .venv/bin/activate
python xiaohongshu_collector.py
```

---

## ⚙️ 配置速查

### 环境变量 (.env)
```bash
# Google Gemini API 密钥（必需）
GEMINI_API_KEY=your_key_here

# Browser Use Cloud API 密钥（可选，用于云浏览器）
BROWSER_USE_API_KEY=your_key_here
```

### 主要配置参数

在 `xiaohongshu_collector.py` 的 `main()` 函数中修改：

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| `xiaohongshu_url` | str | - | 目标页面 URL |
| `max_posts` | int | 3 | 收集帖子数量 |
| `use_vision` | bool | False | 是否显示元素标识 |
| `concurrent` | bool | False | 是否并发收集 |
| `max_concurrent` | int | 2 | 最大并发数 |

### 配置模板

```python
# 开发调试模式
xiaohongshu_url = "https://www.xiaohongshu.com/explore"
max_posts = 2
use_vision = True
concurrent = False
max_concurrent = 2

# 快速收集模式
xiaohongshu_url = "https://www.xiaohongshu.com/explore"
max_posts = 10
use_vision = False
concurrent = True
max_concurrent = 3

# 稳定收集模式
xiaohongshu_url = "https://www.xiaohongshu.com/explore"
max_posts = 5
use_vision = False
concurrent = False
max_concurrent = 2
```

---

## 📂 输出结构

```
collected_posts_optimized/
└── batch_YYYYMMDD_HHMMSS/
    ├── scout_report.json    # Scout 探测报告
    ├── posts_list.json      # 帖子列表汇总
    ├── post_1.json          # 第 1 个帖子详情
    ├── post_2.json          # 第 2 个帖子详情
    ├── post_N.json          # 第 N 个帖子详情
    └── summary.json         # 本次收集汇总
```

---

## 🔑 核心代码片段

### 创建 Agent
```python
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')

agent = Agent(
    task="你的任务描述",
    llm=llm,
    browser_context=context,
    use_vision=False
)

result = await agent.run()
```

### 提取结构化数据
```python
task = """
使用 extract_structured_data 收集：
- field1: 描述
- field2: 描述
返回 JSON 格式
"""
```

### 并发控制
```python
import asyncio

semaphore = asyncio.Semaphore(max_concurrent)

async def task_with_limit(i):
    async with semaphore:
        await do_task(i)

tasks = [task_with_limit(i) for i in range(N)]
await asyncio.gather(*tasks)
```

### 重试机制
```python
for attempt in range(retry_count + 1):
    try:
        result = await do_task()
        break
    except Exception as e:
        if attempt < retry_count:
            await asyncio.sleep(2)
            continue
        else:
            handle_error(e)
```

---

## 🐛 常见问题

### 1. API 密钥未设置
```
错误: GEMINI_API_KEY not found
解决: 在 .env 文件中设置 GEMINI_API_KEY
```

### 2. 浏览器未安装
```
错误: Chromium not found
解决: uvx playwright install chromium --with-deps --no-shell
```

### 3. 依赖未安装
```
错误: ModuleNotFoundError: No module named 'browser_use'
解决: uv pip install browser-use langchain-google-genai python-dotenv
```

### 4. API 配额超限
```
错误: Rate limit exceeded
解决:
- 减少并发数 (max_concurrent = 1)
- 减少收集数量 (max_posts = 3)
- 等待配额恢复（Gemini 免费版：15次/分钟）
```

### 5. 元素未找到
```
错误: Element not found
解决:
- 检查任务描述是否清晰
- 启用视觉模式 (use_vision = True)
- 增加等待时间
```

### 6. JSON 解析失败
```
错误: JSONDecodeError
解决:
- 检查 AI 返回的文本格式
- 查看 extract_json_from_text 的正则模式
- 调整任务描述，明确要求 JSON 格式
```

---

## 📊 性能参考

### API 消耗估算

| 阶段 | API 调用次数 | 说明 |
|-----|-------------|------|
| Scout 探测 | 1 | 识别页面结构 |
| 收集列表 | 1 | 提取帖子列表 |
| 收集详情 | N | N = 帖子数量 |
| **总计** | **N + 2** | - |

**示例**:
- 收集 3 个帖子 = 5 次 API 调用
- 收集 10 个帖子 = 12 次 API 调用

### 时间估算

| 模式 | 单个帖子耗时 | 3个帖子总时间 | 10个帖子总时间 |
|-----|-------------|--------------|---------------|
| 顺序模式 | ~30秒 | ~90秒 | ~300秒 |
| 并发模式 (3并发) | ~30秒 | ~30秒 | ~100秒 |

### 资源占用

| 资源 | 顺序模式 | 并发模式 (3并发) |
|-----|---------|-----------------|
| 内存 | ~500MB | ~800MB |
| CPU | ~20% | ~40% |
| 网络 | 低 | 中 |

---

## 🎯 最佳实践

### DO ✅

1. **明确的任务描述**
   ```python
   task = "点击第 1 个帖子，提取标题和内容"  # 清晰具体
   ```

2. **适当的并发数**
   ```python
   max_concurrent = 2-3  # 平衡速度和稳定性
   ```

3. **资源清理**
   ```python
   try:
       await collect_posts()
   finally:
       await context.close()
       await browser.close()
   ```

4. **错误处理**
   ```python
   try:
       result = await agent.run()
   except Exception as e:
       logger.error(f"Error: {e}")
       # 保存错误信息
   ```

### DON'T ❌

1. **模糊的任务描述**
   ```python
   task = "收集数据"  # 太模糊
   ```

2. **过高的并发数**
   ```python
   max_concurrent = 10  # 会导致浏览器卡顿
   ```

3. **忘记清理资源**
   ```python
   await collect_posts()
   # ❌ 没有 close()，资源泄漏
   ```

4. **忽略错误**
   ```python
   result = await agent.run()
   # ❌ 没有 try-except
   ```

---

## 📖 文档导航

- **[README.md](./README.md)** - 项目介绍和快速开始
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - 详细架构说明
- **[CLAUDE.md](./CLAUDE.md)** - 开发配置指南
- **[QUICKREF.md](./QUICKREF.md)** - 本文档
- **[xiaohongshu_collector.py](./xiaohongshu_collector.py)** - 源码（含注释）

---

## 🔗 外部资源

- [browser-use GitHub](https://github.com/browser-use/browser-use)
- [browser-use 文档](https://docs.browser-use.com)
- [Google Gemini API](https://aistudio.google.com/app/apikey)
- [Playwright 文档](https://playwright.dev/python/)
- [LangChain 文档](https://python.langchain.com/)

---

**提示**: 这是快速参考手册，详细说明请查看 [ARCHITECTURE.md](./ARCHITECTURE.md)

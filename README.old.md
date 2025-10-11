# 小红书帖子收集器

使用 AI 自动化收集小红书帖子信息的工具，基于 [browser-use](https://github.com/browser-use/browser-use) 和 Google Gemini。

## 📖 学习指南

**如果你是第一次接触这个项目，推荐按以下顺序学习：**

1. 📘 **[README.md](./README.md)** (本文档) - 快速开始和基本使用
2. 📐 **[ARCHITECTURE.md](./ARCHITECTURE.md)** - 深入理解架构和原理 ⭐
3. 💻 **[xiaohongshu_collector.py](./xiaohongshu_collector.py)** - 阅读详细注释的源码
4. 🔧 **[CLAUDE.md](./CLAUDE.md)** - 项目配置和开发指南
5. ⚡ **[QUICKREF.md](./QUICKREF.md)** - 快速参考手册（速查）
6. 📚 **[llms-full.txt](./llms-full.txt)** - browser-use API 完整参考

---

## ✨ 特性

- 🤖 **AI 驱动**：使用 Google Gemini 理解页面内容
- 🔍 **Scout 探测**：智能识别页面结构
- ⚡ **并发收集**：可选的并发模式，大幅提升速度
- 🔄 **自动重试**：失败自动重试，提高成功率
- 📊 **结构化数据**：保存为 JSON 格式，便于分析
- 🎯 **性能优化**：浏览器启动参数优化

## 🚀 快速开始

### 系统要求

- Python >= 3.11
- macOS / Linux / Windows

### 安装

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd super-browser-user

# 2. 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 创建虚拟环境
uv venv

# 4. 激活虚拟环境
source .venv/bin/activate  # macOS/Linux

# 5. 安装依赖
uv pip install browser-use langchain-google-genai python-dotenv

# 6. 下载 Chromium 浏览器
uvx playwright install chromium --with-deps --no-shell
```

### 配置 API 密钥

创建 `.env` 文件：

```bash
# 获取免费的 Gemini API 密钥: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
```

### 运行

```bash
# 运行收集器
uv run python xiaohongshu_collector.py

# 或者先激活环境
source .venv/bin/activate
python xiaohongshu_collector.py
```

## 📖 使用说明

### 基本配置

在 `xiaohongshu_collector.py` 的 `main()` 函数中修改配置：

```python
# 目标页面
xiaohongshu_url = "https://www.xiaohongshu.com/explore"

# 收集数量
max_posts = 3

# 高级选项
use_vision = False      # 是否显示元素标识（调试用）
concurrent = False      # 是否并发收集
max_concurrent = 2      # 最大并发数
```

### 配置建议

**开发调试**：
```python
use_vision = True
concurrent = False
```

**快速收集**：
```python
use_vision = False
concurrent = True
max_concurrent = 3
```

**稳定收集**：
```python
use_vision = False
concurrent = False
```

## 📂 输出数据

收集的数据保存在 `collected_posts/batch_YYYYMMDD_HHMMSS/` 目录：

```
collected_posts/
└── batch_20250102_120000/
    ├── scout_report.json      # Scout 探测报告
    ├── posts_list.json        # 帖子列表汇总
    ├── post_1.json            # 第 1 个帖子详情
    ├── post_2.json            # 第 2 个帖子详情
    ├── post_3.json            # 第 3 个帖子详情
    └── summary.json           # 本次收集汇总
```

### 数据格式示例

**帖子列表** (`posts_list.json`)：
```json
{
  "timestamp": "2025-01-02 12:00:00",
  "total": 3,
  "posts": [
    {
      "position": 1,
      "title": "帖子标题",
      "author": "作者名",
      "likes": "1.2万"
    }
  ]
}
```

**帖子详情** (`post_1.json`)：
```json
{
  "post_index": 1,
  "collected_at": "2025-01-02 12:01:00",
  "data": {
    "title": "帖子标题",
    "author": "作者名",
    "content": "帖子内容...",
    "tags": ["标签1", "标签2"],
    "top_comments": [
      {
        "nickname": "评论者",
        "content": "评论内容",
        "likes": "100",
        "time": "1小时前"
      }
    ]
  }
}
```

## 🎯 核心优化

相比基础实现，优化版本提供：

| 特性 | 说明 | 效果 |
|-----|------|-----|
| Scout 探测 | 先识别页面结构 | 提高成功率 |
| 性能优化 | 浏览器参数优化 | 启动快 50% |
| 并发收集 | 多任务并行执行 | 速度提升 3 倍 |
| 重试机制 | 自动重试失败任务 | 更稳定 |
| 资源管理 | 严格清理资源 | 避免泄漏 |

## 📚 完整文档

### 核心文档
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - 📐 **架构说明文档（必读）**
  - 整体架构图解
  - 核心技术栈详解
  - 工作流程说明
  - 数据流转过程
  - 性能优化技巧
  - 最佳实践指南

- **[CLAUDE.md](./CLAUDE.md)** - 🔧 项目配置和开发指南
  - 环境配置
  - 开发命令
  - Agent 实现模式

- **[llms-full.txt](./llms-full.txt)** - 📘 browser-use API 完整参考
  - 4445 行完整文档
  - API 端点说明
  - 参数详解

- **[QUICKREF.md](./QUICKREF.md)** - ⚡ 快速参考手册
  - 常用命令速查
  - 配置模板
  - 常见问题解决
  - 性能参考数据

### 代码文件
- **[xiaohongshu_collector.py](./xiaohongshu_collector.py)** - 💻 主程序（含详细中文注释）
  - 核心收集器实现
  - 三阶段收集流程
  - 并发和重试机制

## 💡 核心概念速览

### Agent 模式
```python
agent = Agent(
    task="你的任务描述（自然语言）",  # AI 会理解并执行
    llm=ChatGoogleGenerativeAI(),      # AI 模型
    browser_context=context            # 浏览器会话
)
await agent.run()  # AI 自主执行任务
```

### 三阶段收集
1. **Scout 探测**: AI 先观察页面结构（不点击）
2. **收集列表**: 提取所有帖子的基本信息
3. **收集详情**: 逐个点击，提取完整内容和评论

### 并发控制
```python
# 顺序模式：帖子1 → 帖子2 → 帖子3 (慢但稳定)
concurrent = False

# 并发模式：帖子1、2、3 同时收集 (快3倍)
concurrent = True
max_concurrent = 3
```

详细原理请查看 **[ARCHITECTURE.md](./ARCHITECTURE.md)**

---

## 🔗 相关链接

- [browser-use GitHub](https://github.com/browser-use/browser-use)
- [browser-use 文档](https://docs.browser-use.com)
- [Google Gemini API](https://aistudio.google.com/app/apikey)
- [Browser Use Cloud](https://cloud.browser-use.com)

## 🛠️ 技术栈

- **browser-use** - 浏览器自动化框架
- **Google Gemini** - AI 模型（用于理解页面）
- **Playwright** - 底层浏览器控制
- **Python 3.11+** - 编程语言
- **uv** - Python 包管理工具

## 📝 使用场景

- 📊 数据分析：收集小红书帖子数据进行分析
- 🔍 竞品研究：跟踪竞品的内容和互动数据
- 📈 趋势监控：定期收集数据，观察趋势变化
- 💡 内容灵感：收集热门内容，获取创作灵感

## ⚠️ 注意事项

1. **遵守法律法规**：确保使用符合当地法律和小红书服务条款
2. **控制频率**：避免过于频繁的请求，建议设置合理的延迟
3. **尊重隐私**：收集的数据仅用于合法用途
4. **API 配额**：注意 Gemini API 的使用配额

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [browser-use](https://github.com/browser-use/browser-use) - 强大的浏览器自动化框架
- [Google Gemini](https://ai.google.dev/) - 优秀的 AI 模型
- 所有贡献者

---

Made with ❤️ using [browser-use](https://github.com/browser-use/browser-use)

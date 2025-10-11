# Super Browser User - MVP

> AI 驱动的旅游攻略收集和行程规划系统

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 特性

- 🤖 **AI 驱动**: 使用 Google Gemini 2.0 Flash 进行智能内容理解和行程规划
- 🌐 **自动化收集**: 基于 browser-use 和 Playwright 的高效数据采集
- 📊 **智能分析**: 自动识别高质量攻略，计算互动率
- 🗺️ **行程生成**: AI 自动生成个性化旅行计划
- 💾 **本地存储**: 简单的 JSON 文件存储，无需数据库
- 🌐 **Web 界面**: 友好的 Web UI，方便查看攻略和计划

## 🚀 快速开始

### 前置要求

- Python >= 3.11
- uv (Python 包管理器)

### 安装

```bash
# 1. 克隆项目
git clone <repository-url>
cd super-browser-user

# 2. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 安装依赖
uv pip install browser-use langchain-google-genai python-dotenv fastapi uvicorn jinja2

# 4. 安装 Playwright 浏览器
uvx playwright install chromium --with-deps --no-shell

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env，填写 GEMINI_API_KEY
```

**获取免费 Gemini API 密钥**: https://aistudio.google.com/app/apikey

### 使用

#### 1. 收集旅游攻略

```bash
# 收集成都的旅游攻略
uv run python collect_guides.py 成都 --max-posts 5

# 启用并发模式（更快）
uv run python collect_guides.py 成都 --max-posts 5 --concurrent

# 查看所有选项
uv run python collect_guides.py --help
```

#### 2. 启动 Web 应用

```bash
# 启动 Web 服务
uv run python run_mvp.py
```

然后访问：
- 🌐 主页: http://localhost:8000
- 📖 API 文档: http://localhost:8000/docs

#### 3. 使用 API 生成旅行计划

```bash
# 生成成都 3 天旅行计划
curl -X POST "http://localhost:8000/api/generate-plan?destination=成都&days=3"
```

## 项目结构

```
super-browser-user/
├── src/                          # 源代码
│   ├── core/                     # 核心业务逻辑
│   │   ├── domain/models/        # 领域模型
│   │   ├── services/             # 业务服务
│   │   └── repositories/         # 数据仓储接口
│   ├── infrastructure/           # 基础设施
│   │   ├── external/             # 外部服务集成
│   │   │   ├── xiaohongshu/      # 小红书收集器
│   │   │   └── ai/               # Gemini AI 客户端
│   │   └── utils/                # 工具类
│   └── storage/                  # 本地存储
├── templates/                    # HTML 模板
├── data/                         # 数据目录 (自动创建)
│   ├── posts/                    # 攻略数据
│   └── plans/                    # 旅行计划
├── tests/                        # 测试
├── examples/                     # 示例代码
├── collect_guides.py             # 攻略收集脚本
├── run_mvp.py                    # MVP 启动脚本
└── web_app.py                    # Web 应用
```

## 核心功能

### 1. 旅游攻略收集

从小红书自动收集旅游攻略：

- 🎯 Scout 探测模式：智能识别页面结构
- ⚡ 并发收集：2-3x 速度提升
- 📊 质量评估：自动计算互动率
- 💾 本地存储：保存为 JSON 文件

### 2. 智能行程生成

基于收集的攻略生成旅行计划：

- 🧠 AI 理解：提取景点、美食、注意事项
- 📅 日程规划：自动安排每日行程
- 💰 预算估算：提供成本参考

### 3. Web 界面

友好的 Web UI：

- 📋 攻略列表：查看所有收集的攻略
- 📖 攻略详情：查看完整内容和图片
- 🗺️ 旅行计划：查看生成的行程
- 📊 统计信息：互动率、热门标签等

## API 端点

### 页面

- `GET /` - 首页
- `GET /posts` - 攻略列表
- `GET /post/{post_id}` - 攻略详情
- `GET /plans` - 旅行计划列表
- `GET /plan/{plan_id}` - 旅行计划详情

### API

- `GET /api/posts` - 获取攻略列表
- `GET /api/plans` - 获取旅行计划列表
- `POST /api/generate-plan` - 生成旅行计划

## 技术栈

- **AI 模型**: Google Gemini 2.0 Flash (免费)
- **浏览器自动化**: browser-use + Playwright
- **Web 框架**: FastAPI
- **模板引擎**: Jinja2
- **存储**: 本地 JSON 文件
- **包管理**: uv

## 配置说明

主要配置项 (`.env`):

```env
# AI 配置 (必需)
GEMINI_API_KEY=your_key_here

# 可选配置
GEMINI_MODEL=gemini-2.0-flash-exp
DEBUG=true
```

## 开发指南

### 运行测试

```bash
# 运行所有单元测试
uv run pytest tests/unit/ -v

# 查看覆盖率
uv run pytest tests/unit/ --cov=src --cov-report=html
```

### 架构说明

项目采用领域驱动设计 (DDD) 和分层架构：

- **Domain Layer**: 领域模型和业务规则 (`src/core/domain/`)
- **Service Layer**: 业务逻辑和服务 (`src/core/services/`)
- **Infrastructure Layer**: 外部服务集成 (`src/infrastructure/`)
- **Storage Layer**: 数据持久化 (`src/storage/`)

详细架构文档：[docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)

### 关键文件

**核心服务**:
- `src/core/services/guide_collector.py` - 攻略收集服务
- `src/core/services/itinerary_generator.py` - 行程生成服务

**外部集成**:
- `src/infrastructure/external/ai/gemini_client.py` - Gemini AI 客户端
- `src/infrastructure/external/xiaohongshu/collector.py` - 小红书收集器

**存储**:
- `src/storage/local_storage.py` - 本地文件存储

**Web 应用**:
- `web_app.py` - FastAPI 应用
- `templates/` - HTML 模板

## 常见问题

**Q: Gemini API 免费吗？**

A: 是的，Gemini Flash 提供免费额度（每分钟 15 次请求），足够个人使用。

**Q: 数据存储在哪里？**

A: 数据以 JSON 格式存储在 `./data/` 目录下。

**Q: 收集速度慢怎么办？**

A: 使用 `--concurrent` 参数启用并发模式，可提升 2-3 倍速度。

**Q: 如何添加新的数据源？**

A: 参考 `src/infrastructure/external/xiaohongshu/collector.py`，实现新的收集器。

## 文档

- [CLAUDE.md](./CLAUDE.md) - 开发指南和 browser-use API 参考
- [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) - 架构设计文档
- [docs/api/API_REFERENCE.md](docs/api/API_REFERENCE.md) - API 参考
- [TEST_REPORT.md](TEST_REPORT.md) - 测试报告

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [browser-use](https://github.com/browser-use/browser-use) - 强大的浏览器自动化框架
- [Google Gemini](https://ai.google.dev/) - 免费的多模态 AI 模型
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架

---

⭐ 如果这个项目对你有帮助，请给个 Star！

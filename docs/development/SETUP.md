# 开发环境设置指南

本文档介绍如何设置 Super Browser User 项目的开发环境。

## 系统要求

- **Python**: >= 3.11
- **操作系统**: macOS, Linux, Windows
- **工具**: uv (Python 包管理器)

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd super-browser-user
```

### 2. 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. 创建虚拟环境

```bash
uv venv
```

### 4. 激活虚拟环境

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 5. 安装依赖

```bash
# 安装所有依赖
uv pip install -e .

# 或使用 requirements.txt
uv pip install -r requirements.txt

# 安装开发依赖
uv pip install -e ".[dev]"
```

### 6. 安装 Playwright 浏览器

```bash
uvx playwright install chromium --with-deps --no-shell
```

### 7. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，至少需要配置以下必填项：

```env
# 必填：Gemini API 密钥
GEMINI_API_KEY=your_gemini_api_key_here

# 可选：数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/super_browser_user
REDIS_URL=redis://localhost:6379/0
```

**获取 API 密钥**：
- Gemini API: https://aistudio.google.com/app/apikey (免费)
- Browser Use Cloud: https://cloud.browser-use.com (可选)

### 8. 初始化数据库

```bash
# 启动 PostgreSQL (如果使用本地数据库)
brew install postgresql@15  # macOS
brew services start postgresql@15

# 创建数据库
createdb super_browser_user

# 运行迁移
alembic upgrade head
```

### 9. 启动 Redis

```bash
# macOS
brew install redis
brew services start redis

# Docker (推荐)
docker run -d -p 6379:6379 redis:latest
```

## 验证安装

### 运行测试

```bash
pytest tests/
```

### 启动 API 服务器

```bash
# 使用 uv run (推荐)
uv run uvicorn apps.api.main:app --reload

# 或直接运行
python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

访问：http://localhost:8000/docs 查看 API 文档

### 使用 CLI

```bash
# 查看帮助
uv run super-browser --help

# 收集攻略示例
uv run super-browser collect "成都" --max-posts 5

# 生成旅行计划
uv run super-browser plan "成都" --days 3 --output plan.json
```

## 开发工具配置

### VSCode 配置

创建 `.vscode/settings.json`：

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### Pre-commit Hooks (可选)

```bash
# 安装 pre-commit
uv pip install pre-commit

# 安装 git hooks
pre-commit install

# 手动运行
pre-commit run --all-files
```

## 常见问题

### Q1: Playwright 安装失败

```bash
# 手动安装 Chromium 依赖
uvx playwright install-deps chromium
```

### Q2: 数据库连接失败

检查 PostgreSQL 是否运行：

```bash
# macOS
brew services list | grep postgresql

# 查看日志
tail -f /usr/local/var/log/postgres.log
```

### Q3: Redis 连接失败

检查 Redis 是否运行：

```bash
redis-cli ping  # 应返回 PONG
```

### Q4: Gemini API 配额超限

免费版限制：
- 每分钟 15 次请求
- 每天 1500 次请求

解决方案：
- 添加重试延迟
- 升级到付费版

## 下一步

- 阅读 [API 设计文档](API_DESIGN.md)
- 查看 [数据库设计文档](DATABASE_DESIGN.md)
- 了解 [架构设计](../architecture/ARCHITECTURE.md)
- 贡献代码前请阅读 [贡献指南](../contributing/CONTRIBUTING.md)

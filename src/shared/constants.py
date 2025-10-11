"""
全局常量
"""

# API 相关
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# 分页
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# 缓存
CACHE_TTL_SHORT = 300  # 5分钟
CACHE_TTL_MEDIUM = 1800  # 30分钟
CACHE_TTL_LONG = 3600  # 1小时

# 任务
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

# 小红书
XHS_BASE_URL = "https://www.xiaohongshu.com"
XHS_SEARCH_URL = f"{XHS_BASE_URL}/search_result"

# AI 模型
GEMINI_MODEL = "gemini-2.0-flash-exp"
GEMINI_TEMPERATURE = 0.7

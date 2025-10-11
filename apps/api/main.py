"""
FastAPI 应用主入口
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.connection import init_db, close_db
from src.infrastructure.cache.redis_client import redis_client
from src.infrastructure.utils.config import settings
from src.infrastructure.utils.logger import setup_logger

from .routers import guide, travel, health


logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info(f"启动 {settings.APP_NAME} v{settings.APP_VERSION}")

    # 初始化数据库
    await init_db()

    # 初始化 Redis
    await redis_client.connect()

    yield

    # 关闭时
    await redis_client.close()
    await close_db()
    logger.info("应用已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI 驱动的浏览器自动化工具集",
    lifespan=lifespan
)


# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])
app.include_router(guide.router, prefix="/api/v1/guides", tags=["旅游攻略"])
app.include_router(travel.router, prefix="/api/v1/travel", tags=["旅行计划"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

"""
健康检查路由
"""

from fastapi import APIRouter
from datetime import datetime

from src.infrastructure.utils.config import settings


router = APIRouter()


@router.get("/health")
async def health_check():
    """
    健康检查接口

    Returns:
        应用健康状态
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/ping")
async def ping():
    """
    简单 Ping 接口

    Returns:
        Pong 响应
    """
    return {"message": "pong"}

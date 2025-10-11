"""
日志工具
"""

import logging
import sys
from typing import Optional
from .config import settings


def setup_logger(
    name: str,
    level: Optional[str] = None
) -> logging.Logger:
    """设置日志器"""

    logger = logging.getLogger(name)
    logger.setLevel(level or settings.LOG_LEVEL)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level or settings.LOG_LEVEL)

    # 格式化
    if settings.LOG_FORMAT == "json":
        # JSON 格式（生产环境）
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"name": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # 文本格式（开发环境）
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# 默认日志器
default_logger = setup_logger("app")

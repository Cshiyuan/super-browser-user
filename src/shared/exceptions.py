"""
自定义异常
"""


class AppException(Exception):
    """应用基础异常"""

    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(AppException):
    """验证错误"""

    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class NotFoundError(AppException):
    """资源未找到"""

    def __init__(self, resource: str, id: str):
        message = f"{resource} with id '{id}' not found"
        super().__init__(message, "NOT_FOUND")


class CollectionError(AppException):
    """数据采集错误"""

    def __init__(self, message: str):
        super().__init__(message, "COLLECTION_ERROR")


class AIError(AppException):
    """AI 处理错误"""

    def __init__(self, message: str):
        super().__init__(message, "AI_ERROR")


class ExternalServiceError(AppException):
    """外部服务错误"""

    def __init__(self, service: str, message: str):
        super().__init__(f"{service}: {message}", "EXTERNAL_SERVICE_ERROR")
        self.service = service

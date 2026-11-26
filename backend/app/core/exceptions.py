class AppError(Exception):
    """业务异常基类；由路由层统一转换为 HTTP 响应。"""


class NotFoundError(AppError):
    """请求的资源不存在。"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

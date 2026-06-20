"""跨平台管理员/root 权限检测包"""

from .core import (
    AdminDetector,
    UnixAdminDetector,
    WindowsAdminDetector,
)

__all__ = [
    "AdminDetector",
    "UnixAdminDetector",
    "WindowsAdminDetector",
]
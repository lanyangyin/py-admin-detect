"""跨平台管理员/root 权限检测包"""

__version__ = "1.0.0"

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
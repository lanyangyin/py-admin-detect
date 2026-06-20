#!/usr/bin/env python3
"""admin-detector 使用示例"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from admin_detector import AdminDetector, UnixAdminDetector, WindowsAdminDetector
import platform


def main():
    print("=== admin-detector 示例 ===\n")

    if AdminDetector.is_admin():
        print("✅ 当前进程拥有管理员/root 权限。")
    else:
        print("❌ 当前进程没有管理员/root 权限。")

    print("\n--- 详细信息 ---")
    info = AdminDetector.get_admin_info()
    for key, value in info.items():
        print(f"{key}: {value}")

    result = AdminDetector.check_admin_with_reason()
    print(f"\n检测原因: {result['reason']}")

    system = platform.system().lower()
    print(f"\n--- {system.capitalize()} 专属信息 ---")
    if system == 'windows':
        w_info = WindowsAdminDetector.get_privilege_info()
        for k, v in w_info.items():
            print(f"{k}: {v}")
    else:
        u_info = UnixAdminDetector.get_privilege_info()
        for k, v in u_info.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
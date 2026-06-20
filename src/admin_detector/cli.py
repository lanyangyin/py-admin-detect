#!/usr/bin/env python3
"""admin-detector 的命令行接口"""

import sys
import json
import argparse
from .core import AdminDetector


def print_human(info: dict) -> None:
    """打印人类可读的输出"""
    print("=== 管理员权限检测 ===")
    print(f"系统:          {info.get('system', 'unknown')}")
    print(f"用户:          {info.get('username', 'unknown')}")
    print(f"是否管理员:    {info.get('is_admin', False)}")
    if 'admin_method' in info:
        print(f"原因:          {info['admin_method']}")
    else:
        result = AdminDetector.check_admin_with_reason()
        print(f"原因:          {result.get('reason', 'unknown')}")

    # 显示 Unix 额外信息（如果存在）
    if 'euid' in info:
        print(f"EUID:          {info['euid']}")
        print(f"Sudo 用户:     {info.get('sudo_user', 'N/A')}")
        print(f"Sudo UID:      {info.get('sudo_uid', 'N/A')}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="检测当前进程是否拥有管理员/root 权限"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出结果（便于脚本解析）"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="输出详细信息（与 --json 同时使用时无效）"
    )
    args = parser.parse_args()

    info = AdminDetector.get_admin_info()
    reason_info = AdminDetector.check_admin_with_reason()
    info['reason'] = reason_info['reason']

    if args.json:
        json.dump(info, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write('\n')
    else:
        print_human(info)


if __name__ == "__main__":
    main()
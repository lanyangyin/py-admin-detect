# admin-detector-py

**跨平台管理员/root 权限检测工具** – 用于检测当前 Python 进程是否拥有 Windows 管理员、Linux/macOS root 或 sudo 权限。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 功能特点

- ✅ **跨平台支持** – Windows（UAC）、Linux、macOS（root/sudo）
- ✅ **零依赖** – 仅使用 Python 标准库
- ✅ **简单 API** – 一行 `AdminDetector.is_admin()` 返回布尔值
- ✅ **详细信息** – 可获取检测原因、EUID、sudo 用户等
- ✅ **命令行工具** – 直接运行 `python -m admin_detector.cli` 即可使用
- ✅ **轻量级** – 无需安装任何第三方包

---

## 使用方法

### 方式一：直接复制源码（推荐）

将 `src/admin_detector` 文件夹完整复制到你的项目目录中，然后导入使用：

```python
from admin_detector import AdminDetector

if AdminDetector.is_admin():
    print("✅ 当前拥有管理员/root 权限")
else:
    print("❌ 当前没有管理员/root 权限")

# 获取详细信息
info = AdminDetector.get_admin_info()
print(info)
# 示例输出：
# {
#   'is_admin': True,
#   'system': 'windows',
#   'username': 'Admin',
#   'admin_method': 'Windows UAC'
# }

# 获取检测原因
result = AdminDetector.check_admin_with_reason()
print(result['reason'])  # 例如："Windows UAC 管理员权限"
```

### 方式二：直接从源码运行（不复制）

将项目根目录添加到 `PYTHONPATH` 或在项目根目录下执行：


```bash
# 运行命令行工具
python -m admin_detector.cli

# 或者在自己的脚本中导入（当前工作目录为项目根目录）
python -c "from admin_detector import AdminDetector; print(AdminDetector.is_admin())"
```

命令行界面

克隆仓库后，运行：

```bash
python -m admin_detector.cli
```

输出示例（人类可读格式）：

```
=== 管理员权限检测 ===
系统:          windows
用户:          Admin
是否管理员:    True
原因:          Windows UAC 管理员权限
```

如需 JSON 格式输出（便于脚本解析）：

```bash
python -m admin_detector.cli --json
```

---

平台专属检测器

若需要更细粒度的控制，可使用以下类：

```python
from admin_detector import WindowsAdminDetector, UnixAdminDetector

# Windows 下
if WindowsAdminDetector.is_user_admin():
    print("Windows 管理员")

# Linux/macOS 下
if UnixAdminDetector.is_root():
    print("root 用户")
if UnixAdminDetector.is_sudo():
    print("通过 sudo 运行")
```

---

项目结构

```
admin-detector-py/
├── src/
│   └── admin_detector/
│       ├── __init__.py
│       ├── core.py          # 核心检测逻辑
│       ├── cli.py           # 命令行入口
│       └── exceptions.py    # 自定义异常
├── tests/
│   ├── __init__.py
│   └── test_core.py         # 单元测试
├── examples/
│   └── demo.py              # 使用示例
├── README.md
├── LICENSE
├── pyproject.toml           # （可选，仅本地开发用）
└── .gitignore
```

---

开发与测试

运行测试（使用内置的 unittest）：

```bash
python -m unittest discover tests
```

运行示例：

```bash
python examples/demo.py
```

---

许可证

本项目采用 MIT 许可证 – 详见 [LICENSE](LICENSE) 文件。

---

贡献

欢迎提交 Issue 或 Pull Request。
#!/usr/bin/env python3
"""
项目验证脚本

验证项目结构、依赖、配置是否正确。
"""

import sys
from pathlib import Path
from typing import List, Tuple


def check_file_exists(filepath: Path) -> bool:
    """检查文件是否存在"""
    return filepath.exists()


def verify_structure() -> List[Tuple[str, bool, str]]:
    """
    验证项目结构

    Returns:
        List[Tuple[str, bool, str]]: (检查项, 是否通过, 说明)
    """
    project_root = Path(__file__).parent.parent
    results = []

    # 必需的目录
    required_dirs = [
        "src/core/domain/models",
        "src/core/services",
        "src/core/repositories",
        "src/infrastructure/external/xiaohongshu",
        "src/infrastructure/external/ai",
        "src/infrastructure/database",
        "src/infrastructure/cache",
        "src/infrastructure/utils",
        "src/shared",
        "apps/api",
        "apps/cli",
        "docs/architecture",
        "docs/api",
        "docs/development",
        "tests/unit",
        "tests/integration",
    ]

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        exists = full_path.is_dir()
        results.append((f"目录: {dir_path}", exists, "✓" if exists else "✗"))

    # 必需的文件
    required_files = [
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        ".env.example",
        "pytest.ini",
        "src/core/domain/models/post.py",
        "src/core/domain/models/user.py",
        "src/core/domain/models/travel.py",
        "src/core/services/guide_collector.py",
        "src/core/services/itinerary_generator.py",
        "src/core/repositories/post_repository.py",
        "apps/api/main.py",
        "apps/cli/main.py",
        "docs/api/API_DESIGN.md",
        "docs/development/SETUP.md",
        "tests/conftest.py",
        "tests/unit/test_domain_models.py",
        "tests/unit/test_post_repository.py",
    ]

    for file_path in required_files:
        full_path = project_root / file_path
        exists = full_path.is_file()
        results.append((f"文件: {file_path}", exists, "✓" if exists else "✗"))

    return results


def verify_imports() -> List[Tuple[str, bool, str]]:
    """
    验证关键模块可以导入

    Returns:
        List[Tuple[str, bool, str]]: (检查项, 是否通过, 说明)
    """
    results = []

    # 添加项目根目录到 Python 路径
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    # 尝试导入关键模块
    imports_to_test = [
        ("src.core.domain.models.post", "PostDetail"),
        ("src.core.domain.models.user", "UserProfile"),
        ("src.core.domain.models.travel", "TravelPlan"),
        ("src.core.repositories.post_repository", "InMemoryPostRepository"),
        ("src.infrastructure.utils.config", "settings"),
        ("src.infrastructure.utils.logger", "setup_logger"),
    ]

    for module_name, class_name in imports_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            success = True
            msg = "✓"
        except Exception as e:
            success = False
            msg = f"✗ ({str(e)[:50]})"

        results.append((f"导入: {module_name}.{class_name}", success, msg))

    return results


def verify_dependencies() -> List[Tuple[str, bool, str]]:
    """
    验证关键依赖是否安装

    Returns:
        List[Tuple[str, bool, str]]: (检查项, 是否通过, 说明)
    """
    results = []

    dependencies = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pytest",
        "sqlalchemy",
        "redis",
        "click",
    ]

    for dep in dependencies:
        try:
            __import__(dep)
            success = True
            msg = "✓"
        except ImportError:
            success = False
            msg = "✗ (未安装)"

        results.append((f"依赖: {dep}", success, msg))

    return results


def print_results(title: str, results: List[Tuple[str, bool, str]]):
    """打印验证结果"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for item, success, msg in results:
        status_color = "\033[92m" if success else "\033[91m"  # 绿色/红色
        reset_color = "\033[0m"
        print(f"{status_color}{msg}{reset_color} {item}")

    print(f"\n通过: {passed}/{total} ({passed/total*100:.1f}%)")


def main():
    """主函数"""
    print("\n🔍 开始验证项目...")

    # 验证项目结构
    structure_results = verify_structure()
    print_results("📁 项目结构检查", structure_results)

    # 验证模块导入
    import_results = verify_imports()
    print_results("📦 模块导入检查", import_results)

    # 验证依赖
    dependency_results = verify_dependencies()
    print_results("🔧 依赖检查", dependency_results)

    # 总结
    all_results = structure_results + import_results + dependency_results
    total_passed = sum(1 for _, success, _ in all_results if success)
    total_checks = len(all_results)

    print(f"\n{'='*60}")
    print(f"总结")
    print(f"{'='*60}")
    print(f"总检查项: {total_checks}")
    print(f"通过: {total_passed}")
    print(f"失败: {total_checks - total_passed}")
    print(f"通过率: {total_passed/total_checks*100:.1f}%")

    if total_passed == total_checks:
        print("\n✅ 所有检查通过！项目结构完整。")
        return 0
    else:
        print("\n⚠️  部分检查失败，请检查上述错误。")
        return 1


if __name__ == "__main__":
    sys.exit(main())

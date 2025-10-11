#!/usr/bin/env python3
"""
MVP 启动脚本 - Super Browser User

快速启动 Web 应用的脚本。
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("=" * 60)
    print("🚀 Super Browser User - MVP")
    print("=" * 60)
    print()
    print("功能:")
    print("  ✅ 查看已收集的旅游攻略")
    print("  ✅ 查看生成的旅行计划")
    print("  ✅ 通过 API 生成新计划")
    print()
    print("访问地址:")
    print("  🌐 主页: http://localhost:8000")
    print("  📖 API 文档: http://localhost:8000/docs")
    print()
    print("提示:")
    print("  - 如果还没有攻略数据，请先运行 collect_guides.py")
    print("  - 按 Ctrl+C 停止服务")
    print()
    print("=" * 60)
    print()

    # 启动 Web 应用
    import uvicorn
    uvicorn.run("web_app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()

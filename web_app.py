"""
简单的 Web 应用 - 查看攻略和旅行计划

使用 FastAPI 提供 Web 界面和 API。
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.storage.local_storage import LocalStorage
from src.core.services.itinerary_generator import ItineraryGeneratorService
from src.core.domain.models.travel import TravelPlan, Itinerary, Budget
from datetime import datetime

# 初始化应用
app = FastAPI(title="Super Browser User - MVP")

# 创建模板目录
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))

# 初始化存储
storage = LocalStorage()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页 - 显示所有攻略"""
    posts = storage.get_all_posts()
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "posts": posts}
    )


@app.get("/posts", response_class=HTMLResponse)
async def posts_page(request: Request, destination: str = None):
    """攻略列表页面"""
    if destination:
        posts = storage.get_posts_by_destination(destination)
    else:
        posts = storage.get_all_posts()

    return templates.TemplateResponse(
        "posts.html",
        {"request": request, "posts": posts, "destination": destination}
    )


@app.get("/post/{post_id}", response_class=HTMLResponse)
async def post_detail(request: Request, post_id: str):
    """攻略详情页面"""
    post = storage.get_post(post_id)
    return templates.TemplateResponse(
        "post_detail.html",
        {"request": request, "post": post}
    )


@app.get("/plans", response_class=HTMLResponse)
async def plans_page(request: Request):
    """旅行计划列表页面"""
    plans = storage.get_all_plans()
    return templates.TemplateResponse(
        "plans.html",
        {"request": request, "plans": plans}
    )


@app.get("/plan/{plan_id}", response_class=HTMLResponse)
async def plan_detail(request: Request, plan_id: str):
    """旅行计划详情页面"""
    plan = storage.get_plan(plan_id)
    return templates.TemplateResponse(
        "plan_detail.html",
        {"request": request, "plan": plan}
    )


@app.post("/api/generate-plan")
async def generate_plan(destination: str, days: int = 3):
    """生成旅行计划 API"""
    # 获取该目的地的攻略
    posts = storage.get_posts_by_destination(destination)

    if not posts:
        return {"error": f"未找到 {destination} 的攻略，请先收集攻略"}

    # 生成行程
    generator = ItineraryGeneratorService()
    itinerary = await generator.generate_itinerary(
        destination=destination,
        days=days,
        guides=posts[:5]  # 只用前 5 篇
    )

    # 创建预算
    budget = Budget(
        transportation=days * 100.0,
        accommodation=days * 300.0,
        food=days * 200.0,
        tickets=days * 100.0,
        shopping=days * 100.0,
        other=days * 50.0
    )

    # 创建旅行计划
    plan = TravelPlan(
        plan_id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        user_id="web_user",
        destination=destination,
        days=days,
        itinerary=itinerary,
        budget=budget
    )

    # 保存
    storage.save_plan(plan)

    return {
        "success": True,
        "plan_id": plan.plan_id,
        "message": f"成功生成 {destination} {days} 天行程"
    }


@app.get("/api/posts")
async def api_get_posts(destination: str = None):
    """获取攻略列表 API"""
    if destination:
        posts = storage.get_posts_by_destination(destination)
    else:
        posts = storage.get_all_posts()

    return {
        "count": len(posts),
        "posts": [
            {
                "post_id": p.post_id,
                "title": p.title,
                "author": p.author,
                "likes": p.likes,
                "comments": p.comments,
                "collects": p.collects,
                "engagement_rate": round(p.engagement_rate, 2),
                "tags": p.tags
            }
            for p in posts
        ]
    }


@app.get("/api/plans")
async def api_get_plans():
    """获取旅行计划列表 API"""
    plans = storage.get_all_plans()
    return {
        "count": len(plans),
        "plans": plans
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 启动 Super Browser User Web 应用...")
    print("📖 访问: http://localhost:8000")
    print("📊 API 文档: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

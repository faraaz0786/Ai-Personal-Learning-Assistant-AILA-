from fastapi import APIRouter

from api.v1.endpoints import (
    health,
    insights,
    learn,
    library,
    progress,
    quizzes,
    sessions,
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(learn.router, prefix="/learn", tags=["learn"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(library.router, prefix="/library", tags=["library"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])

@api_router.get("/", tags=["root"])
async def api_v1_root():
    return {"version": "v1", "status": "active"}

from fastapi import APIRouter

from app.api.v1.endpoints import health, insights, learn, library, progress, quizzes, sessions


router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
router.include_router(learn.router, prefix="/learn", tags=["learn"])
router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
router.include_router(progress.router, prefix="/progress", tags=["progress"])
router.include_router(library.router, prefix="/library", tags=["library"])
router.include_router(insights.router, prefix="/insights", tags=["insights"])

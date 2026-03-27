from app.api.router import api_router
from app.core.app import create_app


app = create_app()
app.include_router(api_router)

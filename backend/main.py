from api.v1.router import api_router
from core.app import create_app


app = create_app()
app.include_router(api_router)

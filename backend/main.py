from core.app import create_app
from api.v1.router import api_router

# ✅ Use the factory to get all middleware and error handlers
app = create_app()

# ✅ Include the router with version prefix
app.include_router(api_router, prefix="/api/v1")



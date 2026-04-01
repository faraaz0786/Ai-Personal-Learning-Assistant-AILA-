import sys
import traceback

print("AILA Backend: Starting main.py initialization...", flush=True)

try:
    from core.app import create_app
    from api.v1.router import api_router

    # [LIFESPAN] Use the factory to get all middleware and error handlers
    app = create_app()

    # [ROUTING] Include the router with version prefix
    app.include_router(api_router, prefix="/api/v1")
except Exception as e:
    print("FATAL STARTUP ERROR:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(3)



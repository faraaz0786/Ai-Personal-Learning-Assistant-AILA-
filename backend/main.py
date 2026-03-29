from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router
from middleware.session import SessionContextMiddleware

app = FastAPI()

# ✅ IMPORTANT: exact origins (NO slash at end)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://ai-personal-learning-assistant-aila.vercel.app",
]

# ✅ Session context for cookie-based state
app.add_middleware(SessionContextMiddleware)

# ✅ MUST BE ADDED BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DEBUGGING LOGS
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"🚀 Incoming: {request.method} {request.url}")
    response = await call_next(request)
    print(f"✅ Status: {response.status_code}")
    return response

# ✅ THEN include router
app.include_router(api_router, prefix="/api/v1")



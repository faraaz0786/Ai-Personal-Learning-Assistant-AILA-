from fastapi import FastAPI
from api.v1.router import api_router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://ai-personal-learning-assistant-aila.vercel.app",
    # "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # ❗ NOT "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

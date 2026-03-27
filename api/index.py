from app.main import app

# Vercel Serverless Function entry point
# This bridges the FastAPI app to Vercel's Python runtime
handler = app

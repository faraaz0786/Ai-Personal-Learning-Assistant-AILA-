from backend.main import app

# Vercel Serverless Function entry point
# Bridges the FastAPI app in /backend to Vercel's runtime
handler = app

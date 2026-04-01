import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

async def test_db():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    print(f"🔍 Testing DB URL (masked): {db_url.split('@')[-1]}")
    
    try:
        engine = create_async_engine(db_url)
        print("⏳ Attempting connection...")
        async with engine.connect() as conn:
            print("⏳ Running SELECT 1...")
            result = await asyncio.wait_for(conn.execute(text("SELECT 1")), timeout=10)
            print(f"✅ Connection successful: {result.fetchone()}")
            
            print("⏳ Checking for sessions table...")
            result = await asyncio.wait_for(conn.execute(text("SELECT count(*) FROM sessions")), timeout=10)
            print(f"✅ Table 'sessions' exists. Count: {result.scalar()}")
            
        await engine.dispose()
    except Exception as e:
        print(f"❌ DB TEST FAILED: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_db())

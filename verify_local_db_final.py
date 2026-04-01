import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

async def test_db_pooler_fix():
    load_dotenv()
    project_ref = "eapmxlzuszoknkkoegmc"
    # Try the project-specific username format for the pooler
    # Use the encoded password from .env but fix the user
    db_url = f"postgresql+asyncpg://postgres.{project_ref}:123far%40%40Zz%23786@db.{project_ref}.supabase.co:6543/postgres"
    
    print(f"🔍 Testing Pooler Fix URL (masked): db.{project_ref}.supabase.co:6543")
    
    try:
        engine = create_async_engine(db_url)
        print("⏳ Attempting connection...")
        async with engine.connect() as conn:
            result = await asyncio.wait_for(conn.execute(text("SELECT 1")), timeout=10)
            print(f"✅ Connection successful: {result.fetchone()}")
        await engine.dispose()
    except Exception as e:
        print(f"❌ POOLER TEST FAILED: {type(e).__name__}: {e}")

async def test_db_direct_fix():
    load_dotenv()
    project_ref = "eapmxlzuszoknkkoegmc"
    # Try direct port with the same encoded password
    db_url = f"postgresql+asyncpg://postgres:123far%40%40Zz%23786@db.{project_ref}.supabase.co:5432/postgres"
    
    print(f"🔍 Testing Direct Port URL (masked): db.{project_ref}.supabase.co:5432")
    
    try:
        engine = create_async_engine(db_url)
        print("⏳ Attempting connection...")
        async with engine.connect() as conn:
            result = await asyncio.wait_for(conn.execute(text("SELECT 1")), timeout=10)
            print(f"✅ Connection successful: {result.fetchone()}")
        await engine.dispose()
    except Exception as e:
        print(f"❌ DIRECT TEST FAILED: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("🚀 Starting Local DB Verification...")
    asyncio.run(test_db_pooler_fix())
    print("-" * 20)
    asyncio.run(test_db_direct_fix())

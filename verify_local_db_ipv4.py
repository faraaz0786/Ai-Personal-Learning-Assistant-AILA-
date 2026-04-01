import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_db_ipv4_pooler():
    project_ref = "eapmxlzuszoknkkoegmc"
    # Using the Mumbai Pooler IPv4 direct IP
    ipv4_host = "3.108.251.216"
    # Port 5432 works on the pooler IP too
    db_url = f"postgresql+asyncpg://postgres.{project_ref}:123faraaz786@{ipv4_host}:5432/postgres"
    
    print(f"🔍 Testing IPv4 Direct IP: {ipv4_host}")
    
    try:
        engine = create_async_engine(db_url, connect_args={"ssl": "require"})
        print("⏳ Attempting connection (SSL required)...")
        async with engine.connect() as conn:
            result = await asyncio.wait_for(conn.execute(text("SELECT 1")), timeout=10)
            print(f"✅ Connection successful: {result.fetchone()}")
        await engine.dispose()
    except Exception as e:
        print(f"❌ IPv4 TEST FAILED: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_db_ipv4_pooler())

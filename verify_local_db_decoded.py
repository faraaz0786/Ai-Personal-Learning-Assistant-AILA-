import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import unquote

async def test_db_decoded():
    load_dotenv()
    raw_url = os.getenv("DATABASE_URL")
    
    # Manually decode the password part if it looks encoded
    if "%" in raw_url:
        print("💡 Detected '%' in URL, attempting to decode...")
        # Note: This is a bit sensitive, but we only print for debugging
        decoded_url = unquote(raw_url)
    else:
        decoded_url = raw_url

    print(f"🔍 Testing Decoded DB URL (masked host): {decoded_url.split('@')[-1]}")
    
    try:
        engine = create_async_engine(decoded_url)
        print("⏳ Attempting connection...")
        async with engine.connect() as conn:
            result = await asyncio.wait_for(conn.execute(text("SELECT 1")), timeout=10)
            print(f"✅ Connection successful: {result.fetchone()}")
        await engine.dispose()
    except Exception as e:
        print(f"❌ DB TEST FAILED: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_db_decoded())

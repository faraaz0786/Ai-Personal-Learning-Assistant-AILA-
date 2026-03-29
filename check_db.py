
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

# Using the URL from the user's .env
DATABASE_URL = "postgresql+asyncpg://postgres:123far%40%40Zz%23786@db.eapmxlzuszoknkkoegmc.supabase.co:5432/postgres"

async def main():
    print(f"Connecting to {DATABASE_URL.split('@')[1]}...")
    engine = create_async_engine(DATABASE_URL)
    
    try:
        async with engine.connect() as conn:
            # Check for tables
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
            
            # Check if sessions exists
            if 'sessions' in tables:
                print("✅ 'sessions' table exists.")
            else:
                print("❌ 'sessions' table MISSING!")
                
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())

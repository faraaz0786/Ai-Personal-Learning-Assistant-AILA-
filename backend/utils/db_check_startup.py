import asyncio
import socket
from sqlalchemy.ext.asyncio import create_async_engine
from core.config import get_settings

async def check_db_connectivity():
    settings = get_settings()
    db_url = settings.database_url
    
    print(f"\n--- 🔍 Production DB Health Check ---")
    print(f"Target: {db_url.split('@')[-1]}")
    
    # 1. Test DNS Resolution
    try:
        hostname = db_url.split('@')[-1].split(':')[0]
        print(f"🌐 Resolving hostname: {hostname}")
        addrs = socket.getaddrinfo(hostname, None)
        for addr in addrs:
            print(f"📍 Resolved IP: {addr[4][0]} (Family: {addr[0]})")
    except Exception as e:
        print(f"❌ DNS Resolution Failed: {str(e)}")

    # 2. Test Engine Connection
    try:
        engine = create_async_engine(db_url)
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed!")
        print(f"📝 Error Details: {str(e)}")
        if "Network is unreachable" in str(e):
            print("💡 PRO TIP: This is often an IPv6 vs IPv4 mismatch on Render. "
                  "Ensure you are using the Supabase Connection Pooler (port 6543) "
                  "and check if Render supports IPv6 for your region.")
    
    print(f"-----------------------------------\n")

if __name__ == "__main__":
    asyncio.run(check_db_connectivity())

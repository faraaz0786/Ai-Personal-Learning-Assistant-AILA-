import asyncio
import socket
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from core.config import get_settings

logger = logging.getLogger(__name__)

async def check_db_connectivity() -> bool:
    settings = get_settings()
    db_url = settings.database_url
    
    # Mask password for logs but verify structure
    try:
        user_part = db_url.split('://')[-1].split('@')[0]
        username = user_part.split(':')[0]
        logger.info(f"👤 Username Check: structure={'[user].[project]' if '.' in username else 'simple'}, length={len(username)}")
        if '.' not in username:
            logger.warning("⚠️ WARNING: Username does NOT contain a dot. Supabase Pooler (port 6543) REQUIRES 'username.project-ref' format.")
    except Exception as e:
        logger.error(f"Failed to parse username for diagnostics: {e}")

    masked_url = db_url.split('@')[-1]
    logger.info(f"🔍 Starting Production DB Health Check on: {masked_url}")
    
    # 1. Test DNS Resolution (Prefer IPv4)
    hostname = db_url.split('@')[-1].split(':')[0]
    try:
        logger.info(f"🌐 Resolving hostname: {hostname}")
        # AF_INET forces IPv4
        addrs = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
        for addr in addrs:
            logger.info(f"📍 Resolved IPv4: {addr[4][0]}")
    except Exception as e:
        logger.error(f"❌ DNS Resolution Failed for {hostname}: {str(e)}")
        # Check if it resolves at all (might be IPv6 only?)
        try:
            any_addrs = socket.getaddrinfo(hostname, None)
            for addr in any_addrs:
                logger.warning(f"⚠️ Found non-IPv4 address: {addr[4][0]} (Family: {addr[0]})")
        except:
            pass
        return False

    # 2. Test Engine Connection
    try:
        # We create a temporary engine just for the check
        engine = create_async_engine(
            db_url,
            connect_args={"ssl": "require", "command_timeout": 10}
        )
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        await engine.dispose()
        logger.info("✅ Database connection successful!")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        if "Network is unreachable" in str(e) or "ETIMEDOUT" in str(e):
            logger.error("💡 CAUSE: This is a network routing issue. Render likely cannot reach the Supabase IP via its current egress.")
        return False

if __name__ == "__main__":
    # For local manual testing
    logging.basicConfig(level=logging.INFO)
    asyncio.run(check_db_connectivity())

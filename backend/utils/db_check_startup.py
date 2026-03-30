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
        # Only warn about the dot-notation if actually using the pooler port 6543
        if '.' not in username and ":6543" in db_url:
            logger.warning("⚠️ WARNING: Username does NOT contain a dot. Supabase Pooler (port 6543) REQUIRES 'username.project-ref' format.")
        elif '.' in username and ":5432" in db_url:
            logger.info("ℹ️ Note: Username contains a project-ref (dot-notation), which is fine but usually optional for direct port 5432.")
    except Exception as e:
        logger.error(f"Failed to parse username for diagnostics: {e}")

    masked_url = db_url.split('@')[-1]
    logger.info(f"🔍 Starting Production DB Health Check on: {masked_url}")
    
    # 0. Wait for network stack to stabilize (Render/Container quirk)
    logger.info("⏳ Waiting 5s for network interfaces to stabilize...")
    await asyncio.sleep(5)

    # 1. Test DNS Resolution with IPv4 Preference and RETRY
    import re
    project_ref = "eapmxlzuszoknkkoegmc"
    
    # Correction logic (redundant but safe)
    if "pooler.supabase.com" in db_url or ":6543" in db_url:
        db_url = re.sub(r"@[^/:]+(:[0-9]+)?", f"@db.{project_ref}.supabase.co:5432", db_url)
        db_url = db_url.replace(f"postgres.{project_ref}", "postgres")
        
    hostname = db_url.split("@")[1].split(":")[0].split("/")[0]
    
    max_retries = 3
    resolved_ip = None
    for attempt in range(max_retries):
        try:
            logger.info(f"🌐 Resolving hostname: {hostname} (Attempt {attempt+1}/{max_retries})")
            # Try IPv4 first (AF_INET)
            try:
                addrs = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
                resolved_ip = addrs[0][4][0]
                logger.info(f"📍 Resolved IPv4: {resolved_ip}")
            except:
                # Fallback to any family (AF_UNSPEC) if IPv4 resolution fails
                addrs = socket.getaddrinfo(hostname, None)
                resolved_ip = addrs[0][4][0]
                family = "IPv6" if addrs[0][0] == socket.AF_INET6 else "Unknown"
                logger.info(f"📍 IPv4 Resolution failed, found {family}: {resolved_ip}")
            break 
        except Exception as e:
            logger.info(f"⏳ DNS Attempt {attempt+1} postponed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2)
            else:
                logger.warning(f"⚠️ DNS resolution could not verify {hostname} during startup (will retry on first request)")

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
        # Downgrade to warning since we are in non-blocking mode
        logger.warning(f"⚠️ Startup connection check failed: {str(e)}")
        if "Network is unreachable" in str(e) or "ETIMEDOUT" in str(e):
            logger.info("💡 CAUSE: Network interface partially ready. The app will automatically connect when the first request arrives.")
        return False

if __name__ == "__main__":
    # For local manual testing
    logging.basicConfig(level=logging.INFO)
    asyncio.run(check_db_connectivity())

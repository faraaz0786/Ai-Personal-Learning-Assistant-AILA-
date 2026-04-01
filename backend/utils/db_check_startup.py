import asyncio
import logging
from core.config import get_settings

logger = logging.getLogger(__name__)

async def check_db_connectivity() -> bool:
    """Quick, non-blocking database connectivity check at startup."""
    settings = get_settings()
    db_url = settings.database_url

    # Log masked URL for diagnostics
    if "@" in db_url:
        masked_url = db_url.split('@')[-1]
    else:
        masked_url = db_url
    logger.info(f"Starting DB Health Check on: {masked_url}")

    # Skip DNS checks for SQLite
    if db_url.startswith("sqlite"):
        logger.info("SQLite detected, skipping network checks.")
    else:
        # Brief pause for container network initialization (Render quirk)
        logger.info("Waiting 2s for network interfaces to stabilize...")
        await asyncio.sleep(2)

    # Actual DB connectivity test
    from db.session import engine
    from sqlalchemy import text
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            logger.info("Database connectivity check passed!")
            return True
    except Exception as e:
        logger.warning(f"Startup connection check failed: {str(e)}")
        if "Network is unreachable" in str(e) or "ETIMEDOUT" in str(e):
            logger.info("CAUSE: Network interface partially ready. The app will connect on first request.")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(check_db_connectivity())

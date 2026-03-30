from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

import os
import sys

print(f"📁 Loading configuration from {os.path.abspath(__file__)}", flush=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = Field(default="AILA", alias="APP_NAME")
    environment: Literal["development", "test", "production"] = Field(
        default="development", alias="ENVIRONMENT"
    )
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    cors_origins: list[str] | str = Field(
        default=["http://localhost:3000"], alias="CORS_ORIGINS"
    )
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    session_cookie_name: str = Field(
        default="aila_session", alias="SESSION_COOKIE_NAME"
    )
    session_ttl_days: int = Field(default=30, alias="SESSION_TTL_DAYS")

    # Supabase PostgreSQL via Supavisor connection pooler
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.eapmxlzuszoknkkoegmc.supabase.co:5432/postgres",
        alias="DATABASE_URL",
    )

    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")
    llm_model_primary: str = Field(default="gpt-4o", alias="LLM_MODEL_PRIMARY")
    llm_model_fallback: str = Field(
        default="gpt-4o-mini", alias="LLM_MODEL_FALLBACK"
    )
    llm_timeout_seconds: int = Field(default=30, alias="LLM_TIMEOUT_SECONDS")
    llm_prompt_version: str = Field(default="1.0", alias="LLM_PROMPT_VERSION")
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str | None = Field(default=None, alias="GROQ_MODEL")

    @field_validator("debug", mode="before")
    @classmethod
    def coerce_debug(cls, value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug"}:
                return True
            if normalized in {"0", "false", "no", "off", "release"}:
                return False
        return bool(value)

    @field_validator("database_url", mode="after")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        # Aggressive Auto-Correction for Supabase Connectivity Issues
        import re
        
        # 1. Detect Project Ref (eapmxlzuszoknkkoegmc)
        project_ref = "eapmxlzuszoknkkoegmc"
        
        # 2. If we see the failing Mumbai pooler, FORCE swap to the verified Direct Host
        if "pooler.supabase.com" in v or ":6543" in v:
            print(f"⚠️  [DB_GUARD] Detected problematic pooler configuration. Forcing direct host redirect.")
            # Use regex to replace the host and port while keeping user/pass/db
            # Format: postgresql+asyncpg://user:pass@host:port/db
            v = re.sub(r"@[^/:]+(:[0-9]+)?", f"@db.{project_ref}.supabase.co:5432", v)
            
            # Ensure standard username (no dot-notation for direct connection)
            v = v.replace(f"postgres.{project_ref}", "postgres")
            
        # 3. Always enforce SSL and disable prepared statement cache for stability
        if "ssl" not in v:
            separator = "&" if "?" in v else "?"
            v = f"{v}{separator}ssl=require"
        
        if "prepared_statement_cache_size=0" not in v:
            separator = "&" if "?" in v else "?"
            v = f"{v}{separator}prepared_statement_cache_size=0"
            
        return v

    @model_validator(mode="after")
    def validate_config(self) -> "Settings":
        if self.environment.lower() == "production":
            if "[YOUR-PASSWORD]" in self.database_url:
                raise ValueError(
                    "DATABASE_URL contains the '[YOUR-PASSWORD]' placeholder. "
                    "Please set the actual DATABASE_URL in your Render environment variables."
                )
        return self
    def validate_groq_config(self) -> "Settings":
        if self.llm_provider == "groq":
            if not self.groq_api_key or self.groq_api_key == "not_used":
                raise ValueError("Groq API key not configured for llm_provider='groq'")
            if not self.groq_model and not self.llm_model_primary:
                raise ValueError("Primary LLM model not configured for llm_provider='groq'")
            # If groq_model is provided in env but llm_model_primary is not set to it, we can override or use groq_model.
            # We'll rely on the service to use Settings.groq_model
        return self


@lru_cache
def get_settings() -> Settings:
    try:
        # 🚀 AUTO-DETECT RENDER / PRODUCTION
        if os.getenv("RENDER"):
            os.environ["ENVIRONMENT"] = "production"
            
        settings = Settings()
        
        # 🧪 DIAGNOSTIC LOGGING: Log DB Host for production debugging
        env_name = settings.environment.lower()
        if env_name == "production":
            from urllib.parse import urlparse
            try:
                parsed = urlparse(settings.database_url)
                print(f"⚙️ Connecting to Database Host: {parsed.hostname}", flush=True)
            except:
                pass

        if isinstance(settings.cors_origins, str):
            settings.cors_origins = [
                origin.strip()
                for origin in settings.cors_origins.split(",")
                if origin.strip()
            ]
        return settings
    except Exception as e:
        print("❌ CONFIGURATION ERROR: Pydantic Validation failed!", file=sys.stderr)
        print(f"Details: {str(e)}", file=sys.stderr)
        sys.stderr.flush()
        sys.stdout.flush()
        raise

# AILA Enterprise Backend

A production-grade, highly resilient backend foundation for the AI Personal Learning Assistant.

## Architecture
- **Web App**: FastAPI natively tracing asynchronous context variables and outputting single-line JSON structured logs.
- **Database**: PostgreSQL (SQLAlchemy Async), fully instrumented for sub-millisecond query latency breakdowns across universally inherited base repositories.
- **Cache**: Redis, optimized with deterministic content hashing and mutual-exclusion distributed locks (`set nx=True`) completely isolating the application from devastating LLM cache stampedes.
- **AI Core**: LLM providers enveloped by Tenacity exponentially backing off to intelligent `CircuitBreakers`, which fail-fast and degrade gracefully to safe string payloads upon total upstream outages. Dedicated Prompt Injection Filters and Regex PII detectors sanitize data bounds continuously.

## Local Setup
1. Copy `.env.example` to `.env`. Required overrides: `OPENAI_API_KEY` and `DATABASE_URL`.
2. Instantiate isolated environments:
   ```bash
   make install
   ```
3. Boot resilient infrastructure:
   ```bash
   docker compose up -d postgres redis
   ```

## Developer Commands
A standardized `Makefile` completely manages continuous developer workflows:
- `make dev`: Spin up the `uvicorn` instance locally trailing port `8000`.
- `make test`: Executes all async API workflows and strictly verifies `app/prompts` Jinja2 LLM template regressions.
- `make format`: Syntactically aligns spacing using Python `black` and `ruff`.
- `make lint`: Traps anti-patterns checking against strict compliance rules via Ruff.
- `make clean`: Sweeps ephemeral caches guaranteeing clean container builds.

## Key APIs & Metrics
- `GET /metrics`: Direct insight scraping engine for Prometheus visualizing throughput, absolute Latency averages, and Generative Cache efficiencies (`ai_cache_hits`).
- `GET /api/v1/health`: Readiness checks verifying Database and Redis availability.

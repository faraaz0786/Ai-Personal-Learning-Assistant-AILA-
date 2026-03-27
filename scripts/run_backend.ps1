$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
  throw "Virtual environment not found. Run scripts/bootstrap_backend.ps1 first."
}

& ".\.venv\Scripts\uvicorn.exe" app.main:app --reload --host 0.0.0.0 --port 8000

$ErrorActionPreference = "Stop"

Push-Location frontend
try {
  if (-not (Test-Path "node_modules")) {
    npm install
  }

  npm run dev -- --host 0.0.0.0 --port 3000
} finally {
  Pop-Location
}

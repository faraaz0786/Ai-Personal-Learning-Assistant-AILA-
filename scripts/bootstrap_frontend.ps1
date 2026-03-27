$ErrorActionPreference = "Stop"

Push-Location frontend
try {
  npm install
  Write-Host "Frontend environment is ready."
} finally {
  Pop-Location
}

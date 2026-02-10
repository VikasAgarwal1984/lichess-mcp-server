# build.ps1 - Setup environment and dependencies

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$OriginalLocation = Get-Location

try {
    Set-Location $ProjectRoot
    Write-Host "Setting up Lichess MCP Server environment in $ProjectRoot" -ForegroundColor Cyan

    # Create virtual environment if it doesn't exist
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv .venv
    }

    # Activate and install dependencies
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & .venv\Scripts\python.exe -m pip install --upgrade pip
    & .venv\Scripts\python.exe -m pip install -r requirements.txt

    # Handle .env file
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
            Copy-Item ".env.example" ".env"
        }
        Write-Host "IMPORTANT: Please edit .env and add your LICHESS_API_TOKEN." -ForegroundColor Red
    }

    Write-Host "Build complete! Use scripts\start.ps1 to run the server." -ForegroundColor Green
}
finally {
    # Restore original terminal path
    Set-Location $OriginalLocation
}

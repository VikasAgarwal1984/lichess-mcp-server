# start.ps1 - Run the MCP server in default (stdio) mode

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$OriginalLocation = Get-Location

try {
    Set-Location $ProjectRoot

    if (-not (Test-Path ".venv")) {
        Write-Host "Virtual environment not found. Running build.ps1 first..." -ForegroundColor Yellow
        & "$PSScriptRoot\build.ps1"
    }

    Write-Host "Starting Lichess MCP Server (stdio mode)..." -ForegroundColor Green
    & .venv\Scripts\python.exe -m src.server
}
finally {
    # Restore original terminal path
    Set-Location $OriginalLocation
}

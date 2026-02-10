param (
    [Parameter(Mandatory=$false)]
    [int]$Port = 8000
)

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$OriginalLocation = Get-Location

try {
    Set-Location $ProjectRoot
    Write-Host "Starting Lichess MCP Server with SSE transport on port $Port" -ForegroundColor Green
    Write-Host "Server will be available at http://localhost:$Port/sse" -ForegroundColor Cyan
    & .venv\Scripts\python.exe -m src.server --transport sse --port $Port
}
finally {
    Set-Location $OriginalLocation
}

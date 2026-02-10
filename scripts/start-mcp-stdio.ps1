$ProjectRoot = (Get-Item "$PSScriptRoot\..").FullName
$OriginalLocation = Get-Location

try {
    Set-Location $ProjectRoot
    $env:PYTHONPATH = $ProjectRoot
    $env:FASTMCP_NO_BANNER = "1"
    $PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
    
    if (Test-Path $PythonExe) {
        & $PythonExe -m src.server --transport stdio
    } else {
        [Console]::Error.WriteLine("Error: Virtual environment not found at $PythonExe")
        exit 1
    }
}
finally {
    Set-Location $OriginalLocation
}

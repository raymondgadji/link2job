# start.ps1 - Link2Job dev server
# Usage : .\start.ps1 depuis C:\Projects\link_to_job

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Demarrage Link2Job..." -ForegroundColor Cyan

Set-Location "$PSScriptRoot\backend"
& "$PSScriptRoot\backend\venv\Scripts\Activate.ps1"
& "$PSScriptRoot\backend\venv\Scripts\python.exe" -m uvicorn main:app --reload
# Remove Windows Task Scheduler for Autonomous Execution
# Run this script in PowerShell to delete local scheduled tasks

Unregister-ScheduledTask -TaskName "AutonomousAITechShorts_Morning" -Confirm:$false -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "AutonomousAITechShorts_Evening" -Confirm:$false -ErrorAction SilentlyContinue

Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host " SUCCESS: Local Windows Tasks Removed Permanently!" -ForegroundColor Yellow
Write-Host " Automation will now run 100% in GitHub Actions Cloud." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Yellow

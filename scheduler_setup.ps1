# Setup Windows Task Scheduler for Autonomous 2x Daily Execution
# Run this script as Administrator to register tasks at 9:00 AM and 6:00 PM.

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$PSScriptRoot\run_daily.bat`""
$trigger1 = New-ScheduledTaskTrigger -Daily -At 9:00AM
$trigger2 = New-ScheduledTaskTrigger -Daily -At 6:00PM

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -TaskName "AutonomousAITechShorts_Morning" -Action $action -Trigger $trigger1 -Principal $principal -Description "Daily Morning AI Tech Short Automation" -Force
Register-ScheduledTask -TaskName "AutonomousAITechShorts_Evening" -Action $action -Trigger $trigger2 -Principal $principal -Description "Daily Evening AI Tech Short Automation" -Force

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " SUCCESS: Scheduled 2x Daily Autonomous Tasks!" -ForegroundColor Green
Write-Host " 1. AutonomousAITechShorts_Morning (9:00 AM)" -ForegroundColor Cyan
Write-Host " 2. AutonomousAITechShorts_Evening (6:00 PM)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green

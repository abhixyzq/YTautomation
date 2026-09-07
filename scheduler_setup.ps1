# Setup Windows Task Scheduler for Autonomous Multi-Daily Execution
# Run this script as Administrator to register tasks at 6:00 AM, 8:00 AM, 1:00 PM, and 8:00 PM.

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$PSScriptRoot\run_daily.bat`""
$trigger1 = New-ScheduledTaskTrigger -Daily -At 6:00AM
$trigger_long = New-ScheduledTaskTrigger -Daily -At 8:00AM
$trigger2 = New-ScheduledTaskTrigger -Daily -At 1:00PM
$trigger3 = New-ScheduledTaskTrigger -Daily -At 8:00PM

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest

# CRITICAL: Allow running on Battery power, start if missed, and require network
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

Register-ScheduledTask -TaskName "AutonomousAITechShorts_Morning" -Action $action -Trigger $trigger1 -Principal $principal -Settings $settings -Description "Daily Morning 6:00 AM Short Automation" -Force
Register-ScheduledTask -TaskName "AutonomousAITech_LongEpisode" -Action $action -Trigger $trigger_long -Principal $principal -Settings $settings -Description "Daily 8:00 AM Long Video Automation" -Force
Register-ScheduledTask -TaskName "AutonomousAITechShorts_Afternoon" -Action $action -Trigger $trigger2 -Principal $principal -Settings $settings -Description "Daily Afternoon 1:00 PM Short Automation" -Force
Register-ScheduledTask -TaskName "AutonomousAITechShorts_Evening" -Action $action -Trigger $trigger3 -Principal $principal -Settings $settings -Description "Daily Evening 8:00 PM Short Automation" -Force

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " SUCCESS: Scheduled Autonomous Tasks!" -ForegroundColor Green
Write-Host " 1. AutonomousAITechShorts_Morning (6:00 AM)" -ForegroundColor Cyan
Write-Host " 2. AutonomousAITech_LongEpisode (8:00 AM)" -ForegroundColor Magenta
Write-Host " 3. AutonomousAITechShorts_Afternoon (1:00 PM)" -ForegroundColor Cyan
Write-Host " 4. AutonomousAITechShorts_Evening (8:00 PM)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green

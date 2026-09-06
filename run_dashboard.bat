@echo off
title AutoTube Mobile Remote Dashboard
cd /d "%~dp0"
echo ===============================================================
echo   AutoTube Studio - Mobile Remote Control Dashboard
echo ===============================================================
echo Starting server on http://0.0.0.0:5000...
echo Connect from your phone on the same Wi-Fi network!
echo ===============================================================
python dashboard.py
pause

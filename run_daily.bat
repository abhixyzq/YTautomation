@echo off
cd /d "%~dp0"
echo =======================================================
echo STARTING DAILY AI AVATAR TECH SHORTS RUN
echo =======================================================

:: Run the pipeline and publish
python main.py --publish

echo =======================================================
echo RUN FINISHED AT %TIME%
echo =======================================================
exit /b 0

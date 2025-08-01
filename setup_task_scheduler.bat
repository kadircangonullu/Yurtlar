@echo off
echo Setting up AI Product Approval Task Scheduler...

REM Get the current directory where the Python script is located
set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%product_approval_ai.py

REM Create the task
schtasks /create /tn "AI Product Approval" /tr "python \"%PYTHON_SCRIPT%\"" /sc minute /mo 10 /ru "SYSTEM" /f

if %ERRORLEVEL% EQU 0 (
    echo Task created successfully!
    echo The AI approval script will run every 10 minutes.
    echo.
    echo To check the task status, run: schtasks /query /tn "AI Product Approval"
    echo To stop the task, run: schtasks /delete /tn "AI Product Approval" /f
    echo.
    echo Logs will be saved to: C:\AI_Approval_Logs\
) else (
    echo Failed to create task. Please run as Administrator.
    echo.
    echo Manual setup instructions:
    echo 1. Open Task Scheduler (taskschd.msc)
    echo 2. Create Basic Task
    echo 3. Name: "AI Product Approval"
    echo 4. Trigger: Every 10 minutes
    echo 5. Action: Start a program
    echo 6. Program: python
    echo 7. Arguments: "%PYTHON_SCRIPT%"
    echo 8. Start in: "%SCRIPT_DIR%"
)

pause 
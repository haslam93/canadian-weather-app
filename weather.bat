@echo off
REM Canadian Weather CLI App - Windows Batch Script
REM Usage: weather.bat <postal_code>

if "%1"=="" (
    echo Usage: weather.bat ^<postal_code^>
    echo Example: weather.bat K1A0A6
    echo.
    echo Canadian postal code formats:
    echo   A1A 1A1 ^(with space^)
    echo   A1A1A1 ^(without space^)
    pause
    exit /b 1
)

python weather_app.py %1
pause

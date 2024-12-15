@echo off
echo Installing required libraries...

:: Install yfinance with specific options
pip install yfinance --upgrade --no-cache-dir

:: Install all other dependencies from requirements.txt
pip install -r requirements.txt

echo Installation complete!
pause

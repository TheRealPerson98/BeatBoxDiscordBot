@echo off

REM Start the bot
start cmd /k "cd backend && python main.py"

REM
start cmd /k "cd backend && python -m web.app"

REM Start the React app
start cmd /k "cd frontend && npm start"

exit

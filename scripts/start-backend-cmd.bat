@echo off
REM 使用CMD启动后端服务

echo 正在启动后端服务...
cd backend
cmd /c "..\venv\Scripts\activate.bat && python manage.py runserver"

pause 
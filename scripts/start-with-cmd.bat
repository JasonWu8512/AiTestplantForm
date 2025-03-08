@echo off
REM 使用CMD启动项目
cd /d %~dp0
cd ..

echo 请选择要启动的服务：
echo 1. 启动后端服务
echo 2. 启动前端服务
echo 3. 启动Docker服务
echo 4. 退出
echo.

set /p choice=请输入选项(1-4): 

if "%choice%"=="1" (
    echo 正在启动后端服务...
    cd backend
    cmd /c "..\venv\Scripts\activate.bat && python manage.py runserver"
    cd ..
) else if "%choice%"=="2" (
    echo 正在启动前端服务...
    cd frontend
    cmd /c "npm run dev"
    cd ..
) else if "%choice%"=="3" (
    echo 正在启动Docker服务...
    call %~dp0\docker-menu.bat
) else if "%choice%"=="4" (
    exit
) else (
    echo 无效的选项！
    timeout /t 2 >nul
    call %~dp0\start-with-cmd.bat
) 
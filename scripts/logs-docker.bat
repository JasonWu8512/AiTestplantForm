@echo off
REM 使用CMD查看Docker服务日志

echo 请选择要查看的服务日志：
echo 1. 所有服务
echo 2. 后端服务
echo 3. 前端服务
echo 4. 数据库服务
echo 5. Redis服务
echo 6. Celery Worker服务
echo 7. Celery Beat服务
echo.

set /p choice=请输入选项(1-7): 

if "%choice%"=="1" (
    echo 正在查看所有服务的日志...
    cmd /c "docker-compose logs"
) else if "%choice%"=="2" (
    echo 正在查看后端服务的日志...
    cmd /c "docker-compose logs backend"
) else if "%choice%"=="3" (
    echo 正在查看前端服务的日志...
    cmd /c "docker-compose logs frontend"
) else if "%choice%"=="4" (
    echo 正在查看数据库服务的日志...
    cmd /c "docker-compose logs db"
) else if "%choice%"=="5" (
    echo 正在查看Redis服务的日志...
    cmd /c "docker-compose logs redis"
) else if "%choice%"=="6" (
    echo 正在查看Celery Worker服务的日志...
    cmd /c "docker-compose logs celery-worker"
) else if "%choice%"=="7" (
    echo 正在查看Celery Beat服务的日志...
    cmd /c "docker-compose logs celery-beat"
) else (
    echo 无效的选项！
)

echo.
pause 
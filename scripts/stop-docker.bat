@echo off
REM 使用CMD停止Docker服务

echo 正在停止Docker服务...
cmd /c "docker-compose down"

echo.
echo Docker服务已停止！
echo.

pause 
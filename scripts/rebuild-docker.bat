@echo off
REM 使用CMD重新构建Docker服务

echo 正在重新构建Docker服务...
cmd /c "docker-compose up -d --build"

echo.
echo Docker服务已重新构建并启动！
echo 前端访问地址: http://localhost
echo 后端API访问地址: http://localhost/api/
echo.

pause 
@echo off
REM 使用CMD启动Docker服务

echo 正在启动Docker服务...
cmd /c "docker-compose up -d"

echo.
echo Docker服务已启动！
echo 前端访问地址: http://localhost
echo 后端API访问地址: http://localhost/api/
echo 默认管理员账号: admin
echo 默认管理员密码: admin123
echo.

pause 
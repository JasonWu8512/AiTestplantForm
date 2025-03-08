@echo off
echo 正在启动前端项目...
cd /d D:\Work\Projects\AiTestplantForm\frontend
echo 当前目录: %CD%
echo 检查package.json文件...
if exist package.json (
    echo package.json文件存在，继续执行...
) else (
    echo package.json文件不存在，请确保您在正确的目录中！
    pause
    exit /b 1
)
echo 运行npm命令...
set NODE_PATH=C:\Program Files\nodejs
set PATH=%NODE_PATH%;%PATH%
"%NODE_PATH%\npm.cmd" run dev
if %ERRORLEVEL% neq 0 (
    echo 运行npm命令时出错，错误代码: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)
pause 
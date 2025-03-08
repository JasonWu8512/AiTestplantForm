@echo off
REM Docker操作主菜单
cd /d %~dp0
cd ..

:menu
cls
echo ===================================
echo        Docker操作主菜单
echo ===================================
echo.
echo  1. 启动Docker服务
echo  2. 停止Docker服务
echo  3. 查看Docker日志
echo  4. 重新构建Docker服务
echo  5. 进入容器Shell
echo  6. 备份数据库
echo  7. 恢复数据库
echo  8. 退出
echo.
echo ===================================
echo.

set /p choice=请输入选项(1-8): 

if "%choice%"=="1" (
    call %~dp0\start-docker.bat
    goto menu
) else if "%choice%"=="2" (
    call %~dp0\stop-docker.bat
    goto menu
) else if "%choice%"=="3" (
    call %~dp0\logs-docker.bat
    goto menu
) else if "%choice%"=="4" (
    call %~dp0\rebuild-docker.bat
    goto menu
) else if "%choice%"=="5" (
    call :enter_container
    goto menu
) else if "%choice%"=="6" (
    call :backup_database
    goto menu
) else if "%choice%"=="7" (
    call :restore_database
    goto menu
) else if "%choice%"=="8" (
    exit
) else (
    echo 无效的选项！
    timeout /t 2 >nul
    goto menu
)

:enter_container
cls
echo 请选择要进入的容器：
echo 1. 后端容器
echo 2. 前端容器
echo 3. 数据库容器
echo 4. Redis容器
echo 5. 返回主菜单
echo.

set /p container_choice=请输入选项(1-5): 

if "%container_choice%"=="1" (
    echo 正在进入后端容器...
    cmd /c "docker-compose exec backend bash"
) else if "%container_choice%"=="2" (
    echo 正在进入前端容器...
    cmd /c "docker-compose exec frontend sh"
) else if "%container_choice%"=="3" (
    echo 正在进入数据库容器...
    cmd /c "docker-compose exec db bash"
) else if "%container_choice%"=="4" (
    echo 正在进入Redis容器...
    cmd /c "docker-compose exec redis sh"
) else if "%container_choice%"=="5" (
    goto :eof
) else (
    echo 无效的选项！
    timeout /t 2 >nul
    goto enter_container
)
goto :eof

:backup_database
cls
echo 正在备份数据库...
set /p backup_file=请输入备份文件名(默认为backup.sql): 

if "%backup_file%"=="" (
    set backup_file=backup.sql
)

cmd /c "docker-compose exec -T db mysqldump -u root -p%MYSQL_ROOT_PASSWORD% %MYSQL_DATABASE% > %backup_file%"
echo 数据库已备份到 %backup_file%
pause
goto :eof

:restore_database
cls
echo 正在恢复数据库...
set /p backup_file=请输入备份文件名: 

if not exist "%backup_file%" (
    echo 备份文件不存在！
    pause
    goto :eof
)

cmd /c "type %backup_file% | docker-compose exec -T db mysql -u root -p%MYSQL_ROOT_PASSWORD% %MYSQL_DATABASE%"
echo 数据库已从 %backup_file% 恢复
pause
goto :eof 
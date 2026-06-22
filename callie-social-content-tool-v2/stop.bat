@echo off
chcp 65001 >nul
echo 正在停止服务...

:: 查找占用8000端口的进程并终止
set "found="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
    echo 已停止进程 PID: %%a
    set "found=1"
)

if defined found (
    echo 服务已停止
)

pause

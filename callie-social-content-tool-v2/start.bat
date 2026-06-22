@echo off
chcp 65001 >nul
title Callie 社媒内容生成工具

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [2/3] 创建虚拟环境（如需要）...
if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
    echo 依赖安装完成
) else (
    call venv\Scripts\activate.bat
)

echo [3/3] 启动服务...
set PORT=8000
python -m uvicorn app:app --host 127.0.0.1 --port %PORT% --reload

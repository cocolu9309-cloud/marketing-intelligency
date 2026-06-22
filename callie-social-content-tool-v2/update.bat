@echo off
chcp 65001 >nul
title 更新产品库

echo 正在更新 Callie 产品库...
if exist "venv" (
    call venv\Scripts\activate.bat
)
python scripts/crawl_products.py
echo 更新完成
pause

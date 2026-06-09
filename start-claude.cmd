@echo off
cls
echo ================================================
echo           启动 Claude + MiniMax 代理
echo ================================================
echo.

:: 设置环境变量
set ANTHROPIC_BASE_URL=http://127.0.0.1:8080
set ANTHROPIC_AUTH_TOKEN=dummy-token
set ANTHROPIC_MODEL=MiniMax-M2.7
set API_TIMEOUT_MS=3000000

echo 已设置环境变量:
echo - ANTHROPIC_BASE_URL: %ANTHROPIC_BASE_URL%
echo - ANTHROPIC_MODEL: %ANTHROPIC_MODEL%
echo.

:: 启动 Claude
echo 启动 Claude Code...
echo.
claude
echo.
echo ================================================
echo                   会话已结束
echo ================================================
pause
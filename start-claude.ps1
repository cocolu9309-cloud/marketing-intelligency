Write-Host "================================================"
Write-Host "           启动 Claude + MiniMax 代理"
Write-Host "================================================"
Write-Host ""

$env:ANTHROPIC_BASE_URL="http://127.0.0.1:8080"
$env:ANTHROPIC_AUTH_TOKEN="dummy-token"
$env:ANTHROPIC_MODEL="MiniMax-M2.7"
$env:API_TIMEOUT_MS="3000000"

Write-Host "已设置环境变量:"
Write-Host "- ANTHROPIC_BASE_URL: $($env:ANTHROPIC_BASE_URL)"
Write-Host "- ANTHROPIC_MODEL: $($env:ANTHROPIC_MODEL)"
Write-Host ""

Write-Host "启动 Claude Code..."
Write-Host ""

claude

Write-Host ""
Write-Host "================================================"
Write-Host "                   会话已结束"
Write-Host "================================================"
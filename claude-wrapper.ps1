param(
    [string]$prompt = ""
)

$proxyPath = "D:\工作\AI\claude-demo\claude-minimax-proxy.py"

# 检查代理是否在运行
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8080" -Method Get -TimeoutSec 1 -ErrorAction Stop
} catch {
    Write-Host "启动代理服务器..."
    Start-Process -FilePath "python" -ArgumentList "-u `"$proxyPath`"" -NoNewWindow -WorkingDirectory "D:\工作\AI\claude-demo"
    Start-Sleep -Seconds 2
}

# 设置环境变量并调用 Claude
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:8080"
$env:ANTHROPIC_AUTH_TOKEN = "dummy-token"
$env:ANTHROPIC_MODEL = "MiniMax-M2.7"

if ($prompt) {
    claude -p $prompt
} else {
    claude
}
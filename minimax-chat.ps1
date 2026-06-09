param(
    [string]$prompt = ""
)

$baseUrl = "https://api.minimaxi.com/anthropic/v1/messages"
$apiKey = "sk-cp-_vJU1xDTzXfpoEucqiaZb0P3HiFVJhKIY0k3xuc6yllTsqE6KUNRqBrllHhJDWnPe3KXe1-uPuRLFuWjE2BfL02A7DaC4BJTxEkK5kugHSGlNpmX6qOLYWo"

function Send-Message {
    param(
        [string]$content
    )
    
    $body = @"
{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"$content"}],"max_tokens":4096}
"@
    
    try {
        $response = Invoke-RestMethod -Uri $baseUrl -Method Post -Body $body -ContentType "application/json" -Headers @{
            "x-api-key" = $apiKey
        } -TimeoutSec 300
        
        $textContent = $response.content | Where-Object { $_.type -eq "text" } | Select-Object -ExpandProperty text -First 1
        return $textContent
    }
    catch {
        Write-Host "API Error: $_" -ForegroundColor Red
        return $null
    }
}

if ($prompt) {
    Send-Message -content $prompt
    exit
}

Write-Host "=== MiniMax-M2.7 Chat ===" -ForegroundColor Cyan
Write-Host "Type 'exit' or 'quit' to quit" -ForegroundColor Gray
Write-Host ""

while ($true) {
    Write-Host "You: " -ForegroundColor Green -NoNewline
    $inputText = Read-Host
    
    if ($inputText -eq "exit" -or $inputText -eq "quit") {
        Write-Host "Goodbye!" -ForegroundColor Cyan
        exit
    }
    
    if (-not $inputText.Trim()) {
        continue
    }
    
    Write-Host ""
    Write-Host "MiniMax: " -ForegroundColor Yellow -NoNewline
    
    $response = Send-Message -content $inputText
    
    if ($response) {
        Write-Host $response
    }
    else {
        Write-Host "Error getting response" -ForegroundColor Red
    }
    
    Write-Host ""
}
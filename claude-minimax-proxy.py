#!/usr/bin/env python3
import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import traceback

MINIMAX_API_URL = "https://api.minimaxi.com/anthropic/v1"
MINIMAX_API_KEY = "sk-cp-_vJU1xDTzXfpoEucqiaZb0P3HiFVJhKIY0k3xuc6yllTsqE6KUNRqBrllHhJDWnPe3KXe1-uPuRLFuWjE2BfL02A7DaC4BJTxEkK5kugHSGlNpmX6qOLYWo"
PROXY_PORT = 8080

class ClaudeMinimaxProxy(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _send_response(self, status_code, content, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        if content:
            self.wfile.write(content.encode("utf-8"))

    def _handle_health(self):
        response = json.dumps({"status": "ok"})
        self._send_response(200, response)

    def _handle_config(self):
        response = json.dumps({
            "models": [
                {"id": "MiniMax-M2.7", "name": "MiniMax-M2.7"},
                {"id": "claude-3-opus", "name": "Claude 3 Opus"},
                {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet"}
            ]
        })
        self._send_response(200, response)

    def _modify_request_body(self, body):
        if not body:
            return body
        try:
            body_json = json.loads(body)
            if "messages" in body_json:
                original_count = len(body_json["messages"])
                body_json["messages"] = [
                    msg for msg in body_json["messages"]
                    if msg.get("role") != "system"
                ]
                removed = original_count - len(body_json["messages"])
                if removed > 0:
                    print(f"[PROXY] 移除了 {removed} 个 system role 消息")
            return json.dumps(body_json)
        except:
            return body

    def _forward_to_minimax(self, path, method, body):
        try:
            url = f"{MINIMAX_API_URL}{path}"
            print(f"[PROXY] 转发到 MiniMax: {method} {url}")
            
            if body:
                body = self._modify_request_body(body)
            
            req = urllib.request.Request(url, data=body.encode("utf-8") if body else None, method=method)
            req.add_header("Content-Type", "application/json")
            req.add_header("x-api-key", MINIMAX_API_KEY)
            
            with urllib.request.urlopen(req, timeout=300) as response:
                return response.read().decode("utf-8")
        except Exception as e:
            print(f"[PROXY] 转发失败: {e}")
            return json.dumps({"error": str(e)})

    def do_GET(self):
        if self.path == "/health":
            self._handle_health()
        elif self.path == "/v1/models" or self.path == "/models":
            self._handle_config()
        else:
            response = self._forward_to_minimax(self.path, "GET", None)
            self._send_response(200, response)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else None
        
        print(f"[PROXY] POST 请求: {self.path} (长度: {content_length})")
        
        if self.path == "/v1/complete" or self.path == "/v1/chat/completions":
            response = json.dumps({
                "id": "test-id",
                "object": "chat.completion",
                "created": 12345,
                "model": "MiniMax-M2.7",
                "choices": [{"message": {"role": "assistant", "content": "Hello from proxy!"}, "finish_reason": "stop"}]
            })
            self._send_response(200, response)
        else:
            response = self._forward_to_minimax(self.path, "POST", body)
            self._send_response(200, response)

def run_proxy():
    server_address = ("127.0.0.1", PROXY_PORT)
    httpd = HTTPServer(server_address, ClaudeMinimaxProxy)
    
    print("=" * 50)
    print("    Claude MiniMax Proxy 已启动")
    print("=" * 50)
    print(f"  本地端口: http://127.0.0.1:{PROXY_PORT}")
    print(f"  目标地址: {MINIMAX_API_URL}")
    print("=" * 50)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n代理服务器已停止")
        httpd.server_close()

if __name__ == "__main__":
    run_proxy()
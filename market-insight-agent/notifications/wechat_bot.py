import httpx
import json
from datetime import datetime
from typing import List

class WeChatBot:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_text(self, content: str):
        """发送文本消息"""
        data = {
            "msgtype": "text",
            "text": {"content": content}
        }
        self._send(data)

    def send_markdown(self, content: str):
        """发送 Markdown 消息"""
        data = {
            "msgtype": "markdown",
            "markdown": {"content": content}
        }
        self._send(data)

    def _send(self, data: dict):
        """发送请求"""
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(self.webhook_url, json=data)
                response.raise_for_status()
        except Exception as e:
            print(f"Failed to send WeChat notification: {e}")

    def send_daily_report(self, opportunities: List[dict], briefs: List[dict]):
        """发送每日简报"""
        content = f"""【市场洞察日报】{datetime.now().strftime('%Y-%m-%d')}

🔥 高价值机会
"""
        for opp in opportunities[:3]:
            content += f"{opp['title']}\n"

        content += f"""
📊 Brief 状态
- 待接收: {len([b for b in briefs if b['status'] == '待接收'])}
- 执行中: {len([b for b in briefs if b['status'] in ['已测试', '已放量']])}
"""
        self.send_markdown(content)

# 使用示例
# bot = WeChatBot("YOUR_WEBHOOK_URL")
# bot.send_text("测试消息")
import argparse
import json
import logging
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI()

# HTML 内容（内嵌）
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>炼金师助手 - 知识变现专家</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .content { padding: 40px; }
        .feature-box {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .feature-box h3 { color: #667eea; margin-bottom: 10px; }
        .chat-container {
            border: 2px solid #e9ecef;
            border-radius: 10px;
            margin-top: 30px;
        }
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
        }
        .message {
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
        }
        .assistant-message {
            background: #f8f9fa;
            color: #333;
        }
        .chat-input {
            display: flex;
            padding: 20px;
            border-top: 2px solid #e9ecef;
        }
        .chat-input input {
            flex: 1;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
        }
        .chat-input button {
            margin-left: 10px;
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        .pricing {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        .pricing-card {
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .pricing-card h4 { color: #667eea; font-size: 1.5em; }
        .pricing-card .price { font-size: 2em; color: #764ba2; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧙‍♂️ 炼金师助手</h1>
            <p>帮助你把隐性经验转化为可出售的知识产品</p>
        </div>
        
        <div class="content">
            <div class="feature-box">
                <h3>✨ 核心功能</h3>
                <p>📋 知识资产盘点 → 💡 选题价值评估 → 🤖 Agent 提示词生成 → 📦 完整产出包</p>
            </div>
            
            <div class="chat-container">
                <div class="chat-messages" id="chatMessages">
                    <div class="message assistant-message">
                        👋 你好！我是炼金师助手。<br><br>
                        我可以帮助你：<br>
                        • 盘点你的知识资产<br>
                        • 评估选题的市场价值<br>
                        • 生成 AI Agent 提示词<br>
                        • 创建完整的知识产品<br><br>
                        <strong>请告诉我你的专业领域或最擅长的技能！</strong>
                    </div>
                </div>
                <div class="chat-input">
                    <input type="text" id="userInput" placeholder="输入你的问题..." onkeypress="if(event.key==='Enter')sendMessage()">
                    <button onclick="sendMessage()">发送</button>
                </div>
            </div>
            
            <div class="pricing">
                <div class="pricing-card">
                    <h4>体验版</h4>
                    <div class="price">¥9.9</div>
                    <p>5次对话</p>
                </div>
                <div class="pricing-card">
                    <h4>标准版</h4>
                    <div class="price">¥29.9</div>
                    <p>20次对话</p>
                </div>
                <div class="pricing-card">
                    <h4>年度会员</h4>
                    <div class="price">¥99</div>
                    <p>100次对话</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;
            
            const chatMessages = document.getElementById('chatMessages');
            
            // 添加用户消息
            chatMessages.innerHTML += `<div class="message user-message">${message}</div>`;
            input.value = '';
            
            // 发送到后端
            try {
                const response = await fetch('/alchemist/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                
                // 添加助手回复
                chatMessages.innerHTML += `<div class="message assistant-message">${data.message}</div>`;
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (error) {
                chatMessages.innerHTML += `<div class="message assistant-message">抱歉，网络错误，请重试。</div>`;
            }
        }
    </script>
</body>
</html>
"""

# ===== 路由定义 =====

@app.get("/")
async def root():
    """根路径"""
    return HTMLResponse(content=HTML_CONTENT, status_code=200)


@app.get("/alchemist")
async def alchemist_page():
    """炼金师助手页面"""
    return HTMLResponse(content=HTML_CONTENT, status_code=200)


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "Service is running"}


@app.post("/alchemist/chat")
async def alchemist_chat(request: Request):
    """对话接口"""
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if not message:
            return JSONResponse({"message": "请输入内容"}, status_code=400)
        
        # 简化回复
        response = f"""
收到你的消息："{message}"

---

🎉 **这是演示版本**，功能已就绪！

系统可以帮你：
1. 📋 盘点知识资产
2. 💡 评估选题价值
3. 🤖 生成 Agent 提示词
4. 📦 输出完整产品包

**完整版正在升级中，敬请期待！**

如需完整功能，请私信获取激活码～
        """
        
        return {"message": response}
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse({"message": f"错误：{str(e)}"}, status_code=500)


# ===== 启动 =====

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, default=5000)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    uvicorn.run("main:app", host="0.0.0.0", port=args.p, reload=False)

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

# HTML 内容
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>炼金师助手</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; display: flex; align-items: center; justify-content: center; }
        .container { background: white; border-radius: 20px; padding: 40px; max-width: 800px; text-align: center; }
        h1 { color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧙‍♂️ 炼金师助手</h1>
        <p>帮助你把隐性经验转化为可出售的知识产品</p>
    </div>
</body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(content=HTML_CONTENT, status_code=200)

@app.get("/alchemist")
async def alchemist():
    return HTMLResponse(content=HTML_CONTENT, status_code=200)

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Service is running"}

@app.post("/alchemist/chat")
async def chat(request: Request):
    data = await request.json()
    return {"message": f"收到：{data.get('message', '')}"}

if __name__ == "__main__":
    args = argparse.ArgumentParser().parse_args()
    uvicorn.run("server:app", host="0.0.0.0", port=8080)

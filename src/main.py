import argparse
import asyncio
import json
import os
import logging
from typing import Any, Dict
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse

# 基础日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI()

# 超时配置
TIMEOUT_SECONDS = 900


def _get_html_path():
    """获取HTML文件的绝对路径"""
    possible_paths = [
        os.path.join(os.getcwd(), "assets/pages/index.html"),
        "/app/assets/pages/index.html",
        "/workspace/projects/assets/pages/index.html",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Found HTML file at: {path}")
            return path
    
    logger.error(f"HTML file not found")
    return None


# ===== 路由定义 =====

@app.get("/", response_class=HTMLResponse)
async def root():
    """决策炼金师首页"""
    html_path = _get_html_path()
    if not html_path:
        return HTMLResponse(content="<h1>页面未找到 - HTML文件不存在</h1>", status_code=404)
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading HTML file: {e}")
        return HTMLResponse(content=f"<h1>页面加载错误: {str(e)}</h1>", status_code=500)


@app.get("/alchemist", response_class=HTMLResponse)
async def alchemist_page():
    """决策炼金师页面"""
    html_path = _get_html_path()
    if not html_path:
        return HTMLResponse(content="<h1>页面未找到 - HTML文件不存在</h1>", status_code=404)
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except Exception as e:
        logger.error(f"Error reading HTML file: {e}")
        return HTMLResponse(content=f"<h1>页面加载错误: {str(e)}</h1>", status_code=500)


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "message": "Service is running",
    }


@app.get("/debug")
async def debug_info():
    """调试端点"""
    html_path = _get_html_path()
    
    return {
        "cwd": os.getcwd(),
        "html_path_found": html_path,
        "assets_exists": os.path.exists("assets/pages/index.html"),
        "app_assets_exists": os.path.exists("/app/assets/pages/index.html"),
        "current_file": __file__,
    }


@app.post("/alchemist/chat")
async def alchemist_chat(request: Request):
    """决策炼金师对话接口"""
    try:
        payload = await request.json()
        message = payload.get("message", "")
        
        if not message:
            raise HTTPException(status_code=400, detail="消息不能为空")
        
        # 简化版：直接返回固定响应
        return {
            "status": "success",
            "message": f"收到您的消息：{message}\n\n系统正在初始化中，请稍后再试。",
            "session_id": "default",
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logger.error(f"Error in alchemist_chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== 启动函数 =====

def parse_args():
    parser = argparse.ArgumentParser(description="Start FastAPI server")
    parser.add_argument("-p", type=int, default=5000, help="HTTP server port")
    return parser.parse_args()


def start_http_server(port):
    logger.info(f"Start HTTP Server on port: {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False, workers=1)


if __name__ == "__main__":
    args = parse_args()
    start_http_server(args.p)
# Force latest deploy

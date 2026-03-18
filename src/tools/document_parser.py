"""
文档解析工具 - 用于解析用户上传的文档
"""
import os
import json
from typing import Optional, Dict, Any
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk.fetch import FetchClient
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def parse_document(
    file_url: str,
    runtime: ToolRuntime = None
) -> str:
    """
    解析文档内容，支持PDF、Word、PPT等格式
    
    Args:
        file_url: 文档的URL地址
        
    Returns:
        文档的文本内容
    """
    ctx = runtime.context if runtime else new_context(method="parse_document")
    
    try:
        client = FetchClient(ctx=ctx)
        response = client.fetch(url=file_url)
        
        if response.status_code != 0:
            return f"文档解析失败: {response.status_message}"
        
        # 提取文本内容
        text_parts = []
        for item in response.content:
            if item.type == "text":
                text_parts.append(item.text)
        
        full_text = "\n".join(text_parts)
        
        # 返回文档信息
        result = {
            "title": response.title,
            "file_type": response.filetype,
            "content": full_text[:5000],  # 限制长度
            "content_length": len(full_text)
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return f"解析文档时出错: {str(e)}"


def parse_document_direct(file_url: str) -> Dict[str, Any]:
    """
    直接解析文档（不作为工具使用）
    
    Args:
        file_url: 文档URL
        
    Returns:
        解析结果
    """
    ctx = new_context(method="parse_document_direct")
    
    try:
        client = FetchClient(ctx=ctx)
        response = client.fetch(url=file_url)
        
        if response.status_code != 0:
            return {
                "success": False,
                "error": response.status_message
            }
        
        # 提取文本内容
        text_parts = []
        for item in response.content:
            if item.type == "text":
                text_parts.append(item.text)
        
        return {
            "success": True,
            "title": response.title,
            "file_type": response.filetype,
            "content": "\n".join(text_parts),
            "url": response.url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

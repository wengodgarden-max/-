"""
决策炼金师 Agent
帮助用户将专业判断能力提炼成AI工具
"""
import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver
from tools.document_parser import parse_document  # 导入文档解析工具
from tools.web_search_tool import web_search, get_industry_benchmark  # 导入搜索工具
from tools.payment_tool import verify_code, check_permission, get_pricing_info  # 导入付费验证工具

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40


def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore


class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


def build_agent(ctx=None):
    """
    构建决策炼金师 Agent
    
    Args:
        ctx: 运行时上下文，用于请求追踪
        
    Returns:
        Agent实例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    # 从配置中读取工具列表
    tools_config = cfg.get("tools", [])
    tools = []
    
    # 根据配置添加工具
    if "parse_document" in tools_config:
        tools.append(parse_document)
    
    # 添加搜索工具
    if "web_search" in tools_config:
        tools.append(web_search)
    
    if "get_industry_benchmark" in tools_config:
        tools.append(get_industry_benchmark)
    
    # 添加付费验证工具
    if "verify_code" in tools_config:
        tools.append(verify_code)
    
    if "check_permission" in tools_config:
        tools.append(check_permission)
    
    if "get_pricing_info" in tools_config:
        tools.append(get_pricing_info)

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )

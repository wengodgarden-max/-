"""联网搜索工具 - 用于补充专家知识缺失"""
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from typing import Optional


@tool
def web_search(query: str, runtime: ToolRuntime = None) -> str:
    """
    联网搜索工具，用于获取实时信息和补充知识。
    
    适用场景：
    - 用户提到不熟悉的行业术语或概念
    - 需要了解某个领域的最新趋势或标准
    - 需要查找行业基准数据或案例
    - 用户知识缺失，需要补充背景信息
    
    Args:
        query: 搜索关键词，应该简洁明确
        
    Returns:
        搜索结果的摘要信息
    """
    ctx = runtime.context if runtime else new_context(method="web_search")
    
    try:
        client = SearchClient(ctx=ctx)
        
        # 执行搜索，获取带AI摘要的结果
        response = client.web_search_with_summary(
            query=query,
            count=5  # 返回5条结果
        )
        
        if not response.web_items:
            return f"未找到关于'{query}'的相关信息。"
        
        # 构建结果文本
        result_parts = []
        
        # 添加AI摘要
        if response.summary:
            result_parts.append(f"📋 **知识摘要**：\n{response.summary}\n")
        
        # 添加搜索结果
        result_parts.append("📚 **参考来源**：")
        for i, item in enumerate(response.web_items[:3], 1):
            result_parts.append(f"\n{i}. **{item.title}**")
            if item.snippet:
                # 截取前200字符
                snippet = item.snippet[:200] + "..." if len(item.snippet) > 200 else item.snippet
                result_parts.append(f"   {snippet}")
            result_parts.append(f"   来源：{item.site_name}")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        return f"搜索失败：{str(e)}。请尝试重新描述您的需求。"


@tool
def get_industry_benchmark(industry: str, metric: str, runtime: ToolRuntime = None) -> str:
    """
    获取行业基准数据工具。
    
    用于查找特定行业的标准指标数据，帮助用户了解行业平均水平，
    以便设置合理的决策标准。
    
    Args:
        industry: 行业名称，如"电商"、"SaaS"、"金融"等
        metric: 指标名称，如"转化率"、"留存率"、"ROI"等
        
    Returns:
        行业基准数据和说明
    """
    ctx = runtime.context if runtime else new_context(method="get_industry_benchmark")
    
    try:
        client = SearchClient(ctx=ctx)
        
        # 构建搜索查询
        query = f"{industry}行业 {metric} 平均值 基准数据 2024"
        
        response = client.web_search_with_summary(
            query=query,
            count=5
        )
        
        if not response.web_items:
            return f"未找到{industry}行业的{metric}基准数据，建议您根据自身经验设定初始标准，后续根据实际数据调整。"
        
        # 构建结果
        result_parts = [f"📊 **{industry}行业 {metric} 基准参考**：\n"]
        
        if response.summary:
            result_parts.append(f"{response.summary}\n")
        
        result_parts.append("**详细数据来源**：")
        for i, item in enumerate(response.web_items[:3], 1):
            result_parts.append(f"\n{i}. {item.title}")
            if item.snippet:
                result_parts.append(f"   {item.snippet[:150]}...")
        
        result_parts.append(f"\n\n💡 **建议**：以上数据仅供参考，您可以根据自己业务的具体情况调整标准。")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        return f"获取行业数据失败：{str(e)}。建议您根据经验设定合理的标准范围。"

"""
付费验证工具 - 用于验证用户是否有使用权限
"""
import os
import json
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context

# 预设验证码（实际生产环境应该用数据库）
# 格式: {验证码: {"usage_limit": 5, "expires_at": "2025-12-31"}}
VERIFICATION_CODES = {
    # 体验版 ¥9.9 / 5次（内测激活码，可多次使用）
    "ALCH-TRIAL-2025": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-001": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-002": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-003": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-004": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-005": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-006": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-007": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-008": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-009": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    "GOLD-010": {"usage_limit": 5, "plan": "体验版", "price": 9.9},
    
    # 标准版 ¥29.9 / 20次
    "SILVER-001": {"usage_limit": 20, "plan": "标准版", "price": 29.9},
    "SILVER-002": {"usage_limit": 20, "plan": "标准版", "price": 29.9},
    "SILVER-003": {"usage_limit": 20, "plan": "标准版", "price": 29.9},
    "SILVER-004": {"usage_limit": 20, "plan": "标准版", "price": 29.9},
    "SILVER-005": {"usage_limit": 20, "plan": "标准版", "price": 29.9},
    
    # 年度会员 ¥99 / 100次
    "DIAMOND-001": {"usage_limit": 100, "plan": "年度会员", "price": 99},
    "DIAMOND-002": {"usage_limit": 100, "plan": "年度会员", "price": 99},
    "DIAMOND-003": {"usage_limit": 100, "plan": "年度会员", "price": 99},
}

# 用户权限存储路径
USER_AUTH_FILE = "assets/data/user_auth.json"


def _load_user_auth() -> Dict[str, Any]:
    """加载用户权限数据"""
    try:
        if os.path.exists(USER_AUTH_FILE):
            with open(USER_AUTH_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_user_auth(data: Dict[str, Any]) -> None:
    """保存用户权限数据"""
    os.makedirs(os.path.dirname(USER_AUTH_FILE), exist_ok=True)
    with open(USER_AUTH_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_user_id(ctx) -> str:
    """获取用户唯一标识"""
    # 尝试从上下文获取用户ID
    if hasattr(ctx, 'user_id') and ctx.user_id:
        return ctx.user_id
    
    # 使用默认ID
    return "default_user"


def check_user_permission(ctx=None) -> Dict[str, Any]:
    """
    检查用户是否有使用权限
    
    Returns:
        {
            "has_permission": bool,
            "remaining_uses": int,
            "plan": str,
            "message": str
        }
    """
    user_id = _get_user_id(ctx) if ctx else "default_user"
    auth_data = _load_user_auth()
    
    if user_id not in auth_data:
        return {
            "has_permission": False,
            "remaining_uses": 0,
            "plan": None,
            "message": "您还未激活，请输入验证码解锁使用"
        }
    
    user_info = auth_data[user_id]
    remaining = user_info.get("usage_limit", 0) - user_info.get("usage_count", 0)
    
    return {
        "has_permission": remaining > 0,
        "remaining_uses": remaining,
        "plan": user_info.get("plan", "未知"),
        "message": f"您还有 {remaining} 次使用机会" if remaining > 0 else "使用次数已用完，请续费"
    }


def consume_usage(ctx=None) -> bool:
    """
    消耗一次使用机会
    
    Returns:
        是否成功消耗
    """
    user_id = _get_user_id(ctx) if ctx else "default_user"
    auth_data = _load_user_auth()
    
    if user_id not in auth_data:
        return False
    
    user_info = auth_data[user_id]
    remaining = user_info.get("usage_limit", 0) - user_info.get("usage_count", 0)
    
    if remaining <= 0:
        return False
    
    user_info["usage_count"] = user_info.get("usage_count", 0) + 1
    user_info["last_used"] = datetime.now().isoformat()
    _save_user_auth(auth_data)
    
    return True


@tool
def verify_code(code: str, runtime: ToolRuntime = None) -> str:
    """
    验证激活码，解锁使用权限
    
    Args:
        code: 激活码（格式如 ALCH-TRIAL-2025）
        
    Returns:
        验证结果信息
    """
    ctx = runtime.context if runtime else new_context(method="verify_code")
    user_id = _get_user_id(ctx)
    
    # 检查验证码是否有效
    if code not in VERIFICATION_CODES:
        return json.dumps({
            "success": False,
            "message": "❌ 验证码无效，请检查后重试"
        }, ensure_ascii=False)
    
    code_info = VERIFICATION_CODES[code]
    auth_data = _load_user_auth()
    
    # 检查用户是否已激活
    if user_id in auth_data:
        old_plan = auth_data[user_id].get("plan", "未知")
        old_remaining = auth_data[user_id].get("usage_limit", 0) - auth_data[user_id].get("usage_count", 0)
        
        # 如果已有权限，叠加次数
        auth_data[user_id]["usage_limit"] += code_info["usage_limit"]
        auth_data[user_id]["plan"] = code_info["plan"]
        auth_data[user_id]["activated_at"] = datetime.now().isoformat()
        _save_user_auth(auth_data)
        
        return json.dumps({
            "success": True,
            "message": f"✅ 验证成功！已为您增加 {code_info['usage_limit']} 次使用机会",
            "plan": code_info["plan"],
            "total_uses": auth_data[user_id]["usage_limit"],
            "remaining_uses": auth_data[user_id]["usage_limit"] - auth_data[user_id]["usage_count"]
        }, ensure_ascii=False)
    
    # 新用户激活
    auth_data[user_id] = {
        "code": code,
        "plan": code_info["plan"],
        "usage_limit": code_info["usage_limit"],
        "usage_count": 0,
        "activated_at": datetime.now().isoformat(),
        "price": code_info["price"]
    }
    _save_user_auth(auth_data)
    
    return json.dumps({
        "success": True,
        "message": f"✅ 激活成功！您已开通「{code_info['plan']}」",
        "plan": code_info["plan"],
        "total_uses": code_info["usage_limit"],
        "remaining_uses": code_info["usage_limit"]
    }, ensure_ascii=False)


@tool
def check_permission(runtime: ToolRuntime = None) -> str:
    """
    检查当前用户的使用权限
    
    Returns:
        用户权限状态
    """
    ctx = runtime.context if runtime else new_context(method="check_permission")
    result = check_user_permission(ctx)
    
    return json.dumps(result, ensure_ascii=False)


@tool
def get_pricing_info(runtime: ToolRuntime = None) -> str:
    """
    获取产品定价信息
    
    Returns:
        定价套餐详情
    """
    pricing = {
        "plans": [
            {
                "name": "体验版",
                "price": 9.9,
                "uses": 5,
                "unit_price": 1.98,
                "best_for": "想先体验效果的用户",
                "features": ["5次完整炼金流程", "产出Agent或课程", "7天有效期"]
            },
            {
                "name": "标准版",
                "price": 29.9,
                "uses": 20,
                "unit_price": 1.50,
                "best_for": "想批量产出知识产品的用户",
                "features": ["20次完整炼金流程", "产出Agent或课程", "30天有效期", "优先客服支持"]
            },
            {
                "name": "年度会员",
                "price": 99,
                "uses": 100,
                "unit_price": 0.99,
                "best_for": "长期经营知识产品的用户",
                "features": ["100次完整炼金流程", "产出Agent或课程", "365天有效期", "专属客服群", "新功能优先体验"]
            }
        ],
        "payment_methods": [
            "小红书私信付款",
            "微信扫码支付"
        ],
        "contact": "付款后联系客服获取激活码"
    }
    
    return json.dumps(pricing, ensure_ascii=False)

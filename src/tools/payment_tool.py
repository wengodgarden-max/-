"""
付费验证工具 - 用于验证用户是否有使用权限
支持：免费体验轮次控制、激活码验证、重做次数限制
"""
import os
import json
from typing import Optional, Dict, Any
from datetime import datetime
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context

# 预设验证码（实际生产环境应该用数据库）
VERIFICATION_CODES = {
    # 体验版 ¥9.9 / 5次
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

# 免费试用对话轮数（让用户感受到价值，但需要付费才能完整产出）
FREE_TRIAL_ROUNDS = 5

# 每次使用允许的重做次数
MAX_REDO_COUNT = 1

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
    if ctx and hasattr(ctx, 'user_id') and ctx.user_id:
        return ctx.user_id
    return "default_user"


def check_user_permission(ctx=None) -> Dict[str, Any]:
    """
    检查用户是否有使用权限
    
    Returns:
        {
            "has_permission": bool,
            "remaining_uses": int,
            "remaining_rounds": int,  # 免费对话轮数
            "plan": str,
            "message": str,
            "is_free_trial": bool,
            "should_prompt_payment": bool  # 是否应该提示付费
        }
    """
    user_id = _get_user_id(ctx) if ctx else "default_user"
    auth_data = _load_user_auth()
    
    # 新用户：有5轮免费对话
    if user_id not in auth_data:
        return {
            "has_permission": True,
            "remaining_uses": 0,
            "remaining_rounds": FREE_TRIAL_ROUNDS,
            "current_round": 0,
            "plan": "免费体验",
            "message": f"🎉 新用户福利：可免费体验 {FREE_TRIAL_ROUNDS} 轮对话，满意再付费！",
            "is_free_trial": True,
            "should_prompt_payment": False,
            "can_redo": False
        }
    
    user_info = auth_data[user_id]
    
    # 检查免费对话轮数
    current_round = user_info.get("free_rounds_used", 0)
    remaining_free_rounds = max(0, FREE_TRIAL_ROUNDS - current_round)
    
    # 还有免费轮数
    if remaining_free_rounds > 0 and not user_info.get("activated", False):
        should_prompt = remaining_free_rounds <= 2  # 剩余2轮时开始提示
        
        return {
            "has_permission": True,
            "remaining_uses": 0,
            "remaining_rounds": remaining_free_rounds,
            "current_round": current_round,
            "plan": "免费体验",
            "message": f"免费体验还剩 {remaining_free_rounds} 轮对话",
            "is_free_trial": True,
            "should_prompt_payment": should_prompt,
            "can_redo": False
        }
    
    # 已激活用户
    if user_info.get("activated", False):
        remaining = user_info.get("usage_limit", 0) - user_info.get("usage_count", 0)
        redo_used = user_info.get("redo_count", 0)
        can_redo = redo_used < MAX_REDO_COUNT
        
        return {
            "has_permission": remaining > 0,
            "remaining_uses": remaining,
            "remaining_rounds": 0,
            "current_round": current_round,
            "plan": user_info.get("plan", "未知"),
            "message": f"您还有 {remaining} 次使用机会" if remaining > 0 else "使用次数已用完，请续费",
            "is_free_trial": False,
            "should_prompt_payment": remaining <= 0,
            "can_redo": can_redo
        }
    
    # 免费轮数用完，需要激活
    return {
        "has_permission": False,
        "remaining_uses": 0,
        "remaining_rounds": 0,
        "current_round": current_round,
        "plan": "免费体验",
        "message": "⚠️ 免费体验已用完\n\n解锁完整产出物需要激活码\n💡 激活后可获得：\n• 完整的AI Agent提示词\n• 测试用例\n• 上架指南\n• 推广文案\n• 定价建议\n\n💰 套餐：体验版¥9.9/标准版¥29.9/年度会员¥99",
        "is_free_trial": False,
        "should_prompt_payment": True,
        "can_redo": False
    }


def consume_free_round(ctx=None) -> bool:
    """消耗一轮免费对话"""
    user_id = _get_user_id(ctx) if ctx else "default_user"
    auth_data = _load_user_auth()
    
    if user_id not in auth_data:
        auth_data[user_id] = {
            "free_rounds_used": 1,
            "activated": False,
            "created_at": datetime.now().isoformat(),
            "redo_count": 0
        }
        _save_user_auth(auth_data)
        return True
    
    user_info = auth_data[user_id]
    user_info["free_rounds_used"] = user_info.get("free_rounds_used", 0) + 1
    user_info["last_used"] = datetime.now().isoformat()
    _save_user_auth(auth_data)
    
    return True


def consume_usage(ctx=None) -> bool:
    """消耗一次付费使用机会"""
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
    # 重置重做次数
    user_info["redo_count"] = 0
    _save_user_auth(auth_data)
    
    return True


def record_redo(ctx=None) -> bool:
    """记录一次重做"""
    user_id = _get_user_id(ctx) if ctx else "default_user"
    auth_data = _load_user_auth()
    
    if user_id not in auth_data:
        return False
    
    user_info = auth_data[user_id]
    redo_count = user_info.get("redo_count", 0)
    
    if redo_count >= MAX_REDO_COUNT:
        return False
    
    user_info["redo_count"] = redo_count + 1
    user_info["last_redo"] = datetime.now().isoformat()
    _save_user_auth(auth_data)
    
    return True


@tool
def verify_code(code: str, runtime: ToolRuntime = None) -> str:
    """
    验证激活码，解锁使用权限
    
    Args:
        code: 激活码（格式如 GOLD-001）
        
    Returns:
        验证结果信息
    """
    ctx = runtime.context if runtime else new_context(method="verify_code")
    user_id = _get_user_id(ctx)
    
    # 检查验证码是否有效
    if code not in VERIFICATION_CODES:
        return json.dumps({
            "success": False,
            "message": "❌ 激活码无效\n\n💡 购买激活码请联系客服\n• 体验版 ¥9.9 / 5次\n• 标准版 ¥29.9 / 20次\n• 年度会员 ¥99 / 100次"
        }, ensure_ascii=False)
    
    code_info = VERIFICATION_CODES[code]
    auth_data = _load_user_auth()
    
    # 新用户激活
    if user_id not in auth_data:
        auth_data[user_id] = {
            "code": code,
            "plan": code_info["plan"],
            "usage_limit": code_info["usage_limit"],
            "usage_count": 0,
            "activated": True,
            "free_rounds_used": FREE_TRIAL_ROUNDS,
            "activated_at": datetime.now().isoformat(),
            "price": code_info["price"],
            "redo_count": 0
        }
        _save_user_auth(auth_data)
        
        return json.dumps({
            "success": True,
            "message": f"✅ 激活成功！您已开通「{code_info['plan']}」，可使用 {code_info['usage_limit']} 次！\n\n现在可以继续您的炼金之旅了！",
            "plan": code_info["plan"],
            "total_uses": code_info["usage_limit"],
            "remaining_uses": code_info["usage_limit"]
        }, ensure_ascii=False)
    
    # 老用户：叠加次数
    user_info = auth_data[user_id]
    user_info["usage_limit"] = user_info.get("usage_limit", 0) + code_info["usage_limit"]
    user_info["plan"] = code_info["plan"]
    user_info["activated"] = True
    user_info["activated_at"] = datetime.now().isoformat()
    user_info["redo_count"] = 0
    _save_user_auth(auth_data)
    
    total_remaining = user_info["usage_limit"] - user_info.get("usage_count", 0)
    
    return json.dumps({
        "success": True,
        "message": f"✅ 激活成功！已增加 {code_info['usage_limit']} 次使用机会，共 {total_remaining} 次！",
        "plan": code_info["plan"],
        "total_uses": user_info["usage_limit"],
        "remaining_uses": total_remaining
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
        "message": "💰 激活码套餐",
        "plans": [
            {"name": "体验版", "price": 9.9, "uses": 5, "recommend": "适合想先试试的用户"},
            {"name": "标准版", "price": 29.9, "uses": 20, "recommend": "性价比最高"},
            {"name": "年度会员", "price": 99, "uses": 100, "recommend": "适合长期使用"}
        ],
        "note": "联系客服购买激活码，输入激活码即可使用",
        "free_trial": f"🎁 新用户可免费体验 {FREE_TRIAL_ROUNDS} 轮对话，满意再付费",
        "guarantee": "✨ 满意度保障：不满意可免费重做1次"
    }
    
    return json.dumps(pricing, ensure_ascii=False)


@tool
def request_redo(reason: str, runtime: ToolRuntime = None) -> str:
    """
    申请重新产出（不满意时使用）
    
    Args:
        reason: 具体哪里不满意，需要怎么调整
        
    Returns:
        重做申请结果
    """
    ctx = runtime.context if runtime else new_context(method="request_redo")
    user_id = _get_user_id(ctx)
    
    # 检查权限
    permission = check_user_permission(ctx)
    
    if not permission.get("can_redo", False):
        return json.dumps({
            "success": False,
            "message": "⚠️ 抱歉，重做次数已用完\n\n每次使用仅限重做1次，建议您：\n1. 详细说明需要调整的地方\n2. 或者激活新的使用次数"
        }, ensure_ascii=False)
    
    # 记录重做
    if record_redo(ctx):
        return json.dumps({
            "success": True,
            "message": f"✅ 已为您申请重做\n\n您的反馈：{reason}\n\n我会根据您的反馈重新产出，请稍等...",
            "redo_remaining": MAX_REDO_COUNT - 1
        }, ensure_ascii=False)
    
    return json.dumps({
        "success": False,
        "message": "重做申请失败，请稍后重试"
    }, ensure_ascii=False)

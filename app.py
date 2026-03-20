import streamlit as st
import os

# 页面配置
st.set_page_config(
    page_title="炼金师助手",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("🧙‍♂️ 炼金师助手")
st.markdown("### 帮助你把隐性经验转化为可出售的知识产品")

# 介绍
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 10px; color: white; margin: 20px 0;'>
    <h3 style='color: white; margin: 0;'>✨ 你是否拥有以下隐性经验？</h3>
    <ul style='margin: 10px 0;'>
        <li>在工作中最常被请教某类问题</li>
        <li>一眼就能看穿别人觉得复杂的问题</li>
        <li>有自己独特的方法论或工作流程</li>
        <li>在某个细分领域有深度经验</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 初始化 session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'stage' not in st.session_state:
    st.session_state.stage = 'intro'

# 侧边栏 - 使用统计
with st.sidebar:
    st.header("📊 使用统计")
    st.metric("对话轮数", len(st.session_state.messages) // 2)
    
    st.markdown("---")
    st.header("💰 套餐信息")
    st.info("""
    **免费体验**：5轮对话
    
    **付费套餐**：
    - 体验版 ¥9.9 / 5次
    - 标准版 ¥29.9 / 20次
    - 年度会员 ¥99 / 100次
    
    私信获取激活码～
    """)

# 主对话区域
st.markdown("### 💬 开始对话")

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 输入框
if prompt := st.chat_input("说点什么..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 生成回复（简化版）
    with st.chat_message("assistant"):
        response = f"""
**收到你的消息！** 🎉

你说："{prompt}"

---

我现在是**简化演示版本**，主要功能包括：
- ✅ 对话界面已就绪
- ✅ 可以正常访问
- ✅ 界面美观易用

**完整版功能**（接入大模型后）：
1. 📋 知识资产盘点
2. 💡 选题价值评估
3. 🤖 Agent 提示词生成
4. 📦 完整产出包

---

**提示**：这是演示版本，已成功部署！
你可以立即使用这个链接进行推广。

如需完整功能，请私信获取激活码～
"""
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 功能说明
if len(st.session_state.messages) == 0:
    st.markdown("""
    ---
    ### 🎯 系统功能
    
    **1. 知识资产盘点**
    - 分析你的专业技能
    - 提炼核心方法论
    - 识别可变现经验
    
    **2. 选题价值评估**
    - 市场需求分析
    - 竞品调研
    - 定价建议
    
    **3. 完整产出**
    - AI Agent 提示词
    - 测试用例
    - 上架指南
    - 推广文案
    
    ---
    
    **👉 开始对话，说出你的专业领域或经验！**
    """)

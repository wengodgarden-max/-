# 决策炼金师 - 快速使用指南

## 🎯 如何访问网页应用

### 方法1：直接访问首页
打开浏览器，访问：`http://localhost:5000/`

### 方法2：访问专用页面
打开浏览器，访问：`http://localhost:5000/alchemist`

## 🔌 如何通过API调用

### 基础对话接口

```bash
curl -X POST "http://localhost:5000/alchemist/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我想创建一个决策工具，帮我判断产品功能是否值得开发",
    "session_id": "user_123"
  }'
```

### 响应示例

```json
{
  "status": "success",
  "message": "太棒了！你想创建一个决策工具来判断产品功能是否值得开发，这是一个非常有价值的场景...",
  "session_id": "user_123",
  "run_id": "run_abc123"
}
```

## 📝 完整流程示例

### 步骤1：访问网页
打开 `http://localhost:5000/`

### 步骤2：选择模式
点击"快速模式"开始

### 步骤3：填写关卡1
回答三个问题：
- 最擅长的问题：评估产品功能是否值得开发
- 目标用户：产品经理、创业者
- 失误后果：浪费开发资源，错失市场机会

### 步骤4：填写关卡2
描述决策过程：
- 第一步：看用户需求强度和市场空间
- 关键标准：用户调研数据、竞品分析、技术可行性
- 转折信号：竞品突然涌入、技术难度超预期
- 常见误区：只看用户反馈，忽略技术成本

### 步骤5：填写规则
添加决策规则：
- 如果 用户需求评分>8 且 技术可行性评分>7
- 那么 属于"优先开发"
- 建议：立即立项，组建团队
- 风险：注意技术风险，预留缓冲时间

### 步骤6：获取提示词
系统自动生成完整AI提示词，可以：
- 复制到Coze创建Bot
- 集成到企业系统
- 作为付费服务提供

## 🚀 启动服务

```bash
# 在项目根目录执行
python src/main.py
```

服务将在 `http://localhost:5000` 启动

## 🎨 自定义配置

### 修改AI模型

编辑 `config/agent_llm_config.json`：

```json
{
  "config": {
    "model": "doubao-seed-1-6-251015",  // 可更换为其他模型
    "temperature": 0.7,
    "max_completion_tokens": 4096
  }
}
```

### 修改系统提示词

在同一文件中修改 `sp` 字段来自定义Agent行为。

## 📦 部署建议

### Docker部署

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "src/main.py"]
```

### 云服务部署
支持部署到：
- 阿里云
- 腾讯云
- AWS
- Google Cloud

## 💡 使用技巧

1. **多轮对话**：可以通过API保持会话上下文
2. **规则迭代**：随时可以返回修改之前的答案
3. **导出分享**：生成的提示词可以分享给团队
4. **持续优化**：根据使用反馈不断完善规则

## ⚠️ 注意事项

1. 确保环境变量配置正确
2. 检查API密钥是否有效
3. 首次使用建议使用快速模式
4. 复杂场景可以分多次完成

## 🎯 开始使用

现在就开始您的决策炼金之旅吧！

```bash
# 启动服务
python src/main.py

# 打开浏览器
# 访问 http://localhost:5000
```

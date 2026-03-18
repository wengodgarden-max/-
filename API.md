# 决策炼金师 API 文档

## 🌐 网页访问

### 启动服务
```bash
python src/main.py
```

### 访问地址
- **主页**：`http://localhost:5000/`
- **决策炼金师页面**：`http://localhost:5000/alchemist`

---

## 📡 API 接口

### 1. 对话接口（推荐）

**接口地址**：`POST /alchemist/chat`

**请求头**：
```
Content-Type: application/json
```

**请求参数**：
```json
{
  "message": "用户消息内容",
  "session_id": "会话ID（可选，用于保持上下文）",
  "mode": "quick 或 assisted（可选）"
}
```

**请求示例**：
```bash
curl -X POST "http://localhost:5000/alchemist/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我是产品经理，工作6年",
    "session_id": "user_123",
    "mode": "assisted"
  }'
```

**响应示例**：
```json
{
  "status": "success",
  "message": "很好！看到您的职业背景了...\n\n接下来，让我们盘点一下您的工作成就...",
  "session_id": "user_123",
  "run_id": "run_abc123"
}
```

**状态码**：
- `200`：成功
- `400`：请求参数错误
- `500`：服务器内部错误

---

### 2. 标准运行接口

**接口地址**：`POST /run`

**请求参数**：
```json
{
  "messages": [
    {
      "type": "human",
      "content": "你好"
    }
  ]
}
```

**请求示例**：
```bash
curl -X POST "http://localhost:5000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"type": "human", "content": "我想创建一个决策工具"}
    ]
  }'
```

**响应示例**：
```json
{
  "messages": [
    {
      "type": "ai",
      "content": "太棒了！你想创建一个决策工具..."
    }
  ],
  "run_id": "run_xyz789"
}
```

---

### 3. 流式运行接口

**接口地址**：`POST /stream_run`

**请求参数**：同 `/run` 接口

**响应格式**：SSE（Server-Sent Events）

**请求示例**：
```javascript
const eventSource = new EventSource('http://localhost:5000/stream_run', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    messages: [{type: 'human', content: '请帮我创建决策工具'}]
  })
});

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

---

### 4. OpenAI 兼容接口

**接口地址**：`POST /v1/chat/completions`

**请求参数**：
```json
{
  "model": "decision-alchemist",
  "messages": [
    {"role": "user", "content": "你好"}
  ],
  "stream": false
}
```

**请求示例**：
```bash
curl -X POST "http://localhost:5000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "decision-alchemist",
    "messages": [
      {"role": "user", "content": "我想创建决策工具"}
    ]
  }'
```

---

### 5. 健康检查

**接口地址**：`GET /health`

**请求示例**：
```bash
curl http://localhost:5000/health
```

**响应示例**：
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

---

## 🔧 集成示例

### JavaScript/TypeScript

```javascript
class DecisionAlchemist {
  constructor(baseUrl = 'http://localhost:5000') {
    this.baseUrl = baseUrl;
    this.sessionId = 'session_' + Date.now();
  }

  async chat(message, mode = 'assisted') {
    const response = await fetch(`${this.baseUrl}/alchemist/chat`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message,
        session_id: this.sessionId,
        mode
      })
    });
    
    const data = await response.json();
    return data;
  }
}

// 使用示例
const alchemist = new DecisionAlchemist();

// 开始对话
const response = await alchemist.chat('我是产品经理，工作6年', 'assisted');
console.log(response.message);
```

### Python

```python
import requests

class DecisionAlchemist:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session_id = f'session_{int(time.time())}'
    
    def chat(self, message, mode='assisted'):
        response = requests.post(
            f'{self.base_url}/alchemist/chat',
            json={
                'message': message,
                'session_id': self.session_id,
                'mode': mode
            }
        )
        return response.json()

# 使用示例
alchemist = DecisionAlchemist()

# 开始对话
response = alchemist.chat('我是产品经理，工作6年', mode='assisted')
print(response['message'])
```

### React 组件示例

```jsx
import React, { useState } from 'react';

function DecisionAlchemistChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const sessionId = React.useRef(`session_${Date.now()}`);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/alchemist/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          message: input,
          session_id: sessionId.current,
          mode: 'assisted'
        })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.message }]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <div className="chat-container">
      {messages.map((msg, i) => (
        <div key={i} className={`message ${msg.role}`}>
          {msg.content}
        </div>
      ))}
      <input 
        value={input} 
        onChange={e => setInput(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? '思考中...' : '发送'}
      </button>
    </div>
  );
}
```

---

## 📋 完整流程示例

### 辅助模式完整流程

```bash
# 1. 开始对话
curl -X POST "http://localhost:5000/alchemist/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "开始",
    "session_id": "test_session",
    "mode": "assisted"
  }'

# 2. 回答职业背景
curl -X POST "http://localhost:5000/alchemist/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我是产品经理，工作6年，主要负责用户增长",
    "session_id": "test_session"
  }'

# 3. 回答工作成就
curl -X POST "http://localhost:5000/alchemist/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "搭建了会员体系，用户留存提升25%，付费率提升15%",
    "session_id": "test_session"
  }'

# 4. 回答被请教的问题
curl -X POST "http://localhost:5000/alchemist/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "同事经常问我一个功能该不该做，怎么评估优先级",
    "session_id": "test_session"
  }'
```

---

## 🚀 部署建议

### Docker 部署

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "src/main.py"]
```

```bash
# 构建镜像
docker build -t decision-alchemist .

# 运行容器
docker run -p 5000:5000 decision-alchemist
```

### 环境变量

```bash
# 必需环境变量
export COZE_WORKLOAD_IDENTITY_API_KEY="your_api_key"
export COZE_INTEGRATION_MODEL_BASE_URL="your_base_url"

# 可选环境变量
export COZE_WORKSPACE_PATH="/workspace/projects"
```

---

## ⚡ 性能优化

### 会话管理

- 使用 `session_id` 保持多轮对话上下文
- 默认保留最近 40 条消息（20轮对话）
- 支持分布式部署（使用数据库存储会话）

### 超时设置

- 默认超时：15分钟（900秒）
- 可在 `src/main.py` 中修改 `TIMEOUT_SECONDS` 常量

### 并发控制

- 支持多用户并发访问
- 每个会话独立维护上下文
- 支持流式响应提升用户体验

---

## 🛠️ 故障排查

### 常见问题

**Q: 服务启动失败**
```bash
# 检查端口是否被占用
lsof -i:5000

# 使用其他端口
python src/main.py -p 5001
```

**Q: API 调用返回 500 错误**
```bash
# 查看日志
tail -f /app/work/logs/bypass/app.log

# 检查环境变量
echo $COZE_WORKLOAD_IDENTITY_API_KEY
```

**Q: 会话上下文丢失**
- 确保每次请求使用相同的 `session_id`
- 检查是否超过最大消息数限制

---

## 📞 技术支持

- GitHub Issues: 提交问题和建议
- 文档: 查看 `README.md` 和 `GUIDE.md`
- 日志: `/app/work/logs/bypass/app.log`

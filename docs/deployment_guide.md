# 🚀 炼金师助手 - 公开部署指南

## 快速部署方案（推荐）

### 方案一：Railway（最简单，推荐）

**优势**：免费、自动部署、支持Python后端

#### 步骤：

1. **创建 `requirements.txt`**（已存在，确保包含）
```
fastapi
uvicorn
langchain
langgraph
langchain-openai
cozeloop
requests
```

2. **创建 `Procfile`**
```
web: python src/main.py -p $PORT
```

3. **部署到 Railway**
   - 访问 https://railway.app
   - 用 GitHub 登录
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择你的仓库
   - 自动部署，获得公开链接：`https://你的项目名.up.railway.app`

4. **访问地址**：
   - 主页：`https://你的项目名.up.railway.app/`
   - 炼金师：`https://你的项目名.up.railway.app/alchemist`

---

### 方案二：Render（免费，稳定）

#### 步骤：

1. **创建 `render.yaml`**
```yaml
services:
  - type: web
    name: alchemist
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py -p $PORT
    envVars:
      - key: PORT
        value: 10000
```

2. **部署到 Render**
   - 访问 https://render.com
   - 用 GitHub 登录
   - 创建新 Web Service
   - 连接 GitHub 仓库
   - 自动部署，获得链接：`https://alchemist.onrender.com`

---

### 方案三：Zeabur（国内友好）

#### 步骤：

1. **访问 https://zeabur.com**
2. 用 GitHub 登录
3. 创建新项目
4. 添加服务 → 从 GitHub 导入
5. 自动部署，获得链接

**优势**：国内访问速度快

---

### 方案四：内网穿透（临时测试用）

#### 使用 ngrok（快速测试）：

```bash
# 安装 ngrok
brew install ngrok  # Mac
# 或下载: https://ngrok.com/download

# 启动服务
python src/main.py -p 5000

# 另一个终端运行
ngrok http 5000
```

会得到类似这样的公网地址：
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

访问地址：
- 主页：`https://abc123.ngrok.io/`
- 炼金师：`https://abc123.ngrok.io/alchemist`

**注意**：ngrok 免费版地址会变化，适合临时测试

---

## 推荐部署流程

### 第一步：推送代码到 GitHub

```bash
git init
git add .
git commit -m "feat: 炼金师助手初始化"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库.git
git push -u origin main
```

### 第二步：选择平台部署

**推荐 Railway**（最简单）：
1. 访问 https://railway.app
2. 用 GitHub 登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择你的仓库
6. 等待自动部署完成

### 第三步：获得公开链接

部署完成后，Railway 会给你一个永久链接：
```
https://alchemist-production-xxxx.up.railway.app
```

### 第四步：在小红书推广

```
🎁 免费体验链接：
https://你的链接/alchemist

新用户免费体验5轮对话
满意再付费解锁完整产出！
```

---

## 环境变量配置

在部署平台设置以下环境变量：

```bash
# 大模型配置（已在系统中配置，无需额外设置）
COZE_WORKLOAD_IDENTITY_API_KEY=你的API密钥
COZE_INTEGRATION_MODEL_BASE_URL=你的模型地址

# 工作空间
COZE_WORKSPACE_PATH=/app
```

---

## 常见问题

### Q: 部署后页面打不开？
A: 检查日志，确保 `PORT` 环境变量正确设置

### Q: API 调用失败？
A: 确认环境变量 `COZE_WORKLOAD_IDENTITY_API_KEY` 已配置

### Q: 如何更新代码？
A: 推送到 GitHub 后，平台会自动重新部署

---

## 成本估算

- **Railway**: 免费额度 $5/月（足够个人使用）
- **Render**: 完全免费（有休眠机制）
- **Zeabur**: 免费额度（国内访问快）
- **ngrok**: 免费版（临时测试）

---

## 下一步

1. ✅ 选择部署平台（推荐 Railway）
2. ✅ 推送代码到 GitHub
3. ✅ 部署并获得公开链接
4. ✅ 在小红书发布推广笔记
5. ✅ 私信发送体验链接和激活码

---

**需要我帮你创建部署配置文件吗？**

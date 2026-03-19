# 🎯 快速获得公开网页链接

## 方案对比

| 方案 | 时间成本 | 费用 | 稳定性 | 推荐度 |
|------|---------|------|--------|--------|
| Railway | 10分钟 | 免费$5/月额度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Render | 15分钟 | 完全免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| ngrok | 5分钟 | 免费（临时） | ⭐⭐ | ⭐⭐⭐ |

---

## 🚀 方案一：Railway（最推荐）

### 第一步：推送代码到 GitHub

```bash
# 在项目目录执行
cd /workspace/projects

# 如果还没有 Git 仓库
git init
git add .
git commit -m "feat: 炼金师助手"

# 推送到 GitHub（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库.git
git branch -M main
git push -u origin main
```

### 第二步：部署到 Railway

1. 打开浏览器，访问：https://railway.app
2. 点击右上角 **"Login with GitHub"**
3. 授权后，点击 **"New Project"**
4. 选择 **"Deploy from GitHub repo"**
5. 选择你刚才推送的仓库
6. Railway 会自动检测到 `Procfile` 并开始部署

### 第三步：获取公开链接

部署完成后（约 2-3 分钟）：
1. 在 Railway 项目页面，点击 **"Settings"**
2. 找到 **"Domains"** 部分
3. 点击 **"Generate Domain"**
4. 获得永久公开链接：`https://你的项目名.up.railway.app`

### 第四步：访问你的应用

```
主页：https://你的链接/
炼金师页面：https://你的链接/alchemist
```

### 第五步：在小红书推广

```
🎁 免费体验链接：
https://你的链接/alchemist

新用户免费体验5轮对话
满意再付费解锁完整产出！

💰 套餐：
• 体验版 ¥9.9 / 5次
• 标准版 ¥29.9 / 20次
• 年度会员 ¥99 / 100次

私信获取激活码～
```

---

## ⚡ 方案二：Render（完全免费）

### 步骤：

1. 访问 https://render.com
2. 用 GitHub 登录
3. 点击 **"New +"** → **"Web Service"**
4. 连接你的 GitHub 仓库
5. 配置：
   - Name: `alchemist`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python src/main.py -p $PORT`
6. 点击 **"Create Web Service"**

等待部署完成，获得链接：`https://alchemist.onrender.com`

**注意**：Render 免费版有冷启动，首次访问可能需要等待 30 秒

---

## 🔧 方案三：ngrok（临时测试）

### 如果你想快速测试，不想部署：

```bash
# 1. 下载 ngrok（如果还没有）
# 访问 https://ngrok.com/download 下载对应系统版本

# 2. 启动你的服务
python src/main.py -p 5000

# 3. 在另一个终端运行
ngrok http 5000

# 4. 会得到类似这样的链接
# Forwarding: https://abc-123-xyz.ngrok-free.app -> http://localhost:5000
```

**缺点**：
- 免费版链接会变化
- 每次重启需要重新获取链接
- 适合临时测试，不适合长期使用

---

## 📝 我帮你准备好了什么？

我已经为你创建了：

✅ `Procfile` - Railway 部署配置
✅ `runtime.txt` - Python 版本指定
✅ `docs/deployment_guide.md` - 详细部署文档
✅ `scripts/deploy_quick.sh` - 快速部署脚本

---

## 🎯 推荐行动路径

### 如果你有 GitHub 账号：
```
1. 推送代码到 GitHub (5分钟)
2. Railway 一键部署 (5分钟)
3. 获得永久链接 (立即)
4. 开始推广 (立即)
```

**总耗时：10-15 分钟**

### 如果你没有 GitHub：
```
1. 注册 GitHub (5分钟)
2. 推送代码 (5分钟)
3. Railway 部署 (5分钟)
4. 获得链接 (立即)
```

**总耗时：15-20 分钟**

---

## 💡 下一步

告诉我：
1. 你有 GitHub 账号吗？
2. 你想用哪个方案部署？

我可以帮你：
- 检查代码是否准备好推送
- 指导具体的部署步骤
- 帮你测试部署后的链接

---

**需要我帮你推送代码到 GitHub 吗？** 🚀

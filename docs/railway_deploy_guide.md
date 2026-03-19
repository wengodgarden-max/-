# 🚀 Railway 部署完整指南（炼金师助手）

## 📦 准备工作确认

✅ **代码已准备好**：
- Procfile（部署配置）
- runtime.txt（Python版本）
- requirements.txt（依赖包）
- src/agents/agent.py（核心代码）

---

## 第1步：GitHub 账号

### 如果你还没有 GitHub 账号：

1. 打开 https://github.com/signup
2. 填写用户名、邮箱、密码
3. 验证邮箱
4. 完成（2分钟）

### 如果已有 GitHub 账号：

直接进入第2步 👇

---

## 第2步：创建 GitHub 仓库

### 操作步骤：

1. 登录 GitHub
2. 点击右上角 **"+"** → **"New repository"**
3. 填写信息：
   - Repository name: `alchemist`
   - Description: `炼金师助手 - 把你的判断力变成付费AI工具`
   - 选择 **Public**（公开）
   - ❌ **不要勾选** "Add a README file"
   - ❌ **不要勾选** ".gitignore"
   - ❌ **不要勾选** "license"
4. 点击 **"Create repository"**

---

## 第3步：推送代码到 GitHub

### 方法一：网页上传（最简单，推荐）

1. 在新建的仓库页面，点击 **"uploading an existing file"**
2. 把以下文件/文件夹拖进去：
   - `Procfile`
   - `runtime.txt`
   - `requirements.txt`
   - `src/` 整个文件夹
   - `config/` 整个文件夹
   - `assets/` 整个文件夹
   - `README.md`
3. 点击 **"Commit changes"**

### 方法二：Git 命令推送

```bash
# 在项目目录执行
cd /workspace/projects

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "feat: 炼金师助手初始化"

# 设置分支
git branch -M main

# 连接远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/alchemist.git

# 推送
git push -u origin main
```

---

## 第4步：Railway 部署

### 4.1 登录 Railway

1. 打开 https://railway.app
2. 点击右上角 **"Login"**
3. 选择 **"Login with GitHub"**
4. 授权 Railway 访问你的 GitHub

### 4.2 创建项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择你刚才创建的 `alchemist` 仓库
4. Railway 会自动检测到 `Procfile` 并开始部署

### 4.3 等待部署

- 部署时间：约 2-3 分钟
- 你会看到构建日志滚动
- 当看到 **"SUCCESS"** 时表示部署完成

---

## 第5步：获得永久公开链接

### 5.1 生成域名

1. 在 Railway 项目页面，点击 **"Settings"** 标签
2. 滚动到 **"Domains"** 部分
3. 点击 **"Generate Domain"**
4. Railway 会自动生成一个域名

### 5.2 你的公开链接

格式如下：
```
https://alchemist-production-xxxx.up.railway.app
```

**访问地址**：
- 主页：`https://你的域名/`
- 炼金师页面：`https://你的域名/alchemist`
- 健康检查：`https://你的域名/health`

---

## 第6步：测试链接

在浏览器打开你的链接，确认：
- ✅ 主页能打开
- ✅ 炼金师页面能打开
- ✅ 可以正常对话

---

## 第7步：环境变量配置（如果需要）

如果在 Railway 部署时遇到错误，可能需要配置环境变量：

1. 在 Railway 项目页面，点击 **"Variables"** 标签
2. 添加以下变量（如果系统没有自动识别）：
   - `PORT`: `5000`（或 Railway 自动分配的端口）

**注意**：大多数情况下不需要手动配置，Railway 会自动处理。

---

## 🎉 完成！现在可以推广了

### 小红书笔记文案

```
🎁 免费体验链接：
https://你的铁路域名/alchemist

新用户免费体验5轮对话
满意再付费解锁完整产出！

💰 套餐：
• 体验版 ¥9.9 / 5次
• 标准版 ¥29.9 / 20次（推荐）
• 年度会员 ¥99 / 100次

私信获取激活码～
```

### 私信话术

```
您好！这是体验链接：
https://你的铁路域名/alchemist

激活码：GOLD-001
（体验版 ¥9.9 / 5次）

有问题随时问我！
```

---

## ⚠️ 常见问题

### Q: 部署失败怎么办？
A: 查看构建日志，检查是否有错误信息。通常是依赖包问题，检查 requirements.txt

### Q: 页面打开很慢？
A: Railway 免费版可能有冷启动，首次访问需要等待几秒

### Q: 如何更新代码？
A: 推送新代码到 GitHub，Railway 会自动重新部署

### Q: 如何查看访问日志？
A: 在 Railway 项目页面点击 "Logs" 标签

---

## 💡 下一步优化

1. ✅ 自定义域名（可选）
2. ✅ 监控访问数据
3. ✅ 配置 SSL 证书（Railway 自动提供）
4. ✅ 设置自动扩容（如果流量大）

---

**现在告诉我你的 GitHub 用户名，我帮你推送代码！** 🚀

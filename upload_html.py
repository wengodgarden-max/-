"""上传HTML到对象存储并生成公开访问链接"""
import os
from coze_coding_dev_sdk.s3 import S3SyncStorage

# 初始化存储客户端
storage = S3SyncStorage(
    endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
    access_key="",
    secret_key="",
    bucket_name=os.getenv("COZE_BUCKET_NAME"),
    region="cn-beijing",
)

# 读取HTML文件
html_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "assets/pages/index.html")
with open(html_path, 'rb') as f:
    html_content = f.read()

# 上传到对象存储
key = storage.upload_file(
    file_content=html_content,
    file_name="decision-alchemist/index.html",
    content_type="text/html; charset=utf-8",
)

print(f"上传成功，key: {key}")

# 生成30天有效的访问链接
url = storage.generate_presigned_url(
    key=key,
    expire_time=2592000,  # 30天
)

print(f"\n✅ 公开访问链接: {url}")

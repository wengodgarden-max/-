#!/usr/bin/env python3
"""
提取参考文档内容的脚本
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.document_parser import parse_document_direct
import json

# 文档URL列表
documents = {
    "知识资产盘点模版": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E7%9B%98%E7%82%B9%E4%B8%AA%E4%BA%BA%E7%9F%A5%E8%AF%86%E8%B5%84%E4%BA%A7%E7%9A%84%E6%A8%A1%E7%89%88_688544.docx&nonce=bb420980-1db8-4ea2-9f46-7e8ce2375990&project_id=7618407610735296563&sign=087dc76ea527bb40ebbf5e3d2f218b9157b444fefcd71b5a4723935624bccf67",
    "课程教学目标模版": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E8%AF%BE%E7%A8%8B%E6%95%99%E5%AD%A6%E7%9B%AE%E6%A0%87%E7%9A%84%E8%AE%BE%E5%AE%9A%E6%A8%A1%E7%89%88_%E5%B0%81%E6%B5%8B%E7%89%88_943469.docx&nonce=cda214fe-2942-4286-9373-8e6277d46fa4&project_id=7618407610735296563&sign=4c002f689de60af302f3f9a7bca7c2009cdaf4d494a620d6333e7aa732b2bc4d",
    "案例一_产品经理": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E6%A1%88%E4%BE%8B%E4%B8%80_6%E5%B9%B4_%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86_134357.pdf&nonce=a36c498a-f437-408f-af9c-054442c658f5&project_id=7618407610735296563&sign=f1b919f2a590883e624c5675f35c6de6f8f39380a8fda8a5d4aca5d8f05807bb",
    "案例二_研发": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E6%A1%88%E4%BE%8B%E4%BA%8C_6%E5%B9%B4_%E7%A0%94%E5%8F%91_398309.pdf&nonce=b7e4b32a-6159-4ab4-ab54-757bc7a8c3f5&project_id=7618407610735296563&sign=585808301e346260bba774ca14f574da854da3a18e9984ead8e00d539438aa98",
    "专业知识分享PPT": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%EF%BC%81%E4%BB%8E%E4%B8%93%E5%AE%B6%E5%87%BA%E5%8F%91%E7%9A%84%E4%B8%93%E4%B8%9A%E7%9F%A5%E8%AF%86%E5%88%86%E4%BA%AB.pptx&nonce=b872da99-1222-4d3b-9061-943743a5fa3c&project_id=7618407610735296563&sign=aa1d15f9994cd9bcddf74a892957e810670b6eacad0f77b82f95cc6cb989d49d"
}

print("开始解析参考文档...")
print("=" * 80)

for name, url in documents.items():
    print(f"\n正在解析: {name}")
    print("-" * 80)
    
    result = parse_document_direct(url)
    
    if result.get("success"):
        print(f"标题: {result.get('title')}")
        print(f"文件类型: {result.get('file_type')}")
        print(f"内容长度: {len(result.get('content', ''))}")
        print(f"\n内容摘要:\n{result.get('content', '')[:1000]}...")
    else:
        print(f"解析失败: {result.get('error')}")
    
    print()

print("=" * 80)
print("文档解析完成！")

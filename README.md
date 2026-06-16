# RAG 智能问答 API

基于 FastAPI + DeepSeek 的文档问答服务，支持多格式文档上传和流式输出。

## 功能

- 📄 支持 TXT、PDF、Word 文档上传
- 🤖 基于 DeepSeek API 智能问答
- ⚡ 流式输出
- 📚 自动生成 Swagger API 文档
- 🔒 环境变量管理 API Key

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn rag_api:app --reload
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /ask_with_file | POST | 上传文档并提问 |
| /ask_with_file_stream | POST | 流式输出版本 |
| /docs | GET | Swagger API 文档 |
| /health | GET | 健康检查 |

## 技术栈

- Python 3.12
- FastAPI
- DeepSeek API
- PyPDF2 / python-docx
- python-dotenv

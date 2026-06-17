# RAG 多格式文档问答 API

支持 TXT / PDF / Word 上传，基于分块+向量检索+DeepSeek 大模型，返回文档相关答案

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

| 技术 | 用途 |
|------|------|
|Python 3.12| 开发语言|
|FastAPI API| 框架|
|DeepSeek API |大模型|
|LangChain| 分块 + 向量检索|
|ChromaDB| 向量数据库|
|HuggingFace Embeddings |文本向量化|
|PyPDF2 / python-docx |文档解析|
|python-dotenv| 环境变量管理|
|uvicorn| 服务部署|

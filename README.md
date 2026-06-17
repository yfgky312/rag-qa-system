# RAG 多格式文档问答 API

支持 TXT / PDF / Word 上传，基于分块+向量检索+DeepSeek 大模型，返回文档相关答案

## 功能

功能 说明
📄 多格式上传 TXT / PDF / Word
✂️ 智能分块 自动分块，支持长文档
🔍 向量检索 基于语义相似度检索相关内容
🤖 大模型生成 DeepSeek 基于文档内容回答
📚 API 文档 Swagger 自动生成

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

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/yfgky312/rag-qa-system.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY

# 4. 启动服务
uvicorn rag_api:app --reload

# RAG 智能问答系统

基于 DeepSeek API + LangChain 的 RAG 问答系统，支持从文档中检索内容并生成回答。

## 功能特点

- 支持 TXT 文档加载
- 文本分块处理（可调 chunk_size）
- 基于向量检索的相似度匹配
- 调用 DeepSeek API 生成回答
- GPU 加速（PyTorch CUDA）

## 技术栈

- Python 3.12
- PyTorch (GPU)
- LangChain
- DeepSeek API
- FastEmbed

## 快速开始

```bash
pip install -r requirements.txt
python rag_complete.py

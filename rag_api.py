import os
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
import torch
from dotenv import load_dotenv
load_dotenv()

# 文档解析库
from pypdf import PdfReader
from docx import Document

# 配置
import os
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

app = FastAPI(title="RAG 问答 API", description="支持多种文档格式的智能问答系统")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    status: str


# ==================== 文档解析函数 ====================

def parse_txt(file) -> str:
    """解析 TXT 文件"""
    content = file.file.read().decode('utf-8')
    return content


def parse_pdf(file) -> str:
    """解析 PDF 文件"""
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def parse_docx(file) -> str:
    """解析 Word 文件"""
    doc = Document(file.file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def parse_file(file: UploadFile) -> str:
    """根据文件扩展名自动选择解析器"""
    filename = file.filename.lower()

    if filename.endswith('.txt'):
        return parse_txt(file)
    elif filename.endswith('.pdf'):
        return parse_pdf(file)
    elif filename.endswith('.docx'):
        return parse_docx(file)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {filename}。仅支持 .txt, .pdf, .docx"
        )


# ==================== 大模型调用 ====================

def ask_deepseek(question: str, context: str) -> str:
    """调用 DeepSeek API 生成回答"""
    # 限制上下文长度，防止超过 token 限制
    max_context_len = 3000
    if len(context) > max_context_len:
        context = context[:max_context_len] + "\n...(内容已截断)"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "基于提供的文档内容回答问题。如果文档中没有相关信息，请明确说明，不要编造。"},
            {"role": "user", "content": f"文档内容：\n{context}\n\n问题：{question}"}
        ]
    )
    return response.choices[0].message.content


# ==================== API 接口 ====================

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ask_with_file", response_model=AnswerResponse)
async def ask_with_file(
        file: UploadFile = File(..., description="上传文档（支持 .txt, .pdf, .docx）"),
        question: str = ""
):
    """
    上传文档并提问
    - 支持格式：TXT、PDF、Word (.docx)
    - 如果不提供问题，默认问"这份文档主要讲了什么？"
    """
    try:
        # 解析文档
        content = parse_file(file)

        if not content or len(content.strip()) < 10:
            raise HTTPException(status_code=400, detail="文档内容为空或太少")

        # 默认问题
        if not question:
            question = "这份文档主要讲了什么？"

        # 调用大模型
        answer = ask_deepseek(question, content)

        return AnswerResponse(answer=answer, status="success")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    使用固定文档回答问题（兼容旧接口）
    """
    TXT_PATH = r"C:\Users\qq_1098\Desktop\新建 文本文档.txt"
    try:
        with open(TXT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        answer = ask_deepseek(request.question, content)
        return AnswerResponse(answer=answer, status="success")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="文档文件不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.responses import StreamingResponse


@app.post("/ask_with_file_stream")
async def ask_with_file_stream(
        file: UploadFile = File(...),
        question: str = ""
):
    """
    流式输出版本，一个字一个字地显示回答
    """
    content = parse_file(file)
    if not question:
        question = "这份文档主要讲了什么？"

    def generate():
        # 调用 DeepSeek 流式接口
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "基于文档内容回答问题。"},
                {"role": "user", "content": f"文档内容：\n{content[:3000]}\n\n问题：{question}"}
            ],
            stream=True  # 开启流式输出
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(generate(), media_type="text/plain")
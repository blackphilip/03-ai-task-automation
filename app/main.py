import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from app.schemas import MeetingSummary
from app.services.ai_agent import analyze_meeting_transcript

# 載入環境變數
load_dotenv()

app = FastAPI(
    title="🤖 AI 會議摘要與 Task 自動化 API",
    description="自動解析會議逐字稿與長文件，萃取核心決議、待辦事項與時間節點 (FastAPI + Gemini API Agent)",
    version="1.0.0"
)

class TranscriptRequest(BaseModel):
    transcript: str = Field(..., description="會議逐字稿、會議紀錄或長文內容", example="專案開會記錄：張主任決定於下週三前完成... ")

@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "service": "AI Task Automation API",
        "version": "1.0.0"
    }

@app.post("/api/v1/analyze", response_model=MeetingSummary, tags=["AI Processing"])
def process_transcript(payload: TranscriptRequest):
    """
    接收會議逐字稿文本，呼叫 Gemini AI Agent 進行自動化解析與 Task 萃取。
    """
    if not payload.transcript.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="會議內容不能為空，請輸入有效的逐字稿文字。"
        )
    
    try:
        result = analyze_meeting_transcript(payload.transcript)
        return result
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI 分析過程發生錯誤：{str(e)}"
        )
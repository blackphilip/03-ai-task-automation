import os
from google import genai
from google.genai import types
from app.schemas import MeetingSummary

def analyze_meeting_transcript(transcript_text: str) -> MeetingSummary:
    """
    呼叫 Gemini API 解析會議逐字稿，透過 Structured Outputs (JSON Schema) 強制輸出格式化資料。
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("未設定 GEMINI_API_KEY，請檢查 .env 檔案。")

    # 初始化 Gemini Client
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    你是一位高效率且專業的專案管理 (PM) 助手。請詳細分析以下會議逐字稿/紀錄內容：
    1. 提煉出會議的核心決議。
    2. 萃取所有待辦事項 (Action Items)，過濾掉無關緊要的發言與禱告詞/發言客套話，精準標註優先順序、負責人與預計完成時間。
    3. 提供一份 200 字以內的精簡會議總結。

    會議內容：
    {transcript_text}
    """
    
    # 使用 gemini-3.1-flash-lite 模型並啟用結構化輸出 (Structured Outputs)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MeetingSummary,
            temperature=0.2,
        ),
    )
    
    # 自動將 JSON 轉譯並驗證為 MeetingSummary Pydantic 物件
    return MeetingSummary.model_validate_json(response.text)
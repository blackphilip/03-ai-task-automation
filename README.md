# 🤖 AI 智慧會議摘要與 Task 自動化 API (AI Meeting Summary & Task Automation Agent)

> **結合 FastAPI、Google Gemini API (`gemini-3.1-flash`) 與 Pydantic 結構化驗證，實現逐字稿自動化解析、核心決議提煉與待辦事項 (Action Items) 萃取之微服務。**

---

## 💡 專案簡介與痛點解決

在跨國團隊、專案開發與企業例會中，整理會議紀錄與追蹤待辦事項往往消耗大量人工時間（每次開會需耗費 15~30 分鐘）。傳統人工整理常面臨**責任指派模糊**、**預計完成時間遺漏**，以及**發言廢話或客套話難以有效過濾**等痛點。

本專案建構了一套**微服務化 AI 工作流 API**：
1. 使用者或前端可透過 RESTful API 端點傳入會議逐字稿、會議紀錄或長文內容。
2. 系統呼叫 **Gemini 3.1 Flash** 進行語意理解與雜訊過濾，自動排除冗長發言與無關客套話。
3. 採用 **Pydantic Schema (Structured Outputs)** 強制 LLM 輸出 100% 格式化的 JSON 資料，精準萃取「核心決議」與包含「負責人、優先級、截止日」的待辦事項。
4. 提供標準 OpenAPI (Swagger) 互動式文件，具備非同步處理與完整的例外處理機制，利於後續擴展串接 Email、Notion 或 Slack 等自動化通知服務。

---

## 🛠️ 技術架構與工具 (Tech Stack)

* **Language:** Python (v3.10+)
* **Framework & Web:** FastAPI, Uvicorn (Asynchronous REST API)
* **AI & LLM:** Google Gemini API (`gemini-3.1-flash`), Google GenAI SDK (`google-genai`)
* **Data Validation & Schemas:** Pydantic (v2.x / Structured Outputs)
* **DevOps & Environment:** Docker, VS Code, Python Virtual Environment (`venv`), Git/GitHub (Version Control), `python-dotenv`

---

## 🏗️ 系統運作架構圖 (Workflow)

```text
[ Client / Web / Postman 傳送逐字稿 ]
         │
         ▼
[ FastAPI POST /api/v1/analyze ] ───► [ Pydantic Payload 輸入驗證 ]
         │
         ▼
[ Gemini 3.1 Flash AI Agent ] ───► (Prompt 過濾發言雜訊與客套話)
         │
         ▼
[ Structured Outputs (JSON Schema) ] ───► [ Pydantic 二道模型驗證 (MeetingSummary) ]
         │
         ▼
[ 結構化 JSON 回應 ] ───► (輸出標題、核心決議、任務與 200 字摘要)
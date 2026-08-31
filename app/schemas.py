from pydantic import BaseModel, Field
from typing import List, Optional

class ActionItem(BaseModel):
    task: str = Field(description="待辦事項內容描述")
    assignee: Optional[str] = Field(default="未指定", description="負責人或執行單位")
    priority: str = Field(description="優先級：高 / 中 / 低")
    due_date: Optional[str] = Field(default="未指定", description="預計完成時間、截止日或時間節點")

class MeetingSummary(BaseModel):
    title: str = Field(description="會議主題或文件標題")
    core_decisions: List[str] = Field(description="核心決議事項列表")
    action_items: List[ActionItem] = Field(description="待辦事項 (Action Items) 列表")
    summary: str = Field(description="200字以內的精簡會議總結")
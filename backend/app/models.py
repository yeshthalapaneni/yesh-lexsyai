from pydantic import BaseModel
from typing import List, Optional


class Placeholder(BaseModel):
id: str
name: str # slug, e.g., company_name
display_name: str # e.g., "Company Name"
value: Optional[str] = None
status: str = "pending" # pending|filled


class ExtractResponse(BaseModel):
session_id: str
filename: str
placeholders: List[Placeholder]
chars: int


class ChatRequest(BaseModel):
session_id: str
placeholder_id: str
message: str


class ChatResponse(BaseModel):
reply: str
placeholder: Placeholder


class SessionInfo(BaseModel):
session_id: str
filename: str
placeholders: List[Placeholder]

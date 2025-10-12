from typing import Optional, Any, Dict

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(..., max_length=1)


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    meta: Dict[str, Any] = {}
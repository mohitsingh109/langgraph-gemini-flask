from typing import Optional, Any, Dict

from pydantic import BaseModel, Field

# Model
# Scheme
# Input payload from human side
class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(..., max_length=1)

# AI Response
class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    meta: Dict[str, Any] = {} # Token usage

# IAM Role, URN code - you can connect two aws account
# DEV, PROD, RES, ...
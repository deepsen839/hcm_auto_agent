from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InteractionCreate(BaseModel):
    hcp_name: str
    interaction_type: str
    raw_notes: str
    follow_up_required: Optional[bool] = False

class ChatRequest(BaseModel):
    message: str
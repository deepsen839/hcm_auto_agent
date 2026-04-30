# app/routes/chat.py

from fastapi import APIRouter

from pydantic import BaseModel

from app.agent import agent

router = APIRouter()

# =========================
# REQUEST MODEL
# =========================

class ChatRequest(BaseModel):

    message: str

    existing_data: dict = {}
    current_datetime: str | None = None

# =========================
# CHAT ROUTE
# =========================

@router.post("/chat")

async def chat(payload: ChatRequest):

    result = agent.invoke({

        "user_input":
            payload.message,

        "interaction_data":
            payload.existing_data,
        "current_datetime":
            payload.current_datetime
    })

    return result["final_output"]
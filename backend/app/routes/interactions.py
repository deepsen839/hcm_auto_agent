from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import InteractionCreate
from app.models import Interaction
from app.db import SessionLocal
from app.agent import agent

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/interactions")
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    result = agent.invoke({
        "input_data": payload.dict()
    })

    interaction = Interaction(**result["output_data"])

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction
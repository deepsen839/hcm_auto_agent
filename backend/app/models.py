from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base
import uuid
from datetime import datetime

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hcp_name = Column(String)
    interaction_type = Column(String)
    raw_notes = Column(Text)
    ai_summary = Column(Text)
    sentiment = Column(String)
    follow_up_required = Column(Boolean)
    follow_up_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
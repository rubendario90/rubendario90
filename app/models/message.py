"""
Database model for messages.
"""
from sqlalchemy import Column, String, DateTime, Integer
from app.core.database import Base
from datetime import datetime, timezone

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sender = Column(String, nullable=False)
    word_count = Column(Integer, nullable=True)
    character_count = Column(Integer, nullable=True)
    processed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
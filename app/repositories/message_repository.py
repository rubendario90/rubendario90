"""
Repository for message data access operations.
"""
from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.schemas import MessageCreate
from typing import List, Optional

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, message_data: MessageCreate, word_count: int, character_count: int) -> Message:
        """Create a new message in the database."""
        db_message = Message(
            message_id=message_data.message_id,
            session_id=message_data.session_id,
            content=message_data.content,
            timestamp=message_data.timestamp,
            sender=message_data.sender,
            word_count=word_count,
            character_count=character_count
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Get a message by its ID."""
        return self.db.query(Message).filter(Message.message_id == message_id).first()

    def get_messages_by_session(
        self, 
        session_id: str, 
        sender: Optional[str] = None, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[Message]:
        """Get messages by session ID with optional filtering and pagination."""
        query = self.db.query(Message).filter(Message.session_id == session_id)
        
        if sender:
            query = query.filter(Message.sender == sender)
        
        return query.offset(offset).limit(limit).all()

    def count_messages_by_session(self, session_id: str, sender: Optional[str] = None) -> int:
        """Count messages in a session."""
        query = self.db.query(Message).filter(Message.session_id == session_id)
        
        if sender:
            query = query.filter(Message.sender == sender)
        
        return query.count()
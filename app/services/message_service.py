"""
Service layer for message processing business logic.
"""
from app.models.schemas import MessageCreate, MessageResponse, MessageMetadata
from app.repositories.message_repository import MessageRepository
from app.core.exceptions import ValidationError, DuplicateMessageError
from typing import List, Optional
import re

class MessageProcessingService:
    # Simple inappropriate words filter (can be extended)
    INAPPROPRIATE_WORDS = ['spam', 'abuse', 'hate', 'violent']

    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    def process_message(self, message_data: MessageCreate) -> MessageResponse:
        """Process and store a message."""
        # Check if message already exists
        existing_message = self.message_repository.get_message_by_id(message_data.message_id)
        if existing_message:
            raise DuplicateMessageError(f"Message with ID {message_data.message_id} already exists")

        # Content filtering
        if self._contains_inappropriate_content(message_data.content):
            raise ValidationError("Message contains inappropriate content")

        # Calculate metadata
        word_count = self._count_words(message_data.content)
        character_count = len(message_data.content)

        # Store message
        stored_message = self.message_repository.create_message(
            message_data, word_count, character_count
        )

        # Return response
        return MessageResponse(
            message_id=stored_message.message_id,
            session_id=stored_message.session_id,
            content=stored_message.content,
            timestamp=stored_message.timestamp,
            sender=stored_message.sender,
            metadata=MessageMetadata(
                word_count=stored_message.word_count,
                character_count=stored_message.character_count,
                processed_at=stored_message.processed_at
            )
        )

    def get_session_messages(
        self, 
        session_id: str, 
        sender: Optional[str] = None, 
        limit: int = 50, 
        offset: int = 0
    ) -> tuple[List[MessageResponse], dict]:
        """Get messages for a session with pagination info."""
        messages = self.message_repository.get_messages_by_session(
            session_id, sender, limit, offset
        )
        total_count = self.message_repository.count_messages_by_session(session_id, sender)

        message_responses = []
        for msg in messages:
            message_responses.append(MessageResponse(
                message_id=msg.message_id,
                session_id=msg.session_id,
                content=msg.content,
                timestamp=msg.timestamp,
                sender=msg.sender,
                metadata=MessageMetadata(
                    word_count=msg.word_count,
                    character_count=msg.character_count,
                    processed_at=msg.processed_at
                )
            ))

        pagination_info = {
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_next": offset + limit < total_count
        }

        return message_responses, pagination_info

    def _contains_inappropriate_content(self, content: str) -> bool:
        """Check if content contains inappropriate words."""
        content_lower = content.lower()
        return any(word in content_lower for word in self.INAPPROPRIATE_WORDS)

    def _count_words(self, content: str) -> int:
        """Count words in content."""
        words = re.findall(r'\b\w+\b', content)
        return len(words)
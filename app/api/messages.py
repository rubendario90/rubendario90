"""
API endpoints for message operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import (
    MessageCreate, 
    ApiResponse, 
    ApiErrorResponse, 
    ErrorDetail,
    MessagesListResponse
)
from app.repositories.message_repository import MessageRepository
from app.services.message_service import MessageProcessingService
from app.core.exceptions import ValidationError, DuplicateMessageError
from typing import Optional
from pydantic import ValidationError as PydanticValidationError

router = APIRouter()

@router.post("/messages", response_model=ApiResponse)
async def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """Create and process a new message."""
    try:
        # Initialize repository and service
        repository = MessageRepository(db)
        service = MessageProcessingService(repository)
        
        # Process the message
        processed_message = service.process_message(message)
        
        return ApiResponse(
            status="success",
            data={
                "message_id": processed_message.message_id,
                "session_id": processed_message.session_id,
                "content": processed_message.content,
                "timestamp": processed_message.timestamp.isoformat(),
                "sender": processed_message.sender,
                "metadata": {
                    "word_count": processed_message.metadata.word_count,
                    "character_count": processed_message.metadata.character_count,
                    "processed_at": processed_message.metadata.processed_at.isoformat()
                }
            }
        )
    
    except DuplicateMessageError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": "error",
                "error": {
                    "code": "DUPLICATE_MESSAGE",
                    "message": "Message already exists",
                    "details": str(e)
                }
            }
        )
    
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "error": {
                    "code": "INVALID_CONTENT",
                    "message": "Message content is invalid",
                    "details": str(e)
                }
            }
        )
    
    except PydanticValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "error": {
                    "code": "INVALID_FORMAT",
                    "message": "Invalid message format",
                    "details": str(e)
                }
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Internal server error",
                    "details": "An unexpected error occurred"
                }
            }
        )

@router.get("/messages/{session_id}", response_model=MessagesListResponse)
async def get_messages(
    session_id: str,
    sender: Optional[str] = Query(None, pattern="^(user|system)$"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get messages for a specific session."""
    try:
        # Initialize repository and service
        repository = MessageRepository(db)
        service = MessageProcessingService(repository)
        
        # Get messages
        messages, pagination_info = service.get_session_messages(
            session_id, sender, limit, offset
        )
        
        # Convert to response format
        message_data = []
        for msg in messages:
            message_data.append({
                "message_id": msg.message_id,
                "session_id": msg.session_id,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "sender": msg.sender,
                "metadata": {
                    "word_count": msg.metadata.word_count,
                    "character_count": msg.metadata.character_count,
                    "processed_at": msg.metadata.processed_at.isoformat()
                }
            })
        
        return MessagesListResponse(
            status="success",
            data=message_data,
            pagination=pagination_info
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Internal server error",
                    "details": "An unexpected error occurred"
                }
            }
        )
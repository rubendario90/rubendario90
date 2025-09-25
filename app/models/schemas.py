"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List

class MessageCreate(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str

    @field_validator('sender')
    @classmethod
    def validate_sender(cls, v):
        if v not in ['user', 'system']:
            raise ValueError('sender must be "user" or "system"')
        return v

    @field_validator('message_id')
    @classmethod
    def validate_message_id(cls, v):
        if not v or not v.strip():
            raise ValueError('message_id cannot be empty')
        return v

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v):
        if not v or not v.strip():
            raise ValueError('session_id cannot be empty')
        return v

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('content cannot be empty')
        return v

class MessageMetadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: datetime

class MessageResponse(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: MessageMetadata

    model_config = {"from_attributes": True}

class ApiResponse(BaseModel):
    status: str
    data: Optional[dict] = None

class ApiErrorResponse(BaseModel):
    status: str
    error: dict

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[str] = None

class MessagesListResponse(BaseModel):
    status: str
    data: List[MessageResponse]
    pagination: Optional[dict] = None
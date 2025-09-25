"""
Unit tests for message service.
"""
import pytest
from datetime import datetime
from app.services.message_service import MessageProcessingService
from app.repositories.message_repository import MessageRepository
from app.models.schemas import MessageCreate
from app.core.exceptions import ValidationError, DuplicateMessageError

def test_process_valid_message(db_session):
    """Test processing a valid message."""
    repository = MessageRepository(db_session)
    service = MessageProcessingService(repository)
    
    message_data = MessageCreate(
        message_id="test-123",
        session_id="session-456",
        content="Hello world, this is a test message",
        timestamp=datetime.now(),
        sender="user"
    )
    
    result = service.process_message(message_data)
    
    assert result.message_id == "test-123"
    assert result.session_id == "session-456"
    assert result.content == "Hello world, this is a test message"
    assert result.sender == "user"
    assert result.metadata.word_count == 7
    assert result.metadata.character_count == 35

def test_process_message_with_inappropriate_content(db_session):
    """Test processing a message with inappropriate content."""
    repository = MessageRepository(db_session)
    service = MessageProcessingService(repository)
    
    message_data = MessageCreate(
        message_id="test-124",
        session_id="session-456",
        content="This is spam content",
        timestamp=datetime.now(),
        sender="user"
    )
    
    with pytest.raises(ValidationError):
        service.process_message(message_data)

def test_process_duplicate_message(db_session):
    """Test processing a duplicate message."""
    repository = MessageRepository(db_session)
    service = MessageProcessingService(repository)
    
    message_data = MessageCreate(
        message_id="test-125",
        session_id="session-456",
        content="Test message",
        timestamp=datetime.now(),
        sender="user"
    )
    
    # First message should succeed
    service.process_message(message_data)
    
    # Second message with same ID should fail
    with pytest.raises(DuplicateMessageError):
        service.process_message(message_data)

def test_get_session_messages(db_session):
    """Test retrieving messages for a session."""
    repository = MessageRepository(db_session)
    service = MessageProcessingService(repository)
    
    # Create test messages
    messages = [
        MessageCreate(
            message_id=f"test-{i}",
            session_id="session-789",
            content=f"Test message {i}",
            timestamp=datetime.now(),
            sender="user" if i % 2 == 0 else "system"
        )
        for i in range(5)
    ]
    
    for msg in messages:
        service.process_message(msg)
    
    # Get all messages
    results, pagination = service.get_session_messages("session-789")
    assert len(results) == 5
    
    # Get only user messages
    user_results, _ = service.get_session_messages("session-789", sender="user")
    assert len(user_results) == 3
    
    # Get only system messages
    system_results, _ = service.get_session_messages("session-789", sender="system")
    assert len(system_results) == 2

def test_word_count_calculation(db_session):
    """Test word count calculation."""
    repository = MessageRepository(db_session)
    service = MessageProcessingService(repository)
    
    # Test with punctuation and multiple spaces
    message_data = MessageCreate(
        message_id="test-word-count",
        session_id="session-word",
        content="Hello,   world! This is a test... with punctuation.",
        timestamp=datetime.now(),
        sender="user"
    )
    
    result = service.process_message(message_data)
    assert result.metadata.word_count == 8
"""
Integration tests for API endpoints.
"""
import pytest
from datetime import datetime

def test_create_message_success(client):
    """Test successful message creation."""
    message_data = {
        "message_id": "msg-123456",
        "session_id": "session-abcdef",
        "content": "Hello, how can I help you today?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "system"
    }
    
    response = client.post("/api/messages", json=message_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["message_id"] == "msg-123456"
    assert data["data"]["content"] == "Hello, how can I help you today?"
    assert data["data"]["metadata"]["word_count"] == 6

def test_create_message_invalid_sender(client):
    """Test message creation with invalid sender."""
    message_data = {
        "message_id": "msg-invalid",
        "session_id": "session-test",
        "content": "Test message",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "invalid"
    }
    
    response = client.post("/api/messages", json=message_data)
    assert response.status_code == 422

def test_create_message_inappropriate_content(client):
    """Test message creation with inappropriate content."""
    message_data = {
        "message_id": "msg-inappropriate",
        "session_id": "session-test",
        "content": "This is spam content",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user"
    }
    
    response = client.post("/api/messages", json=message_data)
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"]["error"]["code"] == "INVALID_CONTENT"

def test_create_duplicate_message(client):
    """Test creating duplicate message."""
    message_data = {
        "message_id": "msg-duplicate",
        "session_id": "session-test",
        "content": "Test message",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user"
    }
    
    # First request should succeed
    response1 = client.post("/api/messages", json=message_data)
    assert response1.status_code == 200
    
    # Second request should fail
    response2 = client.post("/api/messages", json=message_data)
    assert response2.status_code == 409
    
    data = response2.json()
    assert data["detail"]["error"]["code"] == "DUPLICATE_MESSAGE"

def test_get_messages_by_session(client):
    """Test retrieving messages by session."""
    # Create test messages
    messages = [
        {
            "message_id": f"msg-{i}",
            "session_id": "session-get-test",
            "content": f"Test message {i}",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user" if i % 2 == 0 else "system"
        }
        for i in range(5)
    ]
    
    for msg in messages:
        client.post("/api/messages", json=msg)
    
    # Get all messages
    response = client.get("/api/messages/session-get-test")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 5
    assert data["pagination"]["total"] == 5

def test_get_messages_with_sender_filter(client):
    """Test retrieving messages with sender filter."""
    # Create test messages
    messages = [
        {
            "message_id": f"msg-filter-{i}",
            "session_id": "session-filter-test",
            "content": f"Test message {i}",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user" if i % 2 == 0 else "system"
        }
        for i in range(4)
    ]
    
    for msg in messages:
        client.post("/api/messages", json=msg)
    
    # Get only user messages
    response = client.get("/api/messages/session-filter-test?sender=user")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["data"]) == 2
    assert all(msg["sender"] == "user" for msg in data["data"])

def test_get_messages_with_pagination(client):
    """Test message retrieval with pagination."""
    # Create test messages
    messages = [
        {
            "message_id": f"msg-page-{i}",
            "session_id": "session-page-test",
            "content": f"Test message {i}",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user"
        }
        for i in range(10)
    ]
    
    for msg in messages:
        client.post("/api/messages", json=msg)
    
    # Get first page
    response = client.get("/api/messages/session-page-test?limit=5&offset=0")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["data"]) == 5
    assert data["pagination"]["total"] == 10
    assert data["pagination"]["has_next"] == True
    
    # Get second page
    response = client.get("/api/messages/session-page-test?limit=5&offset=5")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["data"]) == 5
    assert data["pagination"]["has_next"] == False

def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Chat Message Processing API is running"
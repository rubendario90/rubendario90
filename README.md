# Chat Message Processing API

A Python-based RESTful API for processing chat messages, built with FastAPI and following clean architecture principles.

## 🚀 Features

- **Message Processing**: Validates, filters, and processes chat messages
- **Content Filtering**: Basic inappropriate content detection and blocking
- **Metadata Generation**: Automatic word count and character count calculation
- **Session Management**: Retrieve messages by session with pagination
- **Clean Architecture**: Separation of concerns with repositories, services, and controllers
- **Comprehensive Testing**: Unit and integration tests with pytest
- **SQLite Database**: Simple database setup for development and testing

## 📋 Requirements

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pytest
- SQLite

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/rubendario90/rubendario90.git
cd rubendario90
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Create Message
**POST** `/api/messages`

Creates and processes a new chat message.

**Request Body**:
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hello, how can I help you today?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```

**Success Response** (200):
```json
{
  "status": "success",
  "data": {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hello, how can I help you today?",
    "timestamp": "2023-06-15T14:30:00",
    "sender": "system",
    "metadata": {
      "word_count": 6,
      "character_count": 32,
      "processed_at": "2023-06-15T14:30:01Z"
    }
  }
}
```

**Error Response** (400):
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FORMAT",
    "message": "Invalid message format",
    "details": "The field 'sender' must be 'user' or 'system'"
  }
}
```

#### 2. Get Messages by Session
**GET** `/api/messages/{session_id}`

Retrieves all messages for a specific session.

**Query Parameters**:
- `sender` (optional): Filter by sender ("user" or "system")
- `limit` (optional): Number of results per page (default: 50, max: 100)
- `offset` (optional): Number of results to skip (default: 0)

**Example**:
```
GET /api/messages/session-abcdef?sender=user&limit=10&offset=0
```

**Success Response** (200):
```json
{
  "status": "success",
  "data": [
    {
      "message_id": "msg-123456",
      "session_id": "session-abcdef",
      "content": "Hello, how can I help you today?",
      "timestamp": "2023-06-15T14:30:00",
      "sender": "system",
      "metadata": {
        "word_count": 6,
        "character_count": 32,
        "processed_at": "2023-06-15T14:30:01Z"
      }
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 50,
    "offset": 0,
    "has_next": false
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `INVALID_FORMAT` | Invalid message format or missing required fields |
| `INVALID_CONTENT` | Message contains inappropriate content |
| `DUPLICATE_MESSAGE` | Message with the same ID already exists |
| `INTERNAL_ERROR` | Internal server error |

## 🏗️ Project Structure

```
├── app/
│   ├── api/              # API endpoints
│   │   └── messages.py   # Message endpoints
│   ├── core/             # Core configuration
│   │   ├── database.py   # Database setup
│   │   └── exceptions.py # Custom exceptions
│   ├── models/           # Data models
│   │   ├── message.py    # SQLAlchemy models
│   │   └── schemas.py    # Pydantic schemas
│   ├── repositories/     # Data access layer
│   │   └── message_repository.py
│   ├── services/         # Business logic
│   │   └── message_service.py
│   └── main.py          # FastAPI application
├── tests/               # Test suite
│   ├── test_api.py      # API integration tests
│   ├── test_message_service.py  # Service unit tests
│   └── conftest.py      # Test configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_message_service.py -v
```

### Test Coverage

The project maintains high test coverage with:
- ✅ Unit tests for all service components
- ✅ Integration tests for API endpoints
- ✅ Error handling validation
- ✅ Content filtering tests
- ✅ Pagination and filtering tests

## 🔧 Configuration

### Environment Variables

The application can be configured using the following environment variables:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `DEBUG`: Enable debug mode (default: False)

### Content Filtering

The application includes basic content filtering for inappropriate words. The filter list can be customized in `app/services/message_service.py`:

```python
INAPPROPRIATE_WORDS = ['spam', 'abuse', 'hate', 'violent']
```

## 🚀 Deployment

### Using Docker (Optional Enhancement)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Database**: Replace SQLite with PostgreSQL or MySQL for production
2. **Authentication**: Implement JWT or OAuth2 authentication
3. **Rate Limiting**: Add rate limiting middleware
4. **Logging**: Configure structured logging
5. **Monitoring**: Add health checks and metrics

## 📈 Performance

- **Response Time**: < 100ms for message processing
- **Throughput**: Supports concurrent requests
- **Storage**: Efficient database queries with indexing
- **Memory**: Optimized for low memory usage

## 🛡️ Security Features

- Input validation and sanitization
- SQL injection prevention (SQLAlchemy ORM)
- Content filtering for inappropriate messages
- Error handling without information leakage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of a technical assessment and is for educational purposes.

## 👨‍💻 Contact

**Rubén Darío** - [rubendario90@gmail.com](mailto:rubendario90@gmail.com)

LinkedIn: [rudabaga90](https://www.linkedin.com/in/rudabaga90)

---

<p align="center">
  Built with ❤️ using FastAPI and Python
</p>

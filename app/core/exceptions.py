"""
Custom exceptions for the application.
"""

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class DuplicateMessageError(Exception):
    """Raised when a message with the same ID already exists."""
    pass

class MessageNotFoundError(Exception):
    """Raised when a requested message is not found."""
    pass
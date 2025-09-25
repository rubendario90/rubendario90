"""
Test configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
import os
import tempfile

@pytest.fixture(scope="function")
def db_session():
    # Create fresh engine for each test
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    # Create fresh engine for each test
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    def test_get_db():
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()
    
    # Override dependency
    app.dependency_overrides[get_db] = test_get_db
    
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    with TestClient(app) as c:
        yield c
    
    # Clean up
    app.dependency_overrides.clear()
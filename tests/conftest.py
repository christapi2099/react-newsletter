# tests/conftest.py
import pytest
import os
import json

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    os.environ['TESTING'] = 'true'
    os.environ['FIREBASE_CREDENTIALS_PATH'] = 'tests/mock_data/mock_firebase_credentials.json'
    os.environ['SENDGRID_API_KEY'] = 'mock_sendgrid_key'
    
@pytest.fixture
def mock_firebase_credentials(tmp_path):
    """Create mock Firebase credentials file"""
    creds = {
        "type": "service_account",
        "project_id": "mock-project",
        "private_key": "mock-key",
        "client_email": "mock@example.com"
    }
    
    creds_file = tmp_path / "mock_firebase_credentials.json"
    with open(creds_file, 'w') as f:
        json.dump(creds, f)
        
    return str(creds_file)
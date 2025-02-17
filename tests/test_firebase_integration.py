# tests/test_firebase_integration.py
import pytest
import asyncio
from src.extract_user_information import FirebaseManager, UserPreference
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_firestore():
    with patch('firebase_admin.firestore.client') as mock:
        yield mock

@pytest.mark.firebase
@pytest.mark.asyncio
class TestFirebaseManager:
    async def test_get_user_preferences(self, mock_firestore):
        # Mock user data
        mock_user_doc = MagicMock()
        mock_user_doc.exists = True
        mock_user_doc.to_dict.return_value = {
            'email': 'test@example.com',
            'name': 'Test User'
        }
        
        # Mock preferences data
        mock_pref_doc = MagicMock()
        mock_pref_doc.exists = True
        mock_pref_doc.to_dict.return_value = {
            'sport_preferences': ['basketball'],
            'notification_frequency': 'weekly'
        }
        
        # Setup mock Firestore
        mock_firestore.return_value.collection().document().get.side_effect = [
            mock_user_doc,
            mock_pref_doc
        ]
        
        # Test
        firebase_manager = FirebaseManager()
        user_pref = await firebase_manager.get_user_preferences("test_user_id")
        
        assert user_pref is not None
        assert user_pref.email == 'test@example.com'
        assert user_pref.sport_preferences == ['basketball']

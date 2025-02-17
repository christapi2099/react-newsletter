import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, List, Optional
import os
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class UserPreference:
    user_id: str
    email: str
    name: str
    sport_preferences: List[str]
    notification_frequency: str  # 'daily', 'weekly', 'monthly'
    last_newsletter_sent: datetime
    is_active: bool

class FirebaseManager:
    def __init__(self, credentials_path: str = None):
        """
        Initialize Firebase connection
        
        Args:
            credentials_path: Path to Firebase service account key JSON file
        """
        if not firebase_admin._apps:
            cred_path = credentials_path or os.getenv('FIREBASE_CREDENTIALS_PATH')
            if not cred_path:
                raise ValueError("Firebase credentials path not provided")
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
        self.users_ref = self.db.collection('users')
        self.preferences_ref = self.db.collection('newsletter_preferences')

    async def get_user_preferences(self, user_id: str) -> Optional[UserPreference]:
        """
        Retrieve user preferences from Firebase
        """
        try:
            user_doc = self.users_ref.document(user_id).get()
            if not user_doc.exists:
                return None

            user_data = user_doc.to_dict()
            pref_doc = self.preferences_ref.document(user_id).get()
            pref_data = pref_doc.to_dict() if pref_doc.exists else {}

            return UserPreference(
                user_id=user_id,
                email=user_data.get('email'),
                name=user_data.get('name'),
                sport_preferences=pref_data.get('sport_preferences', []),
                notification_frequency=pref_data.get('notification_frequency', 'weekly'),
                last_newsletter_sent=pref_data.get('last_newsletter_sent'),
                is_active=pref_data.get('is_active', True)
            )
        except Exception as e:
            print(f"Error fetching user preferences: {e}")
            return None

    async def get_active_subscribers(self) -> List[UserPreference]:
        """
        Get all active newsletter subscribers
        """
        try:
            # Query for active subscribers
            active_prefs = self.preferences_ref.where('is_active', '==', True).stream()
            
            subscribers = []
            for pref in active_prefs:
                user_id = pref.id
                user_doc = self.users_ref.document(user_id).get()
                
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    pref_data = pref.to_dict()
                    
                    subscribers.append(UserPreference(
                        user_id=user_id,
                        email=user_data.get('email'),
                        name=user_data.get('name'),
                        sport_preferences=pref_data.get('sport_preferences', []),
                        notification_frequency=pref_data.get('notification_frequency', 'weekly'),
                        last_newsletter_sent=pref_data.get('last_newsletter_sent'),
                        is_active=True
                    ))
            
            return subscribers
        except Exception as e:
            print(f"Error fetching active subscribers: {e}")
            return []

    async def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """
        Update user preferences in Firebase
        """
        try:
            # Update preferences
            self.preferences_ref.document(user_id).set(
                preferences,
                merge=True
            )
            return True
        except Exception as e:
            print(f"Error updating user preferences: {e}")
            return False

    async def update_last_sent_timestamp(self, user_id: str) -> bool:
        """
        Update the timestamp of last sent newsletter
        """
        try:
            self.preferences_ref.document(user_id).update({
                'last_newsletter_sent': datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error updating last sent timestamp: {e}")
            return False

    async def get_users_due_for_newsletter(self, frequency: str) -> List[UserPreference]:
        """
        Get users who are due for a newsletter based on their frequency preference
        """
        try:
            # Query for active users with matching frequency
            query = self.preferences_ref.where('is_active', '==', True)\
                                     .where('notification_frequency', '==', frequency)
            
            users_due = []
            for pref in query.stream():
                last_sent = pref.get('last_newsletter_sent')
                if self._is_due_for_newsletter(last_sent, frequency):
                    user_pref = await self.get_user_preferences(pref.id)
                    if user_pref:
                        users_due.append(user_pref)
            
            return users_due
        except Exception as e:
            print(f"Error fetching users due for newsletter: {e}")
            return []

    def _is_due_for_newsletter(self, last_sent: datetime, frequency: str) -> bool:
        """
        Check if a user is due for a newsletter based on their frequency preference
        """
        if not last_sent:
            return True
            
        now = datetime.now()
        delta = now - last_sent
        
        if frequency == 'daily':
            return delta.days >= 1
        elif frequency == 'weekly':
            return delta.days >= 7
        elif frequency == 'monthly':
            return delta.days >= 30
        return False

# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize Firebase manager
        firebase_manager = FirebaseManager()
        
        # Get all active subscribers
        subscribers = await firebase_manager.get_active_subscribers()
        
        # Get users due for daily newsletter
        daily_users = await firebase_manager.get_users_due_for_newsletter('daily')
        
        # Example of getting specific user preferences
        user_pref = await firebase_manager.get_user_preferences("user123")
        
        # Example of updating preferences
        new_preferences = {
            'sport_preferences': ['basketball', 'football'],
            'notification_frequency': 'weekly'
        }
        await firebase_manager.update_user_preferences("user123", new_preferences)

    # Run the async main function
    import asyncio
    asyncio.run(main())
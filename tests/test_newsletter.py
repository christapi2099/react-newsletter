# tests/test_newsletter.py
import pytest
from src.newsletter import NewsletterGenerator
from unittest.mock import Mock, patch
import json

@pytest.fixture
def mock_sendgrid():
    with patch('sendgrid.SendGridAPIClient') as mock:
        yield mock

@pytest.mark.newsletter
class TestNewsletterGenerator:
    def test_process_scraped_content(self):
        generator = NewsletterGenerator("mock_api_key")
        content = """
        <h1>NBA Updates</h1>
        <p>Latest basketball news and scores.</p>
        """
        result = generator.process_scraped_content(content)
        assert result is not None
        assert 'title' in result
        assert 'text' in result
        
    def test_generate_newsletter_content(self):
        generator = NewsletterGenerator("mock_api_key")
        sport = "basketball"
        scraped_data = ["<h1>NBA News</h1><p>Test content</p>"]
        
        html_content = generator.generate_newsletter_content(sport, scraped_data)
        assert "basketball" in html_content.lower()
        assert "NBA News" in html_content
        
    def test_send_newsletter(self, mock_sendgrid):
        generator = NewsletterGenerator("mock_api_key")
        mock_sendgrid.return_value.send.return_value = Mock(status_code=202)
        
        result = generator.send_newsletter(
            "test@example.com",
            "<html>Test newsletter</html>",
            "basketball"
        )
        assert result == True



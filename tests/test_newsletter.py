# tests/test_newsletter.py
import pytest
from src.newsletter import NewsletterGenerator
from unittest.mock import Mock, patch, MagicMock
import json

@pytest.fixture
def mock_article():
    with patch('newspaper.Article') as mock:
        article = Mock()
        article.title = "NBA Updates"
        article.text = "Latest basketball news and scores"
        article.summary = "Basketball news summary"
        article.keywords = ["NBA", "basketball"]
        article.publish_date = "2025-02-17"
        
        # Configure the mock Article class
        mock.return_value = article
        yield article

@pytest.fixture
def mock_sendgrid():
    with patch('sendgrid.SendGridAPIClient') as mock:
        client = Mock()
        response = Mock()
        response.status_code = 202
        client.send.return_value = response
        mock.return_value = client
        yield mock

class TestNewsletterGenerator:
    def test_process_scraped_content(self, mock_article):
        with patch('newspaper.Article') as MockArticle:
            MockArticle.return_value = mock_article
            
            generator = NewsletterGenerator("mock_api_key")
            content = """
            <h1>NBA Updates</h1>
            <p>Latest basketball news and scores.</p>
            """
            result = generator.process_scraped_content(content)
            
            assert result is not None
            assert result['title'] == "NBA Updates"
            assert "basketball news" in result['text'].lower()
            
    def test_generate_newsletter_content(self, mock_article):
        with patch('newspaper.Article') as MockArticle:
            MockArticle.return_value = mock_article
            
            generator = NewsletterGenerator("mock_api_key")
            sport = "basketball"
            scraped_data = ["<h1>NBA News</h1><p>Test content</p>"]

            # Mock the process_scraped_content method
            generator.process_scraped_content = MagicMock(return_value={
                'title': 'NBA News',
                'text': 'Test content',
                'summary': 'Test summary',
                'keywords': ['NBA', 'basketball'],
                'publish_date': '2025-02-17'
            })
            
            html_content = generator.generate_newsletter_content(sport, scraped_data)
            
            assert "basketball" in html_content.lower()
            assert "NBA News" in html_content
            assert "Test content" in html_content
            
    @patch('sendgrid.Mail')
    def test_send_newsletter(self, mock_mail, mock_sendgrid):
        generator = NewsletterGenerator("mock_api_key")
        
        # Configure mock mail
        mock_mail.return_value = Mock()
        
        # Configure mock SendGrid client response
        mock_sendgrid.return_value.send.return_value.status_code = 202
        
        result = generator.send_newsletter(
            "test@example.com",
            "<html>Test newsletter</html>",
            "basketball"
        )
        
        assert result == True
        mock_sendgrid.return_value.send.assert_called_once()
        
    def test_generate_newsletter_without_content(self):
        generator = NewsletterGenerator("mock_api_key")
        sport = "basketball"
        scraped_data = []
        
        html_content = generator.generate_newsletter_content(sport, scraped_data)
        assert "No updates available" in html_content
        
    def test_process_invalid_content(self, mock_article):
        mock_article.download.side_effect = Exception("Download failed")
        
        with patch('newspaper.Article') as MockArticle:
            MockArticle.return_value = mock_article
            
            generator = NewsletterGenerator("mock_api_key")
            content = "Invalid content"
            result = generator.process_scraped_content(content)
            
            assert result is None
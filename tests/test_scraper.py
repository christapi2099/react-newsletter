# tests/test_scraper.py
import pytest
import responses
from src.scraper import scrape_and_add_dynamic, validate_url, scrape_with_rate_limit
from bs4 import BeautifulSoup
import json

@pytest.fixture
def mock_html_content():
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Sports News</h1>
            <p>Test content for sports news.</p>
        </body>
    </html>
    """

@pytest.mark.scraper
class TestScraper:
    @responses.activate
    def test_scrape_valid_url(self, mock_html_content):
        # Setup mock response
        test_url = "https://example.com/sports"
        responses.add(
            responses.GET,
            test_url,
            body=mock_html_content,
            status=200
        )
        
        # Test scraping
        result = scrape_with_rate_limit([test_url], delay=0)
        assert len(result) == 1
        assert "Sports News" in result[0].text
        
    def test_validate_url(self):
        assert validate_url("https://example.com") == True
        assert validate_url("not_a_url") == False
        
    @pytest.mark.slow
    def test_rate_limiting(self, mock_html_content):
        urls = ["https://example.com/1", "https://example.com/2"]
        for url in urls:
            responses.add(responses.GET, url, body=mock_html_content, status=200)
            
        import time
        start = time.time()
        results = scrape_with_rate_limit(urls, delay=1)
        duration = time.time() - start
        
        assert duration >= 1  # Should take at least 1 second due to rate limiting

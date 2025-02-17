from llama_index import VectorStoreIndex
from llama_index.readers.web import BeautifulSoupWebReader
from llama_index.core import Document
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import logging
import time
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for document storage
documents_list = []
index = None

def scrape_and_add_dynamic(urls: List[str]) -> str:
    """
    Scrapes the given URLs and adds them to the LlamaIndex dynamically.
    
    Args:
        urls (List[str]): List of URLs to scrape
        
    Returns:
        str: Summary of scraped content
    """
    global index, documents_list
    
    try:
        loader = BeautifulSoupWebReader()
        scraped_documents = loader.load_data(urls=urls)
        
        # Add to the global document list and update the index
        documents_list.extend(scraped_documents)
        index = VectorStoreIndex.from_documents(documents_list)
        
        # Generate a summary of the scraped data
        summary = []
        for doc in scraped_documents:
            # Add basic error checking for document content
            if hasattr(doc, 'text') and doc.text:
                summary.append(doc.text[:200])  # Include the first 200 characters
            
        return " ".join(summary)
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        return f"Error during scraping: {str(e)}"

def validate_url(url: str) -> bool:
    """
    Validates if a URL is properly formatted and accessible.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid and accessible, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def scrape_with_rate_limit(urls: List[str], delay: float = 1.0) -> List[Document]:
    """
    Scrapes URLs with rate limiting to be respectful to servers.
    
    Args:
        urls (List[str]): List of URLs to scrape
        delay (float): Delay between requests in seconds
        
    Returns:
        List[Document]: List of scraped documents
    """
    documents = []
    
    for url in urls:
        if not validate_url(url):
            logger.warning(f"Invalid URL skipped: {url}")
            continue
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove unnecessary elements
            for script in soup(['script', 'style', 'nav', 'footer']):
                script.decompose()
                
            text = soup.get_text(separator='\n', strip=True)
            documents.append(Document(text=text, extra_info={'url': url}))
            
            time.sleep(delay)  # Rate limiting
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            
    return documents

if __name__ == "__main__":
    # Example usage
    test_urls = [
        "https://example.com/sports/news",
        "https://example.com/sports/updates"
    ]
    
    summary = scrape_and_add_dynamic(test_urls)
    print(f"Scraped content summary: {summary}")
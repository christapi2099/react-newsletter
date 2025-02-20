from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.schema import Document
from llama_index.readers.web import BeautifulSoupWebReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import logging
import time
from urllib.parse import urlparse
import os
from gen_urls import generate_urls_from_query

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
        # Print the URLs we're trying to scrape (for debugging)
        print(urls)
        
        # IMPORTANT: Configure to use local Hugging Face embeddings with Settings
        embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
        Settings.embed_model = embed_model
        
        # Use rate-limited scraping instead of BeautifulSoupWebReader for more control
        scraped_documents = scrape_with_rate_limit(urls, delay=1.0)
        
        if not scraped_documents:
            return "No content was successfully scraped from the provided URLs."
        
        # Add to the global document list and update the index
        documents_list.extend(scraped_documents)
        
        # Use settings-based approach instead of service_context
        index = VectorStoreIndex.from_documents(documents_list)
        
        # Generate a summary of the scraped data
        summary = []
        for doc in scraped_documents:
            if hasattr(doc, 'text') and doc.text:
                summary.append(doc.text[:200])  # Include the first 200 characters
        
        if not summary:
            return "Content was scraped but no text was extracted."
            
        return " ".join(summary)
        
    except Exception as e:
        logger.error(f"Error during scraping: \n******\n{str(e)}\n******")
        return f"Error during scraping: \n******\n{str(e)}\n******"

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
            response = requests.get(
                url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove unnecessary elements
            for script in soup(['script', 'style', 'nav', 'footer']):
                script.decompose()
                
            text = soup.get_text(separator='\n', strip=True)
            if text:
                documents.append(Document(text=text, extra_info={'url': url}))
            else:
                logger.warning(f"No text content extracted from {url}")
            
            time.sleep(delay)  # Rate limiting
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing {url}: {e}")
            
    return documents

if __name__ == "__main__":
    # Example usage
    test_urls = generate_urls_from_query('baseball')
    print(test_urls)
    summary = scrape_and_add_dynamic(test_urls)
    print(f"Scraped content summary: {summary}")
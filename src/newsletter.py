#Contains all the code to generate dynamic newsletter based on user cateogry. 

from typing import List, Dict
import os
from datetime import datetime
from newspaper import Article
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
from jinja2 import Template
import json

class NewsletterGenerator:
    def __init__(self, sendgrid_api_key: str):
        self.sg = SendGridAPIClient(sendgrid_api_key)
        
    def process_scraped_content(self, raw_content: str) -> Dict:
        """
        Process scraped content into structured data for the newsletter
        """
        try:
            # Use newspaper3k to extract article content
            article = Article(url='')
            article.download()
            article.parse()
            
            return {
                'title': article.title,
                'text': article.text[:500],  # First 500 chars for preview
                'summary': article.summary,
                'keywords': article.keywords,
                'publish_date': article.publish_date
            }
        except Exception as e:
            print(f"Error processing content: {e}")
            return None

    def generate_newsletter_content(self, sport_preference: str, scraped_data: List[str]) -> str:
        """
        Generate newsletter HTML content based on sport preference and scraped data
        """
        # Basic newsletter template
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ sport }} Newsletter</title>
        </head>
        <body>
            <h1>{{ sport }} News Update</h1>
            <p>Here are the latest updates in {{ sport }}:</p>
            
            {% for article in articles %}
            <div class="article">
                <h2>{{ article.title }}</h2>
                <p>{{ article.summary }}</p>
                {% if article.keywords %}
                <p>Topics: {{ article.keywords|join(', ') }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </body>
        </html>
        """
        
        # Process all scraped content
        processed_articles = []
        for content in scraped_data:
            if processed := self.process_scraped_content(content):
                processed_articles.append(processed)
        
        # Generate HTML using Jinja2
        template = Template(template_str)
        html_content = template.render(
            sport=sport_preference,
            articles=processed_articles,
            date=datetime.now().strftime("%Y-%m-%d")
        )
        
        return html_content

    def send_newsletter(self, recipient_email: str, html_content: str, sport: str) -> bool:
        """
        Send the newsletter using SendGrid
        """
        try:
            message = Mail(
                from_email='your-verified-sender@domain.com',
                to_emails=recipient_email,
                subject=f'Your {sport} Newsletter Update',
                html_content=html_content
            )
            
            response = self.sg.send(message)
            return response.status_code == 202
            
        except Exception as e:
            print(f"Error sending newsletter: {e}")
            return False

    def save_subscriber_preference(self, email: str, sport_preference: str) -> None:
        """
        Save subscriber preferences to a JSON file
        """
        try:
            preferences = {}
            if os.path.exists('subscriber_preferences.json'):
                with open('subscriber_preferences.json', 'r') as f:
                    preferences = json.load(f)
            
            preferences[email] = sport_preference
            
            with open('subscriber_preferences.json', 'w') as f:
                json.dump(preferences, f)
                
        except Exception as e:
            print(f"Error saving preferences: {e}")

# Usage example:
if __name__ == "__main__":
    # Initialize the newsletter generator
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    newsletter_gen = NewsletterGenerator(SENDGRID_API_KEY)
    
    # Example user preference and scraped data
    sport = "basketball"
    email = "subscriber@example.com"
    
    # Get URLs from your existing generate_urls_from_query function
    urls = generate_urls_from_query(sport)
    
    # Use your existing scraper to get content
    scraped_content = scrape_and_add_dynamic(urls)
    
    # Generate and send newsletter
    html_content = newsletter_gen.generate_newsletter_content(sport, [scraped_content])
    if newsletter_gen.send_newsletter(email, html_content, sport):
        print(f"Newsletter sent successfully to {email}")
        newsletter_gen.save_subscriber_preference(email, sport)
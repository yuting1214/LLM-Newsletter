import os
from config.settings import load_env_variables
from services.content_service import generate_newsletter
from services.email_service import send_email
from services.pdf_service import create_pdf
from utils.logger import get_logger
from datetime import datetime

# Load environment variables
load_env_variables()

# Configure logging
logger = get_logger(__name__)

def main():
    logger.info("Starting newsletter generation process...")
    
    # Define the prompt for GPT-4
    current_month = datetime.now().strftime("%B %Y")
    prompt = f"Create a monthly newsletter for {current_month} for our subscribers. Highlight the latest updates, interesting articles, and upcoming events."
    
    # Generate newsletter content
    newsletter_content = generate_newsletter(prompt)
    if not newsletter_content:
        logger.error("Failed to generate newsletter content.")
        return
    
    # Create a PDF from the content (optional)
    pdf_path = os.path.join("pdfs", "newsletter.pdf")
    # create_pdf(newsletter_content, output_path=pdf_path)
    
    # Define email subject and body
    subject = f"Your Monthly Newsletter - {current_month}"
    body = f"Hi there,\n\nPlease find the latest updates in our newsletter below.\n\n{newsletter_content}"
    
    # Send the email with PDF attachment
    recipient = os.getenv("RECIPIENT_EMAIL")
    if recipient:
        send_email(subject, body, recipient, attachment_path=None)
    else:
        logger.error("No recipient email found in environment variables.")

    logger.info("Newsletter generation process completed successfully.")

if __name__ == "__main__":
    main()

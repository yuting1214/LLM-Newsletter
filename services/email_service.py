import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from utils.logger import get_logger

logger = get_logger(__name__)

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(subject, body, recipient, attachment_path=None):
    """
    Sends an email with the specified subject, body, and optional attachment.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        recipient (str): Recipient's email address.
        attachment_path (str, optional): Path to the attachment. Defaults to None.
    """
    try:
        # Configure the email
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        # Add attachment if provided
        if attachment_path and os.path.isfile(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(attachment_path)}"',
            )
            msg.attach(part)
        
        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
            logger.info(f"Email sent successfully to {recipient}.")
    except Exception as e:
        logger.error(f"Error sending email to {recipient}: {e}")

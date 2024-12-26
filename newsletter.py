import os
import smtplib
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# Validate environment variables
required_env_vars = ['OPENAI_API_KEY', 'GMAIL_USER', 'GMAIL_APP_PASSWORD', 'RECIPIENT_EMAIL']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

def generate_newsletter(prompt="Create a monthly newsletter for our subscribers highlighting the latest updates and interesting articles."):
    """
    Generates newsletter content using OpenAI's GPT-4 API based on the provided prompt.

    Args:
        prompt (str): The prompt to send to the GPT-4 model.

    Returns:
        str: Generated newsletter content.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates engaging newsletter content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
        )
        content = response.choices[0].message['content'].strip()
        return content
    except Exception as e:
        print(f"Error generating newsletter: {e}")
        return None

def send_email(subject, body, from_email, to_email, attachment_path=None, smtp_server='smtp.gmail.com', smtp_port=587):
    """
    Sends an email with the specified subject and body to the recipient. Optionally attaches a file.

    Args:
        subject (str): Subject of the email.
        body (str): HTML body of the email.
        from_email (str): Sender's email address.
        to_email (str): Recipient's email address.
        attachment_path (str, optional): Path to the file to attach. Defaults to None.
        smtp_server (str, optional): SMTP server address. Defaults to 'smtp.gmail.com'.
        smtp_port (int, optional): SMTP server port. Defaults to 587.
    """
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Attach the email body
        msg.attach(MIMEText(body, 'html'))

        # Attach a file if provided
        if attachment_path and os.path.isfile(attachment_path):
            filename = os.path.basename(attachment_path)
            with open(attachment_path, 'rb') as attachment_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"',
            )
            msg.attach(part)

        # Connect to Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, GMAIL_APP_PASSWORD)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def create_pdf(newsletter_content, output_path='assets/newsletter.pdf'):
    """
    Creates a PDF file from the newsletter content.

    Args:
        newsletter_content (str): The newsletter content to include in the PDF.
        output_path (str, optional): Path to save the generated PDF. Defaults to 'assets/newsletter.pdf'.
    """
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Split content into lines and add to PDF
        for line in newsletter_content.split('\n'):
            pdf.multi_cell(0, 10, line)
        
        pdf.output(output_path)
        print(f"PDF successfully created at {output_path}")
    except ImportError:
        print("fpdf library is not installed. Install it using 'pip install fpdf'")
    except Exception as e:
        print(f"Error creating PDF: {e}")

def main():
    """
    Main function to generate the newsletter and send it via email.
    """
    # Define the prompt for GPT-4
    current_month = datetime.now().strftime("%B %Y")
    prompt = f"Create a monthly newsletter for {current_month} for our subscribers. Highlight the latest updates, interesting articles, and upcoming events."

    # Generate newsletter content
    newsletter_content = generate_newsletter(prompt)
    if not newsletter_content:
        print("Failed to generate newsletter content.")
        return

    # Optional: Create a PDF of the newsletter
    # Uncomment the following lines if you wish to include a PDF attachment
    # pdf_path = "assets/newsletter.pdf"
    # create_pdf(newsletter_content, output_path=pdf_path)

    # Define email subject
    subject = f"Your Monthly Newsletter - {current_month}"

    # Load HTML template
    template_path = os.path.join('assets', 'newsletter_template.html')
    if os.path.isfile(template_path):
        with open(template_path, 'r', encoding='utf-8') as template_file:
            html_template = template_file.read()
    else:
        print(f"HTML template not found at {template_path}. Using default formatting.")
        html_template = """
        <html>
            <head>
                <style>
                    body {font-family: Arial, sans-serif; line-height: 1.6;}
                    h2 {color: #333333;}
                </style>
            </head>
            <body>
                <h2>Monthly Newsletter - {month}</h2>
                <p>{content}</p>
                <br>
                <p>Best regards,<br>Your Company Team</p>
            </body>
        </html>
        """

    # Format the HTML content
    if '{month}' in html_template and '{content}' in html_template:
        html_body = html_template.format(month=current_month, content=newsletter_content.replace('\n', '<br>'))
    else:
        # If template placeholders are missing, use default formatting
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{font-family: Arial, sans-serif; line-height: 1.6;}}
                    h2 {{color: #333333;}}
                </style>
            </head>
            <body>
                <h2>Monthly Newsletter - {current_month}</h2>
                <p>{newsletter_content.replace('\n', '<br>')}</p>
                <br>
                <p>Best regards,<br>Your Company Team</p>
            </body>
        </html>
        """

    # Path to the PDF attachment (optional)
    # Uncomment the following line if you created a PDF
    # attachment_path = "assets/newsletter.pdf"

    # Send the email
    send_email(
        subject=subject,
        body=html_body,
        from_email=GMAIL_USER,
        to_email=RECIPIENT_EMAIL,
        # attachment_path=attachment_path  # Uncomment if attaching a PDF
    )

if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv

def load_env_variables():
    """Loads environment variables from the .env file."""
    load_dotenv()
    required_vars = ["OPENAI_API_KEY", "GMAIL_USER", "GMAIL_APP_PASSWORD", "RECIPIENT_EMAIL"]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")

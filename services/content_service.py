from openai import OpenAI
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_newsletter(prompt):
    """
    Generates newsletter content using OpenAI's GPT-4 API.

    Args:
        prompt (str): The prompt to generate content for the newsletter.

    Returns:
        str: The generated content.
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates engaging newsletter content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        logger.info("Newsletter content generated successfully.")
        return content
    except Exception as e:
        logger.error(f"Error generating newsletter content: {e}")
        return None

from fpdf import FPDF
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def create_pdf(content, output_path):
    """
    Creates a PDF that supports Unicode characters using FPDF with a Unicode-compatible font.

    Args:
        content (str): The text content for the PDF.
        output_path (str): The path where the PDF will be saved.
    """
    try:
        # Directory for fonts
        font_dir = os.path.join("assets", "fonts")
        os.makedirs(font_dir, exist_ok=True)

        # Path to the DejaVuSans.ttf font
        font_path = os.path.join(font_dir, "DejaVuSans.ttf")
        # Create a new FPDF instance
        pdf = FPDF()
        pdf.add_page()

        # Register and set the Unicode-compatible font
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)

        # Write content to the PDF
        for line in content.split("\n"):
            pdf.multi_cell(0, 10, line)

        # Save the PDF
        pdf.output(output_path)
        logger.info(f"PDF with Unicode support created successfully at {output_path}.")
    except Exception as e:
        logger.error(f"Error creating Unicode PDF: {e}")

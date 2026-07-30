"""
Hybrid Payment Extractor

Priority:
1. Gemini Vision
2. EasyOCR (Fallback)
"""

from gemini_ocr import process_payment
from ocr_engine import process_receipt


def extract_payment_data(image):
    """
    Extract payment information using Gemini first.
    Falls back to EasyOCR if Gemini fails.
    """

    result = process_payment(image)

    if result.get("success"):
        return result

    return process_receipt(image)
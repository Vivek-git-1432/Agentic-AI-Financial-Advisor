"""
Hybrid Payment Extractor

Priority:
1. Gemini Vision
2. EasyOCR (Fallback)
"""

from gemini_ocr import process_payment
from ocr_engine import process_receipt


def extract_payment_data(image):

    print("\n========== TRYING GEMINI ==========")

    result = process_payment(image)

    print("Gemini Result:")
    print(result)

    if result.get("success"):
        print("✅ Gemini Success")
        return result

    print("❌ Gemini Failed")
    print("Error:", result.get("error"))

    print("➡️ Falling back to EasyOCR")

    return process_receipt(image)
import easyocr
import cv2
import numpy as np
import re

from PIL import Image
from datetime import datetime

# --------------------------------------------------
# EasyOCR Initialization
# --------------------------------------------------

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

# --------------------------------------------------
# Image Preprocessing
# --------------------------------------------------

def preprocess_image(image: Image.Image):
    """
    Preprocess the uploaded image to improve OCR accuracy.
    """

    # Convert PIL image to NumPy array
    image = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    # Upscale image
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Remove noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Improve text visibility
    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return gray

# --------------------------------------------------
# OCR Text Extraction
# --------------------------------------------------

def extract_text(image: Image.Image):
    """
    Extract all readable text from the preprocessed image.
    Returns:
        text (str): OCR extracted text
        results (list): EasyOCR raw detection results
    """

    processed = preprocess_image(image)

    results = reader.readtext(
        processed,
        detail=1
    )

    text_lines = []

    for result in results:
        text_lines.append(result[1])

    text = "\n".join(text_lines)

    return text, results

# --------------------------------------------------
# Amount Detection
# --------------------------------------------------

def detect_amount(text: str):
    """
    Detect the transaction amount from OCR text.
    Returns an integer amount if found, otherwise None.
    """

    # Normalize common OCR mistakes
    cleaned = text.replace("₹", "Rs ")
    cleaned = cleaned.replace("R", "Rs ")

    patterns = [
        r'Rs\s*([0-9,]+(?:\.\d{2})?)',
        r'INR\s*([0-9,]+(?:\.\d{2})?)',
        r'amount\s*[:\-]?\s*([0-9,]+(?:\.\d{2})?)',
        r'paid\s*[:\-]?\s*([0-9,]+(?:\.\d{2})?)'
    ]

    for pattern in patterns:
        match = re.search(pattern, cleaned, re.IGNORECASE)

        if match:
            amount = match.group(1).replace(",", "")

            try:
                return int(float(amount))
            except ValueError:
                continue

    return None


# --------------------------------------------------
# Recipient Detection
# --------------------------------------------------

def detect_recipient(text: str):
    """
    Detect the recipient's name from OCR text.
    """

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    keywords = [
        "To",
        "To:",
        "Paid to",
        "Sent to"
    ]

    for i, line in enumerate(lines):

        for keyword in keywords:

            if line.lower().startswith(keyword.lower()):

                # Example:
                # To DILEEP GL
                parts = line.split(keyword, 1)

                if len(parts) > 1 and parts[1].strip():
                    return parts[1].strip()

                # Example:
                # To
                # DILEEP GL
                if i + 1 < len(lines):
                    return lines[i + 1]

    return "Unknown"

# --------------------------------------------------
# Payment App Detection
# --------------------------------------------------

def detect_payment_app(text: str):
    """
    Detect the payment application used for the transaction.
    """

    text = text.lower()

    payment_apps = {
        "phonepe": "PhonePe",
        "google pay": "Google Pay",
        "gpay": "Google Pay",
        "paytm": "Paytm",
        "bhim": "BHIM",
        "amazon pay": "Amazon Pay",
        "cred": "CRED",
        "mobikwik": "MobiKwik"
    }

    for keyword, app_name in payment_apps.items():
        if keyword in text:
            return app_name

    return "Unknown"


# --------------------------------------------------
# Date Detection
# --------------------------------------------------

def detect_date(text: str):
    """
    Detect transaction date from OCR text.
    Returns date in YYYY-MM-DD format.
    """

    patterns = [
        r'(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})',
        r'(\d{2}/\d{2}/\d{4})',
        r'(\d{2}-\d{2}-\d{4})'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            date_str = match.group(1)

            for fmt in ("%d %b %Y", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue

    return datetime.today().strftime("%Y-%m-%d")


# --------------------------------------------------
# Category Detection
# --------------------------------------------------

def detect_category(text: str):
    """
    Predict expense category based on merchant or keywords.
    """

    text = text.lower()

    category_map = {
        "zomato": "Food",
        "swiggy": "Food",
        "dominos": "Food",
        "pizza hut": "Food",

        "uber": "Travel",
        "ola": "Travel",
        "irctc": "Travel",

        "amazon": "Shopping",
        "flipkart": "Shopping",
        "myntra": "Shopping",
        "dmart": "Shopping",
        "reliance": "Shopping",

        "medical": "Medical",
        "pharmacy": "Medical",

        "electricity": "Bills",
        "water": "Bills",
        "gas": "Bills"
    }

    for keyword, category in category_map.items():
        if keyword in text:
            return category

    return "Others"


# --------------------------------------------------
# Main Receipt Processing Function
# --------------------------------------------------

def process_receipt(image: Image.Image):
    """
    Process a payment screenshot using EasyOCR.
    Returns structured transaction data.
    """

    try:

        text, results = extract_text(image)

        receipt = {
            "amount": detect_amount(text),
            "recipient": detect_recipient(text),
            "payment_app": detect_payment_app(text),
            "date": detect_date(text),
            "category": detect_category(text),
            "ocr_text": text,
            "success": True
        }

        return receipt

    except Exception as e:

        return {
            "success": False,
            "amount": None,
            "recipient": "Unknown",
            "payment_app": "Unknown",
            "date": "",
            "category": "Others",
            "ocr_text": "",
            "error": str(e)
        }
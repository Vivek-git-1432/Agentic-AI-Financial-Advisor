import os
import json
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")
    
client = genai.Client(
    api_key=api_key
)
PROMPT = """
You are an expert financial document extraction AI.

Analyze the uploaded UPI payment screenshot.

Extract ONLY these fields and return ONLY valid JSON.

{
    "amount": 0,
    "recipient": "",
    "payment_app": "",
    "date": "",
    "category": ""
}

Rules:

1. amount
- Only transaction amount
- Integer only
- Ignore phone numbers
- Ignore account numbers
- Ignore UTR
- Ignore reference IDs
- Ignore transaction IDs

2. recipient
- Person or merchant receiving money

3. payment_app
Must be one of:
PhonePe
Google Pay
Paytm
Amazon Pay
BHIM
Unknown

4. date
Return in YYYY-MM-DD format.
If unavailable return "".

5. category
Choose ONLY one:

Food
Shopping
Travel
Bills
Medical
Entertainment
Education
Fuel
Transfer
Others

Return ONLY JSON.
"""


def process_payment(image: Image.Image):
    print("############################")
    print("GEMINI FUNCTION CALLED")
    print("############################")
    
    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[PROMPT, image]
        )

        text = response.text.strip()

        text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(text)

        return {
            "success": True,
            "amount": int(data.get("amount", 0)),
            "recipient": data.get("recipient", "Unknown"),
            "payment_app": data.get("payment_app", "Unknown"),
            "date": data.get("date", ""),
            "category": data.get("category", "Others")
        }

    except Exception as e:

        return {
            "success": False,
            "amount": 0,
            "recipient": "Unknown",
            "payment_app": "Unknown",
            "date": "",
            "category": "Others",
            "error": str(e)
        }
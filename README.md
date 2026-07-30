# 💰 Agentic AI Financial Advisor

An intelligent AI-powered financial management web application built with **Streamlit**, **Google Gemini Vision**, **EasyOCR**, **LangChain**, and **Groq LLM**. The application automatically extracts expense details from payment screenshots, tracks spending, and provides personalized AI-driven financial insights.

---

# 🚀 Features

## 📷 AI-Powered OCR Expense Detection
- Upload payment screenshots
- Extract expense details using **Google Gemini Vision** and **EasyOCR**
- Automatically detect payment amount and expense category
- Save expenses directly into the dashboard

## 🤖 Agentic AI Financial Advisor
- Financial assistant powered by **Groq LLM**
- Personalized financial recommendations
- Budget planning assistance
- Savings suggestions
- Financial health analysis
- Intelligent answers to finance-related questions

## 📊 Interactive Dashboard
- Total expense tracking
- Budget utilization monitoring
- Expense distribution visualization
- Monthly expense trends
- Financial Health Score
- AI-powered smart spending alerts

## 📝 Expense Management
- Automatic expense detection
- Manual expense entry
- Edit existing expenses
- Delete expenses
- Expense history management

## 👤 User Profile
- Personal profile management
- Financial information management
- Profile completion tracking

## 📑 AI Financial Reports
- AI-generated financial summaries
- Spending behavior analysis
- Budget improvement suggestions
- Personalized financial recommendations

---

# 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini Vision API
- Groq LLM
- LangChain
- EasyOCR
- OpenCV
- SQLite
- Pandas
- Matplotlib
- Pillow

---

# 📂 Project Structure

```text
Agentic-AI-Financial-Advisor/
│── app.py
│── account.py
│── extractor.py
│── gemini_ocr.py
│── ocr_engine.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Vivek-git-1432/Agentic-AI-Financial-Advisor.git
```

Go to the project folder

```bash
cd Agentic-AI-Financial-Advisor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🔑 API Configuration

## Google Gemini API

Create a `.env` file (for local development only):

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

For **Streamlit Community Cloud**, add your API key in **App Settings → Secrets** instead of uploading the `.env` file.

## Groq API

Enter your **Groq API Key** in the application's sidebar when running the app.

---

# 📷 Application Workflow

1. Upload a payment screenshot.
2. Gemini Vision and EasyOCR extract the expense details.
3. AI identifies the amount and expense category.
4. Expense is automatically stored in the database.
5. Dashboard updates instantly.
6. Groq-powered AI analyzes spending patterns.
7. Personalized financial insights and recommendations are generated.

---

# 🌟 Future Enhancements

- Secure user authentication
- Multi-user support
- Cloud database integration
- Export financial reports as PDF
- Voice-enabled AI financial assistant
- Mobile application support

---

# 👨‍💻 Developed By

**Vivek G L**

AI & Agentic AI Developer

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
import sqlite3
from datetime import datetime
from langchain_groq import ChatGroq

plt.style.use("dark_background")

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

conn = sqlite3.connect(
    "expenses.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    amount INTEGER,
    category TEXT,
    date TEXT
)
""")

conn.commit()


# ---------------------------------------------------
# SESSION
# ---------------------------------------------------

if "budget" not in st.session_state:
    st.session_state.budget = 15000

if "profile" not in st.session_state:

    st.session_state.profile = {
        "name": "",
        "age": 18,
        "occupation": "",
        "income": 0,
        "goal": ""
    }
if "show_report" not in st.session_state:

    st.session_state.show_report = False

if "report_content" not in st.session_state:

    st.session_state.report_content = ""

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_sql_query(
    "SELECT * FROM expenses",
    conn
)

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------

total_expense = 0

if not df.empty:
    total_expense = df["amount"].sum()

# Financial score

if total_expense <= 5000:
    financial_score = 90

elif total_expense <= 10000:
    financial_score = 75

elif total_expense <= 20000:
    financial_score = 60

else:
    financial_score = 40

# Budget status

budget_status = "Under Control"

if total_expense > st.session_state.budget:
    budget_status = "Budget Exceeded"

    # Top spending category

top_category = "No Data"

if not df.empty:

    category_totals = df.groupby(
        "category"
    )["amount"].sum()

    top_category = category_totals.idxmax()

# ---------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------

def detect_category(text):

    text = text.lower()

    # Food
    food_keywords = [
        "food",
        "restaurant",
        "swiggy",
        "zomato",
        "cafe",
        "hotel"
    ]

    # Shopping
    shopping_keywords = [
        "amazon",
        "flipkart",
        "shopping",
        "myntra",
        "store"
    ]

    # Travel
    travel_keywords = [
        "uber",
        "ola",
        "travel",
        "bus",
        "train",
        "flight"
    ]

    # Entertainment
    entertainment_keywords = [
        "movie",
        "netflix",
        "prime",
        "spotify"
    ]

    # Bills
    bill_keywords = [
        "electricity",
        "water",
        "recharge",
        "bill",
        "wifi"
    ]

    for word in food_keywords:
        if word in text:
            return "Food"

    for word in shopping_keywords:
        if word in text:
            return "Shopping"

    for word in travel_keywords:
        if word in text:
            return "Travel"

    for word in entertainment_keywords:
        if word in text:
            return "Entertainment"

    for word in bill_keywords:
        if word in text:
            return "Bills"

    return "Transfer"


def get_ai_advice(category):

    if not df.empty:

        category_totals = df.groupby(
            "category"
        )["amount"].sum()

        top_category = category_totals.idxmax()

        top_amount = category_totals.max()

    else:

        top_category = category
        top_amount = 0

    # Personalized advice

    if top_category == "Shopping":

        return f"""
        You are spending the most on Shopping (₹{top_amount}).
        Try reducing unnecessary purchases and improve monthly savings.
        """

    elif top_category == "Food":

        return f"""
        Food is your highest spending category (₹{top_amount}).
        Maintain a balanced food budget and avoid overspending.
        """

    elif top_category == "Travel":

        return f"""
        Travel expenses are high (₹{top_amount}).
        Plan trips carefully and maintain budget control.
        """

    elif top_category == "Bills":

        return f"""
        Your recurring bills are increasing (₹{top_amount}).
        Monitor monthly subscriptions and utility usage.
        """

    else:

        return """
        Track expenses regularly and maintain healthy savings habits.
        """
# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("💰 AI Financial Advisor")
groq_api_key = st.sidebar.text_input(
    "Enter Groq API Key",
    type="password"
)

# ---------------------------------------------------
# LLM SETUP
# ---------------------------------------------------

llm = None

if groq_api_key:

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile"
    )

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Expense",
        "Expense History",
        "AI Advisor",
        "Profile"
    ]
)

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

if page == "Dashboard":

    st.title("AI Financial Advisor")

    st.caption(
        "Smart Expense Tracking & Financial Intelligence"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Expense",
            f"₹{total_expense}"
        )

    with col2:
        st.metric(
            "Financial Score",
            f"{financial_score}/100"
        )

    with col3:
        st.metric(
            "Budget Status",
            budget_status
        )
    with col4:
        st.metric(
            "Top Category",
            top_category
        )

    st.divider()

    st.subheader("Budget Utilization")

    budget_used_percentage = (
        total_expense / st.session_state.budget
    ) * 100

    if budget_used_percentage > 100:
        budget_used_percentage = 100

    st.progress(
        int(budget_used_percentage)
    )

    st.write(
        f"Budget Used: {budget_used_percentage:.1f}%"
    )

    remaining_budget = (
        st.session_state.budget - total_expense
    )

    st.write(
        f"Remaining Budget: ₹{remaining_budget}"
    )

    st.divider()

    st.subheader("Expense Distribution")

    if not df.empty:

        category_data = df.groupby(
            "category"
        )["amount"].sum()

        fig2, ax2 = plt.subplots(figsize=(3,3))

        ax2.pie(
            category_data.values,
            labels=category_data.index,
            autopct='%1.1f%%'
        )

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

          st.pyplot(fig2)
    else:
        st.info("No expense data available.")
    
        st.divider()

    st.subheader("AI Smart Alerts")

    if total_expense > st.session_state.budget:

        st.error(
            "🚨 AI Alert: You have exceeded your monthly budget."
        )

    elif total_expense > (0.9 * st.session_state.budget):

        st.warning(
            "⚠ AI Alert: Your expenses are very close to budget limit."
        )

    if not df.empty:

        highest_category = category_data.idxmax()

        highest_amount = category_data.max()

        if highest_category == "Shopping":

            st.warning(
                f"⚠ High Shopping Expense Detected: ₹{highest_amount}"
            )

        elif highest_category == "Food":

            st.info(
                f"🍔 Food spending is currently high: ₹{highest_amount}"
            )

        elif highest_category == "Travel":

            st.info(
                f"✈ Travel expenses are increasing: ₹{highest_amount}"
            )

    if financial_score < 50:

        st.error(
            "🚨 Financial health is poor. Reduce unnecessary spending."
        )

    elif financial_score < 75:

        st.warning(
            "⚠ Financial health needs improvement."
        )

    else:

        st.success(
            "✅ Financial health looks stable."
        )

    st.divider()

    st.subheader("Monthly Expense Trend")

    if not df.empty:

        trend_data = df.groupby(
            "date"
        )["amount"].sum()

        fig3, ax3 = plt.subplots(figsize=(7,3))

        ax3.plot(
            trend_data.index,
            trend_data.values,
            marker='o'
        )

        ax3.set_xlabel("Date")
        ax3.set_ylabel("Expense Amount")

        plt.xticks(rotation=45)

        st.pyplot(fig3)

    else:
        st.info("No trend data available.")

    st.divider()

    st.subheader("AI Financial Report")

    generate_report = st.button(
      "Generate AI Financial Report"
    )

    if generate_report:

      if llm is None:

        st.warning(
            "Please enter Groq API Key in sidebar."
        )

      else:

        if not df.empty:

            report_categories = df.groupby(
                "category"
            )["amount"].sum().to_dict()

        else:

            report_categories = {}

        report_prompt = f"""

        You are an advanced AI Financial Analyst.

        Analyze the user's financial condition professionally.

        USER FINANCIAL DATA:

        Total Expense: ₹{total_expense}

        Monthly Budget: ₹{st.session_state.budget}

        Financial Score: {financial_score}/100

        Expense Breakdown:
        {report_categories}

        Generate a detailed financial report including:

        1. Financial Summary
        2. Spending Behavior Analysis
        3. Overspending Detection
        4. Savings Suggestions
        5. Budget Improvement Advice
        6. Investment Suggestions
        7. Financial Risk Warnings
        8. Long-term Financial Improvement Tips

        Keep the report:
        - professional
        - practical
        - intelligent
        - personalized
        - beginner friendly

        """

        report_response = llm.invoke(
            report_prompt
        )

        st.session_state.report_content = (
            report_response.content
        )

        st.session_state.show_report = True


    if st.session_state.show_report:

      col1, col2 = st.columns([10,1])

      with col2:

        if st.button("❌"):

            st.session_state.show_report = False

            st.session_state.report_content = ""

            st.rerun()

      st.chat_message("assistant").write(
        st.session_state.report_content
      )

    st.divider()

    st.subheader("Recent Expenses")

    if not df.empty:

        recent_df = df.tail(5).copy()

        recent_df.columns = [
          "ID",
          "Amount",
          "Category",
          "Date"
        ]

        recent_df = recent_df.reset_index(drop=True)

        st.dataframe(
          recent_df,
          use_container_width=True,
          hide_index=True
        )

    else:
        st.info("No expenses recorded.")

# ---------------------------------------------------
# UPLOAD PAGE
# ---------------------------------------------------

elif page == "Upload Expense":

    st.title("Upload Expense Screenshot")

    uploaded_file = st.file_uploader(
        "Upload Screenshot",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

          st.image(
            image,
            caption="Uploaded Screenshot",
            width=300
          )

        # OCR

        opencv_image = cv2.cvtColor(
            np.array(image),
            cv2.COLOR_RGB2BGR
        )

        extracted_text = pytesseract.image_to_string(
            opencv_image
        )

        st.subheader("OCR Extracted Text")

        st.text(extracted_text)

        # Smart amount detection

        # Smart amount detection

        amount_matches = re.findall(
          r"(?:₹|Rs\.?|rs\.?|INR|%|=)\s?(\d+(?:,\d+)*)",
          extracted_text
        )

        if amount_matches:

          amounts = [
            int(x.replace(",", ""))
            for x in amount_matches
          ]

          detected_amount = max(amounts)

        else:

          detected_amount = 0

        category = detect_category(
            extracted_text
        )

        advice = get_ai_advice(
            category
        )

        st.subheader("Expense Analysis")

        st.success(
            f"Detected Amount: ₹{detected_amount}"
        )

        st.info(
            f"Detected Category: {category}"
        )

        st.write("### AI Recommendation")

        st.write(advice)

        # Save button

        # Auto save expense

        if "last_uploaded_file" not in st.session_state:

          st.session_state.last_uploaded_file = None

        current_file = uploaded_file.name

        if (
          detected_amount > 0 and
          st.session_state.last_uploaded_file != current_file
        ):

            cursor.execute("""
            INSERT INTO expenses
            (amount, category, date)
            VALUES (?, ?, ?)
            """, (
                detected_amount,
                category,
                datetime.now().strftime("%Y-%m-%d")
            ))

            conn.commit()

            st.session_state.last_uploaded_file = current_file

            st.success(
                "Expense Automatically Added Successfully!"
            )

            st.rerun()


            st.divider()

    st.subheader("Manual Expense Entry")

    manual_amount = st.number_input(
        "Enter Amount",
        min_value=1,
        step=1
    )

    manual_category = st.selectbox(
        "Select Category",
        [
            "Food",
            "Shopping",
            "Travel",
            "Bills",
            "Transfer",
            "Entertainment",
            "Health",
            "Other"
        ]
    )

    if st.button("Add Manual Expense"):

        cursor.execute("""
        INSERT INTO expenses
        (amount, category, date)
        VALUES (?, ?, ?)
        """, (
            manual_amount,
            manual_category,
            datetime.now().strftime("%Y-%m-%d")
        ))

        conn.commit()

        st.success(
            "Manual Expense Added Successfully!"
        )

        st.rerun()
# ---------------------------------------------------
# EXPENSE HISTORY
# ---------------------------------------------------

elif page == "Expense History":

    st.title("Expense History")

    if not df.empty:

        display_df = df.copy()

        display_df.columns = [
          "ID",
          "Amount",
          "Category",
          "Date"
        ]

        display_df = display_df.reset_index(drop=True)

        st.dataframe(
          display_df,
          use_container_width=True,
          hide_index=True
        )

        st.divider()

        csv = df.to_csv(
            index=False
        ).encode('utf-8')

        st.download_button(
            label="Download Expense Report",
            data=csv,
            file_name='expense_report.csv',
            mime='text/csv'
        )

        st.divider()

        st.subheader("Delete Expense")

        expense_ids = df["id"].tolist()

        selected_id = st.selectbox(
            "Select Expense ID",
            expense_ids
        )

        if st.button("Delete Expense"):

            cursor.execute(
                "DELETE FROM expenses WHERE id=?",
                (selected_id,)
            )

            conn.commit()

            st.success(
                "Expense Deleted Successfully!"
            )
            st.rerun()
        
        st.divider()

        st.subheader("Edit Expense")

        edit_id = st.selectbox(
            "Select Expense ID to Edit",
            expense_ids,
            key="edit_expense"
        )

        selected_expense = df[
            df["id"] == edit_id
        ].iloc[0]

        new_amount = st.number_input(
            "New Amount",
            value=int(selected_expense["amount"])
        )

        new_category = st.selectbox(
            "New Category",
            [
                "Food",
                "Shopping",
                "Travel",
                "Entertainment",
                "Bills",
                "Transfer"
            ],
            index=[
                "Food",
                "Shopping",
                "Travel",
                "Entertainment",
                "Bills",
                "Transfer"
            ].index(selected_expense["category"])
        )

        if st.button("Update Expense"):

            cursor.execute("""
            UPDATE expenses
            SET amount=?, category=?
            WHERE id=?
            """, (
                new_amount,
                new_category,
                edit_id
            ))

            conn.commit()

            st.success(
                "Expense Updated Successfully!"
            )
            st.rerun()

    else:
        st.info("No expense history available.")

# ---------------------------------------------------
# AI ADVISOR
# ---------------------------------------------------

elif page == "AI Advisor":

    st.title("Agentic AI Financial Advisor")

    st.write(
        "Ask anything about your expenses, savings, investments or financial habits."
    )
    if st.button("Clear Chat History"):

        st.session_state.chat_history = []

        st.success("Chat history cleared successfully!")

    question = st.chat_input(
    "Ask your financial question"
)

 # Conversation memory

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # Display previous chat history

    for chat in st.session_state.chat_history:

        st.chat_message(
            chat["role"]
        ).write(chat["content"])

    if question:

        if llm is None:

            st.warning(
                "Please enter Groq API Key in sidebar."
            )

        else:

            # User financial context

            if not df.empty:

              category_summary = df.groupby(
              "category"
              )["amount"].sum().to_dict()

              transaction_history = df.to_string(
                index=False
              )

            else:

              category_summary = {}

              transaction_history = "No transaction history available."

            # Prompt

            prompt = f"""

            You are an advanced Agentic AI Financial Advisor.

            Your role:
            - Analyze user financial behavior
            - Understand spending habits
            - Give intelligent financial reasoning
            - Provide personalized savings suggestions
            - Recommend investment ideas carefully
            - Detect overspending behavior
            - Act like a professional AI financial mentor

            USER FINANCIAL PROFILE:

            Name: {st.session_state.profile['name']}

            Age: {st.session_state.profile['age']}

            Occupation: {st.session_state.profile['occupation']}

            Monthly Income: ₹{st.session_state.profile['income']}

            Financial Goal: {st.session_state.profile['goal']}

            Total Expense: ₹{total_expense}

            Monthly Budget: ₹{st.session_state.budget}

            Financial Score: {financial_score}/100

            Expense Breakdown:
            {category_summary}

            Transaction History:
            {transaction_history}

            BEHAVIOR ANALYSIS:
            - Identify highest spending category
            - Detect risky spending habits
            - Suggest financial improvements
            - Suggest better savings habits
            - Give practical real-world advice

            USER QUESTION:
            {question}

            IMPORTANT:
            Give personalized answers based on user's actual expenses.
            Also:
            - Suggest SIP or mutual fund investing for long-term savings if appropriate
            - Recommend emergency fund planning
            - Encourage healthy budgeting habits
            - Explain financial risks carefully
            - Give beginner-friendly financial education
            - Avoid unrealistic financial promises
            Keep responses practical, intelligent and professional.

            """

            # Main AI Response

             # Store conversation

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            # Add previous conversation

            conversation_context = ""

            for chat in st.session_state.chat_history:

                conversation_context += f"""
                {chat['role']}: {chat['content']}
                """

            # Final prompt

            final_prompt = f"""

            Previous Conversation:
            {conversation_context}

            Current Request:
            {prompt}

            """

            # AI response

            with st.spinner("AI Financial Agent is analyzing..."):

              response = llm.invoke(final_prompt)

            # Save AI response

            st.session_state.chat_history.append(
              { 
                "role": "assistant",
                "content": response.content
              }
            )

            st.chat_message("assistant").write(
              response.content
            )
# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------

# ---------------------------------------------------
# PROFILE
# ---------------------------------------------------

elif page == "Profile":

    st.title("Financial Profile")

    if "edit_profile" not in st.session_state:

        st.session_state.edit_profile = False

    profile = st.session_state.profile

    # PROFILE DISPLAY

    if not st.session_state.edit_profile:

        st.markdown(f"""
        ### 👤 {profile['name'] if profile['name'] else 'User'}

        **Age:** {profile['age']}

        **Occupation:** {profile['occupation']}

        **Monthly Income:** ₹{profile['income']}

        **Financial Goal:** {profile['goal']}

        **Monthly Budget:** ₹{st.session_state.budget}
        """)

        st.divider()

        if st.button("Edit Profile"):

            st.session_state.edit_profile = True

            st.rerun()

    # EDIT MODE

    else:

        st.subheader("Edit Financial Profile")

        name = st.text_input(
            "Name",
            value=profile["name"]
        )

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=profile["age"]
        )

        occupation = st.text_input(
            "Occupation",
            value=profile["occupation"]
        )

        income = st.number_input(
            "Monthly Income",
            min_value=0,
            value=profile["income"]
        )

        goal = st.selectbox(
            "Financial Goal",
            [
                "Savings",
                "Investment",
                "Emergency Fund",
                "Debt Reduction",
                "Wealth Building"
            ]
        )

        budget = st.number_input(
            "Monthly Budget",
            value=st.session_state.budget,
            step=1000
        )

        if st.button("Save Profile"):

            st.session_state.profile = {
                "name": name,
                "age": age,
                "occupation": occupation,
                "income": income,
                "goal": goal
            }

            st.session_state.budget = budget

            st.session_state.edit_profile = False

            st.success(
                "Profile Updated Successfully!"
            )

            st.rerun()

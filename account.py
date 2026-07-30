import streamlit as st


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def info_row(label, value):
    """Horizontal key/value row."""
    col1, col2 = st.columns([1.2, 2.5], gap="small")

    with col1:
        st.markdown(f"**{label}**")

    with col2:
        st.write(value)


def profile_completion(profile):
    score = 0

    if profile["name"].strip():
        score += 1

    if profile["occupation"].strip():
        score += 1

    if profile["goal"].strip():
        score += 1

    if profile["income"] > 0:
        score += 1

    return int(score / 4 * 100)


# -------------------------------------------------
# ACCOUNT PAGE
# -------------------------------------------------

def show_account(df):

    profile = st.session_state.profile

    st.title("👤 My Account")
    st.caption("Manage your profile and financial information")

    st.divider()

    # -------------------------------------------------
    # PROFILE HEADER
    # -------------------------------------------------

    with st.container(border=True):

        left, right = st.columns([1, 5])

        with left:

            if profile["name"].strip():

                words = profile["name"].split()

                initials = (
                    words[0][0] +
                    (words[-1][0] if len(words) > 1 else "")
                ).upper()

            else:

                initials = "U"

            st.markdown(
                f"""
                <div style="
                width:90px;
                height:90px;
                border-radius:50%;
                background:#4F46E5;
                color:white;
                display:flex;
                justify-content:center;
                align-items:center;
                font-size:36px;
                font-weight:bold;">
                {initials}
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.subheader(
                profile["name"] if profile["name"] else "Welcome"
            )

            st.caption("AI Financial Advisor User")

            percent = profile_completion(profile)

            st.progress(percent)

            st.caption(f"Profile Completion : {percent}%")

    st.write("")

    # -------------------------------------------------
    # INFORMATION CARDS
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    # ---------------------------------------

    with col1:

        with st.container(border=True):

            st.markdown("### 👤 Personal Information")

            info_row(
                "👤 Name",
                profile["name"] or "Not Set"
            )

            info_row(
                "🎂 Age",
                profile["age"]
            )

            info_row(
                "💼 Occupation",
                profile["occupation"] or "Not Set"
            )

    # ---------------------------------------

    with col2:

        with st.container(border=True):

            st.markdown("### 💰 Financial Information")

            info_row(
                "💰 Income",
                f"₹{profile['income']:,}"
            )

            info_row(
                "💳 Budget",
                f"₹{st.session_state.budget:,}"
            )

            info_row(
                "🎯 Goal",
                profile["goal"] or "Not Set"
            )

    st.write("")
    
        # -------------------------------------------------
    # DIALOGS
    # -------------------------------------------------

    @st.dialog("✏️ Edit Profile")
    def edit_profile():

        with st.form("profile_form"):

            name = st.text_input(
                "Full Name",
                profile["name"]
            )

            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=int(profile["age"])
            )

            occupation = st.text_input(
                "Occupation",
                profile["occupation"]
            )

            income = st.number_input(
                "Monthly Income",
                min_value=0,
                value=int(profile["income"])
            )

            goal = st.text_input(
                "Financial Goal",
                profile["goal"]
            )

            budget = st.number_input(
                "Monthly Budget",
                min_value=0,
                value=int(st.session_state.budget)
            )

            save = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

            if save:

                profile["name"] = name
                profile["age"] = age
                profile["occupation"] = occupation
                profile["income"] = income
                profile["goal"] = goal

                st.session_state.budget = budget

                st.success("Profile Updated Successfully")

                st.rerun()

    # -------------------------------------------------
    # QUICK ACTIONS
    # -------------------------------------------------

    st.subheader("⚙️ Quick Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        with st.container(border=True):

            st.markdown("### ✏️")

            st.markdown("**Profile**")

            st.caption("Edit personal details")

            if st.button(
                "Open",
                key="profile_btn",
                use_container_width=True
            ):

                edit_profile()

    with c2:

        with st.container(border=True):

            st.markdown("### 💰")

            st.markdown("**Budget**")

            st.caption(
                f"₹{st.session_state.budget:,}"
            )

            if st.button(
                "Edit",
                key="budget_btn",
                use_container_width=True
            ):

                edit_profile()

    with c3:

        with st.container(border=True):

            st.markdown("### 🎯")

            st.markdown("**Goal**")

            st.caption(
                profile["goal"] or "Not Set"
            )

            if st.button(
                "Update",
                key="goal_btn",
                use_container_width=True
            ):

                edit_profile()

    with c4:

        with st.container(border=True):

            st.markdown("### 📥")

            st.markdown("**Export**")

            st.caption("Download CSV Report")

            st.download_button(
                "Download",
                df.to_csv(index=False).encode(),
                "expense_report.csv",
                "text/csv",
                use_container_width=True
            )

    st.write("")
    
        # -------------------------------------------------
    # ABOUT
    # -------------------------------------------------

    with st.container(border=True):

        st.subheader("ℹ️ About")

        info_row(
            "Application",
            "AI Financial Advisor"
        )

        info_row(
            "Version",
            "1.0.0"
        )

        info_row(
            "Framework",
            "Streamlit"
        )

        info_row(
            "Database",
            "SQLite"
        )

        info_row(
            "LLM",
            "Groq Llama 3.3 70B"
        )

        info_row(
            "OCR",
            "Gemini OCR + EasyOCR"
        )

    st.write("")

    # -------------------------------------------------
    # FOOTER
    # -------------------------------------------------

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:gray;
            font-size:14px;
            padding-top:10px;">
            © 2026 <b>Vivek G L</b> • AI Financial Advisor
        </div>
        """,
        unsafe_allow_html=True
    )
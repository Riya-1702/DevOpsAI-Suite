import streamlit as st
import sqlite3
import pandas as pd


# --- Admin credentials (temporary hardcoded) ---
ADMIN_EMAIL = "Riyasharmaabcd334@gmail.com"
ADMIN_PASSWORD = "Riya1417"

def run1():
    # ✅ Apply theme globally
   

    st.title("🛠️ Admin Panel")

    # --- Admin login form ---
    with st.form("admin_login_form"):
        admin_email = st.text_input("Admin Email")
        admin_password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")

    # --- Check credentials ---
    if login_submit:
        if admin_email == ADMIN_EMAIL and admin_password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("Admin login successful!")
            st.rerun()
        else:
            st.error("Invalid admin credentials")

    # --- Show admin tools if logged in ---
    if st.session_state.get("admin_logged_in"):

        st.success("Welcome Admin!")
        st.markdown("Use the tools below to manage students and view feedback.")
        st.markdown("---")

        st.header("👥 View & Delete Student Entries")

        # --- Connect to student database ---
        try:
            conn1 = sqlite3.connect("student_data.db")
            cursor1 = conn1.cursor()

            students_df = pd.read_sql_query("SELECT * FROM users", conn1)
            st.dataframe(students_df)

            selected_email = st.selectbox("Select a student to delete", students_df["email"].unique())

            if st.button("Delete Student"):
                cursor1.execute("DELETE FROM users WHERE email = ?", (selected_email,))
                conn1.commit()
                st.success(f"Deleted student: {selected_email}")
                st.rerun()

            conn1.close()
        except Exception as e:
            st.error(f"Error accessing student database: {e}")

        st.markdown("---")
        st.header("📝 View User Feedbacks")

        # --- Connect to feedback database ---
        try:
            conn2 = sqlite3.connect("settingm.db")
            feedback_df = pd.read_sql_query("SELECT email, ef, feedback FROM users", conn2)
            st.dataframe(feedback_df)
            conn2.close()
        except Exception as e:
            st.error(f"Error accessing feedback database: {e}")

    else:
        st.warning("Invalid credential")

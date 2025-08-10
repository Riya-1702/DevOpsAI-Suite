import streamlit as st
import pandas as pd
import sqlite3
import hashlib


def init_db():
    conn = sqlite3.connect('settingm.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            ef TEXT,
            feedback TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def run1():
      # ✅ Apply global theme

    st.title("⚙️ Settings")

    # ✅ Initialize DB
    init_db()
    with st.popover("📝 Feedback Form"):
        st.markdown("**Please provide your feedback**")

        email = st.text_input("Enter your email")
        password = st.text_input("Enter your password", type="password")
        ef = st.feedback("faces")
        feedback = st.text_area("Write your feedback")

        if st.button("Submit"):
            if email and password and feedback:
                try:
                    conn = sqlite3.connect('settingm.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (email, password, ef, feedback) VALUES (?, ?, ?, ?)",
                    (email, hashlib.sha256(password.encode()).hexdigest(), ef, feedback))
                    conn.commit()
                    conn.close()
                    st.success("✅ Thank you for your feedback. We will surely improve it.")
                except sqlite3.IntegrityError:
                        st.error("⚠️ Feedback not submitted. Email already exists.")
            else:
                    st.error("⚠️ Please fill in all required fields.")


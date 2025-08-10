

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib


def run_home():
    # Initialize DB
    def init_db():
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()

    def add_user(email, password):
        if not email or not password:
            return False
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def verify_user(email, password):
        if not email or not password:
            return None
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
        user = cursor.fetchone()
        conn.close()
        return user

    # Initialize DB once
    init_db()

    # Session defaults
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

    # Custom CSS
    st.markdown("""
    <style>
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .welcome-card h2 {
        margin-bottom: 1rem;
        font-size: 2.5em;
    }
    .welcome-card p {
        font-size: 1.2em;
        opacity: 0.9;
    }
    .login-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main Page
    st.title("🎓 Student Guider - Home")

    if st.session_state.logged_in:
        st.markdown(f"""
        <div class="success-message">
            <h3>Welcome back, {st.session_state.user_email}!</h3>
            <p>You are successfully logged in to Student Guider.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Logout", type="secondary"):
                st.session_state.logged_in = False
                st.session_state.user_data = None
                st.session_state.user_email = None
                st.success("You have been logged out successfully!")
                st.rerun()

    else:
        st.markdown("""
        <div class="welcome-card">
            <h2>Welcome to Student Guider!</h2>
            <p>Your personal academic companion for guidance and support</p>
        </div>
        """, unsafe_allow_html=True)

        option = st.selectbox("Choose an option:", ["Login", "Sign up"])

        if option == "Login":
            st.markdown('<div class="login-section">', unsafe_allow_html=True)
            st.subheader("Login to Your Account")

            with st.form(key=f"student_login_form_{id(st)}"):
                login_email = st.text_input("Email Address", placeholder="Enter your email")
                login_password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("Login", type="primary")

                if submit_login:
                    if login_email and login_password:
                        user = verify_user(login_email, login_password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_data = user
                            st.session_state.user_email = login_email
                            st.success(f"Welcome back, {login_email}!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")
                    else:
                        st.warning("⚠️ Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown('<div class="login-section">', unsafe_allow_html=True)
            st.subheader("Create New Account")

            with st.form(key=f"signup_form_{id(st)}"):
                signup_email = st.text_input("Email Address", placeholder="Enter your email")
                signup_password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                submit_signup = st.form_submit_button("Create Account", type="primary")

                if submit_signup:
                    if signup_email and signup_password and confirm_password:
                        if signup_password == confirm_password:
                            if len(signup_password) >= 6:
                                success = add_user(signup_email, signup_password)
                                if success:
                                    st.success("Account created successfully! Please login with your credentials.")
                                else:
                                    st.error("Email already exists. Please use a different email.")
                            else:
                                st.error("Password must be at least 6 characters long.")
                        else:
                            st.error("Passwords do not match. Please try again.")
                    else:
                        st.warning("Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)


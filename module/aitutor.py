def run():
    import streamlit as st

    # Set page config
    st.title("Student Guider")

    st.markdown("""
    <style>
        /* Remove default spacing and padding */
        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 1000px;
        }
        
        /* Hide Streamlit header and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Light background */
        .stApp {
            background: #ffffff;
            min-height: 100vh;
        }
        
        /* Simple light container */
        .main-container {
            background: transparent;
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem auto;
            max-width: 800px;
        }
        
        /* Dark title */
        .main h1 {
            color: #333333;
            text-align: center;
            font-size: 3.5rem;
            margin: 0;
            font-weight: 700;
            text-shadow: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -1px;
        }
        
        /* Dark subtitle */
        .subtitle {
            color: #666666;
            text-align: center;
            font-size: 1.2rem;
            margin: 0.5rem 0 2rem 0;
            font-weight: 300;
            letter-spacing: 0.5px;
        }
        
        /* Dark welcome card */
        .welcome-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #e9ecef;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .welcome-card p {
            color: #495057;
            font-size: 1.1rem;
            margin: 0;
            line-height: 1.6;
        }
        
        /* Light status messages */
        .stSuccess {
            background: rgba(168, 230, 207, 0.2);
            border: 1px solid rgba(168, 230, 207, 0.8);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            color: #155724;
        }
        
        .stWarning {
            background: rgba(255, 234, 167, 0.3);
            border: 1px solid rgba(255, 234, 167, 0.8);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            color: #856404;
        }
        
        /* Lavender sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #d9bfff 0%, #caa3ff 100%);
        border-right: 1px solid #b88cff;
    }

        
        /* Light navigation menu */
        .stSelectbox > div > div {
            background: #ffffff;
            border: 1px solid #d4c5ff;
            border-radius: 10px;
            color: #495057;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div > div {
            color: #495057;
        }
        
        /* Selectbox hover effect */
        .stSelectbox > div > div:hover {
            background: #f8f5ff;
            border-color: #b899ff;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(184, 153, 255, 0.2);
        }
        
        /* Selectbox dropdown styling */
        .stSelectbox [data-baseweb="select"] > div {
            background: #ffffff;
            border: 1px solid #d4c5ff;
            border-radius: 10px;
        }
        
        /* Selectbox dropdown options */
        .stSelectbox [data-baseweb="select"] [role="option"] {
            background: #ffffff;
            color: #495057;
            transition: all 0.3s ease;
        }
        
        /* Selectbox dropdown options hover */
        .stSelectbox [data-baseweb="select"] [role="option"]:hover {
            background: linear-gradient(135deg, #f3f0ff 0%, #e8e3ff 100%);
            color: #6f42c1;
        }
        
        /* Selectbox dropdown options selected */
        .stSelectbox [data-baseweb="select"] [role="option"][aria-selected="true"] {
            background: linear-gradient(135deg, #b899ff 0%, #a085ff 100%);
            color: #ffffff;
        }
        
        /* Selectbox arrow */
        .stSelectbox [data-baseweb="select"] svg {
            color: #6f42c1;
        }
        
        /* Light button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }
        
        /* Light input styling */
        .stTextInput > div > div > input {
            background: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 10px;
            color: #495057;
            padding: 0.75rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #6c757d;
        }
        
        /* Remove default dividers */
        hr {
            display: none;
        }
        
        /* Floating animation */
        .main-container {
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        /* Page load animation */
        .main {
            animation: fadeIn 1s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main h1 {
                font-size: 2.5rem;
            }
            
            .main-container {
                padding: 1.5rem;
                margin: 0.5rem;
            }
            
            .main .block-container {
                padding: 0.5rem;
            }
        }
        
        /* Light scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f8f9fa;
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #ced4da;
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #667eea;
        }
        
        /* Hide markdown container backgrounds */
        .main .markdown-text-container {
            background: transparent;
            padding: 0;
            margin: 0;
            box-shadow: none;
            border: none;
        }
        
        /* Special text styling */
        .element-container {
            background: transparent;
            padding: 0;
            margin: 0;
            box-shadow: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Import home (function-based), but delay other imports until needed
    import homem

    # Initialize session
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Create main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Title and intro
    st.title("🎓 Student Guider")
    st.markdown('<p class="subtitle">Your personal academic assistant</p>', unsafe_allow_html=True)

    # 🟢 If user is logged in — show navigation
    if st.session_state.logged_in:
        st.success(f"✨ Welcome back, {st.session_state.get('user_email', 'user')}!")
        
        # ⏳ Import only when logged in
        import ai_tutorm 
        import settingm
        import admin
        import logout
        c = st.sidebar.selectbox("Menu", ["AI Tutor", "Settings", "Admin", "Logout"])
        
        if c == "AI Tutor":
            ai_tutorm.run1()
        elif c == "Settings":
            settingm.run1()
        elif c == "Logout":
            logout.run1()
        elif c == "Admin":
            admin.run1()

    # 🔴 If not logged in — show home login/signup page only
    else:
        st.markdown('''
        <div class="welcome-card">
            <p>🔐 Please login to continue</p>
        </div>
        ''', unsafe_allow_html=True)
        
        homem.run_home()

    st.markdown('</div>', unsafe_allow_html=True)


        

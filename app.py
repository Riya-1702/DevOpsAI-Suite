import streamlit as st
import importlib
import sys
import os

# --- Page Configuration and Setup (No changes here) ---
# Add the module directory to the Python path
# Assuming the script is in the root directory and modules are in './module/'
module_path = os.path.join(os.path.dirname(__file__), 'module')
if module_path not in sys.path:
    sys.path.append(module_path)

# Configure page
st.set_page_config(
    page_title="DevOpsAI Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (No changes here) ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header"><h1>🚀 DevOpsAI Suite</h1></div>', unsafe_allow_html=True)

# --- Page Modules Dictionary (No changes here) ---
page_modules = {
    "Home": "home",
    "Linux Dashboard": "linux_menu",
    "Docker Dashboard": "docker_menu",
    "Python Menu": "python_menu",
    "Kubernetes Dashboard": "kubernetes_dashboard",
    "AWS Automation": "aws_automation",
    "Git Automation": "git_automation",
    "Linear Regression": "linear_regression",
    "ML Dashboard": "ml_dashboard",
    "Amazon WebScrape": "amazon_webscrape",
    "AI Tutor": "aitutor",
    "Gesture Docker Dashboard": "gesture_docker_dashboard",
    "JavaScript Menu": "js",
    "Mood Swifter": "mylangchaintool"
}

# --- CORRECTED NAVIGATION LOGIC ---

# 1. Initialize session state to remember the page.
#    This runs only once at the start of the session.
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# 2. Create the sidebar selectbox.
#    The `key` argument is crucial. It links the widget's state to st.session_state.
#    We will use the value from st.session_state to determine the page to show.
#    To make the selectbox display the correct page after a rerun, we set its `index`.
page_options = list(page_modules.keys())
st.sidebar.title("📚 Navigation")
selected_page = st.sidebar.selectbox(
    "Select a page", 
    page_options, 
    index=page_options.index(st.session_state.page), # Set current selection based on session state
    key='navigation_selectbox' # Use a key to access its value if needed, though we primarily use callbacks now
)

# Update the session state page IF the selectbox value has changed
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun() # Rerun to load the new page immediately

# --- CORRECTED PAGE LOADING LOGIC ---

# 3. Import and run the module based on the **persisted session state**.
try:
    current_page_key = st.session_state.page
    page_module_name = page_modules[current_page_key]
    
    # Import the selected module
    page_module = importlib.import_module(page_module_name)
    
    # Run the page's main function
    if hasattr(page_module, 'run_app'):
        page_module.run_app()
    elif hasattr(page_module, 'run'):
        page_module.run()
    # If no run function, the import itself runs the page code.
    
except ModuleNotFoundError:
    st.error(f"Module for '{st.session_state.page}' not found. Please ensure the file `module/{page_modules[st.session_state.page]}.py` exists.")
    st.info("You may need to install required dependencies. Check the requirements.txt file.")
    st.code("pip install -r requirements.txt", language="bash")
except Exception as e:
    st.error(f"Error loading the {st.session_state.page} page: {str(e)}")
    st.info("Please make sure the module exists and is properly implemented.")
    with st.expander("Detailed Error Information"):
        st.exception(e)

# --- Footer (No changes here) ---
st.sidebar.markdown("---")
st.sidebar.info(
    "This multi-page dashboard integrates various tools and utilities for different domains."
)
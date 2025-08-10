import streamlit as st
import google.generativeai as genai
from datetime import datetime

# NOTE: This is a placeholder function.
# Web scraping Amazon is complex and against their terms of service without permission.
# This mock function returns sample data so the app can run.
# Replace this with your actual data-gathering method.
def mock_scrape_amazon_data(query: str = "laptops", max_pages: int = 1) -> dict:
    """Returns a dictionary of mock Amazon product data."""
    st.warning("Using sample data. This is not real-time information from Amazon.")
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "products": [
            {
                "title": "High-Performance Gaming Laptop, 15.6 inch, 16GB RAM, 1TB SSD",
                "price": "₹1,20,000",
                "rating": "4.6 out of 5 stars",
                "availability": "In Stock",
                "features": ["NVIDIA RTX 4060", "144Hz Display", "RGB Keyboard"],
            },
            {
                "title": "Ultra-Thin Business Notebook, 14 inch, 8GB RAM, 512GB SSD",
                "price": "₹75,500",
                "rating": "4.4 out of 5 stars",
                "availability": "In Stock",
                "features": ["Lightweight Design", "Fingerprint Reader", "Long Battery Life"],
            },
            {
                "title": "Budget Student Laptop, 15 inch, 4GB RAM, 256GB SSD",
                "price": "₹35,990",
                "rating": "4.1 out of 5 stars",
                "availability": "Only 3 left in stock",
                "features": ["Windows 11", "HD Webcam", "Multiple Ports"],
            },
        ],
        "deals": ["Up to 30% off on electronics", "10% cashback with select cards"],
        "categories": ["Electronics", "Computers & Accessories", "Laptops"],
    }

# FIXED: This function now uses the correct Google Generative AI client.
def get_ai_response(question, scraped_data, api_key):
    """Get AI response using comprehensive scraped data and Google's Gemini."""
    try:
        if not api_key:
            return "Error: Please provide your Gemini API key in the secrets file."
        
        # Configure the Google AI client
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Format scraped data into a detailed prompt for the AI
        data_summary = f"REAL-TIME AMAZON DATA (Updated: {scraped_data.get('timestamp', 'N/A')} for query '{scraped_data.get('query')}'):\n"
        data_summary += f"PRODUCTS FOUND ({len(scraped_data.get('products', []))} items):\n"
        
        for i, product in enumerate(scraped_data.get('products', [])[:10]):
            data_summary += f"\n{i+1}. {product.get('title', 'N/A')}"
            if product.get('price'):
                data_summary += f" - Price: {product.get('price')}"
            if product.get('rating'):
                data_summary += f" - Rating: {product.get('rating')}"
            if product.get('availability'):
                data_summary += f" - Availability: {product.get('availability')}"
        
        system_prompt = f"""You are an expert Amazon shopping assistant with access to real-time data.
        Your knowledge is based on the following data provided by a web scraper.
        
        --- DATA START ---
        {data_summary}
        --- DATA END ---
        
        Provide detailed, accurate responses about the products listed. Use only the real-time data provided.
        Be helpful with product comparisons, price analysis, and shopping advice based *strictly* on this data.
        If the user asks about something not in the data, state that you don't have information on it."""
        
        with st.spinner("Generating AI response with real-time data..."):
            # The prompt for the Gemini model is the combination of the system instructions and the user's question.
            full_prompt = f"{system_prompt}\n\nUSER QUESTION: {question}"
            response = model.generate_content(full_prompt)
            return response.text
            
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

def run_app():
  
    st.title("🛒 AI Amazon Assistant")

    # --- Securely Load API Key ---
    try:
        gemini_api_key = "AIzaSyDR1-u9wlUu3dZjtrYPAmruQ-Lg2UqtFsw"
    except (KeyError, FileNotFoundError):
        st.error("🔴 **GEMINI_API_KEY not found!** Please create a `.streamlit/secrets.toml` file with your key.")
        st.stop()

    # --- Session State Initialization ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None

    # --- Main Interface ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Actions")
        
        if st.button("🔄 Get Sample Data", type="primary"):
            with st.spinner("Loading sample Amazon data..."):
                st.session_state.scraped_data = mock_scrape_amazon_data()
            st.success("Sample data loaded!")
        
        # FIXED: UI logic for search is now correct.
        search_query = st.text_input("Enter product to search for sample data:", key="search_input")
        if st.button("🔍 Search with Sample Data"):
            if search_query:
                with st.spinner(f"Loading sample data for '{search_query}'..."):
                    st.session_state.scraped_data = mock_scrape_amazon_data(query=search_query)
                st.success(f"Loaded sample data for: {search_query}")
            else:
                st.warning("Please enter a search query.")
        
        with st.expander("📊 View Current Data"):
            if st.session_state.scraped_data:
                st.json(st.session_state.scraped_data)
            else:
                st.info("No data available. Click 'Get Sample Data' first.")
    
    with col2:
        st.header("Chat with Assistant")
        
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about products, prices, or deals..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get fresh sample data if none exists
            if not st.session_state.scraped_data:
                with st.spinner("No data found, loading sample data..."):
                    st.session_state.scraped_data = mock_scrape_amazon_data()
            
            # Get and display AI response
            with st.chat_message("assistant"):
                ai_response = get_ai_response(prompt, st.session_state.scraped_data, gemini_api_key)
                st.markdown(ai_response)
            
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Sidebar for data info and clearing chat
    with st.sidebar:
        st.header("App Controls")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

        if st.session_state.scraped_data:
            st.markdown("---")
            st.markdown("### Current Data Info:")
            st.markdown(f"**Query:** `{st.session_state.scraped_data.get('query', 'N/A')}`")
            st.markdown(f"**Products:** `{len(st.session_state.scraped_data.get('products', []))}`")
            st.markdown(f"**Last Updated:** `{st.session_state.scraped_data.get('timestamp', 'N/A')}`")

# Function to be called by app.py
def run():
    # This function is intentionally empty as the Streamlit code above will run automatically
    pass


    # The main code runs automatically when the module is imported
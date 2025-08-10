import streamlit as st
from textblob import TextBlob

# --- LangChain Imports ---
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI


# --- Tool Definitions ---
# The agent will use the docstrings to decide which tool to use.

@tool
def get_emotion_from_text(text: str) -> str:
    """
    Analyzes the provided text to determine if the sentiment is positive, negative, or neutral.
    """
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        
        if sentiment > 0.1:
            return "positive"
        elif sentiment < -0.1:
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        return "neutral"

# Helper function to display mood emoji
def display_mood_emoji(mood: str):
    """
    Displays an emoji based on the detected mood.
    """
    mood_emojis = {
        "positive": "😊",
        "negative": "😔",
        "neutral": "😐"
    }
    
    emoji = mood_emojis.get(mood.lower(), "🤔")
    return emoji

@tool
def get_song_link_by_mood(mood: str) -> str:
    """
    Provides a clickable Spotify playlist link based on a given mood (positive, negative, or neutral).
    """
    mood_lower = mood.lower()
    
    MOOD_PLAYLIST_URLS = {
        "positive": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aJc1uA",  # Happy Hits
        "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX0XUfTFmNBRM", # Lofi Beats
        "negative": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1"  # Sad Indie
    }
    
    url = MOOD_PLAYLIST_URLS.get(mood_lower, MOOD_PLAYLIST_URLS["neutral"])
    
    # The agent will return this markdown string as its final answer.
    return f"Based on the detected mood, here is a playlist for you. [**Click here to listen 🎵**]({url})"


# --- Additional Tool for Enhanced Experience ---
@tool
def get_mood_recommendations(mood: str) -> str:
    """
    Provides personalized recommendations based on the detected mood.
    """
    mood_lower = mood.lower()
    
    recommendations = {
        "positive": [
            "Take a walk in nature to maintain your positive energy",
            "Share your happiness with friends or family",
            "Try a creative activity to channel your positive energy"
        ],
        "neutral": [
            "Practice mindfulness meditation to center yourself",
            "Read a book that interests you",
            "Try light exercise to boost your mood"
        ],
        "negative": [
            "Practice deep breathing exercises",
            "Write down your thoughts in a journal",
            "Reach out to a friend or family member for support"
        ]
    }
    
    mood_recs = recommendations.get(mood_lower, recommendations["neutral"])
    recommendations_text = "\n- " + "\n- ".join(mood_recs)
    
    return f"**Mood Recommendations:**{recommendations_text}"


# --- Main Application Logic ---
def run_app():
    """
    Initializes and runs the Streamlit application.
    """
    # Set page title and description
    st.title("🎵 Mood Swift - LangChain Tool")
    st.markdown("Tell me how you're feeling, and I'll find a playlist to match your mood and provide personalized recommendations.")
    st.markdown("---")

    # --- Sidebar with Information ---
    with st.sidebar:
        st.header("About This App")
        st.markdown("""
        This app uses LangChain and Gemini AI to:
        1. Analyze your mood from text
        2. Recommend music based on your emotional state
        3. Provide personalized recommendations
        
        **Technologies Used:**
        - LangChain for agent orchestration
        - TextBlob for sentiment analysis
        - Gemini AI for natural language understanding
        - Streamlit for the user interface
        """)

    # --- Load API Key ---
    google_api_key = 'AIzaSyDR1-u9wlUu3dZjtrYPAmruQ-Lg2UqtFsw'
    
    if not google_api_key or google_api_key == '':
        st.error("🔴 **Google API Key not found or invalid!**")
        st.info("Please make sure you have a valid Google API key configured.")
        st.stop()

    # --- Initialize the LLM and Agent ---
    # The LLM acts as the "brain" of the agent
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        temperature=0.2
    )

    # Define the list of tools the agent can use
    tools = [get_emotion_from_text, get_song_link_by_mood, get_mood_recommendations]

    # Create the LangChain agent executor
    agent_executor = create_react_agent(llm, tools)

    # --- Chat Interface ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message.type):
            st.markdown(message.content)

    # Get user input
    user_input = st.chat_input("Hi! Tell me how you're feeling today...")

    if user_input:
        # Add user message to history and display it
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.chat_message("human"):
            st.markdown(user_input)
        
        # Define the task for the agent
        task = f"""
        First, analyze the emotion of the following text to determine if it's positive, negative, or neutral.
        Then, based on that detected emotion, get a song playlist link.
        Finally, provide personalized recommendations based on the detected mood.
        Here is the text: "{user_input}"
        """

        # Stream the agent's response
        with st.chat_message("ai"):
            with st.spinner("Analyzing your mood and finding recommendations..."):
                try:
                    # Invoke the agent with the user's request
                    response = agent_executor.invoke(
                        {"messages": [HumanMessage(content=task)]}
                    )
                    
                    # The final answer is in the 'messages' list of the response
                    final_answer = response['messages'][-1].content
                    st.markdown(final_answer)
                except Exception as e:
                    # Log the detailed error for debugging
                    error_message = f"Error: {str(e)}"
                    st.error(error_message)
                    
                    # Provide a fallback response with direct tool calls
                    st.warning("I'll analyze your mood directly instead.")
                    
                    try:
                        # Direct tool calls as fallback
                        mood = get_emotion_from_text(user_input)
                        mood_emoji = display_mood_emoji(mood)
                        playlist = get_song_link_by_mood(mood)
                        recommendations = get_mood_recommendations(mood)
                        
                        # Display results with visual enhancements
                        st.markdown(f"### Detected mood: {mood_emoji} **{mood.capitalize()}**")
                        
                        # Create columns for better layout
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### 🎵 Music Recommendation")
                            st.markdown(playlist)
                        with col2:
                            st.markdown("#### 🌟 Mood Tips")
                            st.markdown(recommendations)
                        
                        final_answer = f"Detected mood: {mood}\n{playlist}\n{recommendations}"
                    except Exception as inner_e:
                        st.error(f"Fallback also failed: {str(inner_e)}")
                        final_answer = "I'm sorry, I encountered an error while processing your request. Please try again."
                        st.markdown(final_answer)

        # Add AI response to history
        st.session_state.messages.append(AIMessage(content=final_answer))

# --- Main execution block ---
if __name__ == "__main__":
    run_app()
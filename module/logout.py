import streamlit as st


def run1():
    # Apply global light/dark theme


    st.title("🚪 Logout")

    # Initialize login state if needed
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # If user is logged in, confirm logout
    if st.session_state.logged_in:
        st.warning("Are you sure you want to log out?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Log me out"):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.user_data = None
                st.success("✅ You have been logged out.")
                st.markdown("Return to the [Home page](main.py) to log in again.")
                st.stop()

        with col2:
            if st.button("❌ Cancel"):
                st.success("✅ Logout canceled.")
                st.markdown("You are still logged in. Go back to your dashboard.")
                st.stop()

    else:
        st.info("ℹ️ You are already logged out.")
        st.markdown("Go to the [Home page](main.py) to log in.")


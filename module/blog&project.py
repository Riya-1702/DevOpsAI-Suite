
"""
A Streamlit web application that serves as a central hub for blog posts and projects
related to Linux and Docker.
"""
import streamlit as st
import webbrowser

# --- Page Configuration and Main Title ---
st.title("My Linux & Docker Hub")
st.markdown("---")
st.write(
    """
    Welcome! This is a central hub for my blog posts and projects on Linux and Docker.
    Explore the resources below to learn more about these powerful technologies.
    """
)

# --- Linux Blog Section ---
st.header("Linux Blog")

st.subheader("1. Why Companies Use Linux")
st.write("An exploration of why companies are adopting Linux and the benefits they gain.")
if st.button("Read Article", key="read_linux_companies"):
    webbrowser.open_new_tab("https://kubernetesointee.blogspot.com/2025/07/why-our-company-thrives-on-linux-deeper.html")
    st.info("Opening 'Why Companies Use Linux' in a new tab...")

st.markdown("---")

st.subheader("2. 5 GUI Commands in Linux")
st.write("A look at 5 GUI programs in Linux and the commands working behind the scenes.")
if st.button("Read Article", key="read_gui_commands"):
    webbrowser.open_new_tab("https://kubernetesointee.blogspot.com/2025/07/5-gui-programs-in-linux-and-find-out.html")
    st.info("Opening '5 GUI Programs in Linux' in a new tab...")

st.markdown("---")

st.subheader("3. Understanding Ctrl+C and Ctrl+Z")
st.write("Unmasking the signals and system calls behind the Ctrl+C and Ctrl+Z keyboard shortcuts.")
if st.button("Read Article", key="read_ctrl_commands"):
    webbrowser.open_new_tab("https://kubernetesointee.blogspot.com/2025/07/unmasking-ctrlc-and-ctrlz-hidden.html")
    st.info("Opening 'Commands Behind Ctrl+C and Ctrl+Z' in a new tab...")

# --- Docker Blog & Projects Section ---
st.header("Docker Blog & Projects")

st.subheader("Docker Blog Post")
st.markdown("**Why Companies Use Docker**")
st.write("Discover why companies are using Docker and the competitive advantages it provides.")
# NOTE: The original URL for this article was incorrect. Please replace the placeholder with the correct link.
if st.button("Read Article", key="read_docker_companies"):
    # This URL is a placeholder. Update it with your actual Docker article link.
    docker_article_url = "https://kubernetesointee.blogspot.com/"
    webbrowser.open_new_tab(docker_article_url)
    st.info("Opening 'Why Companies Use Docker' in a new tab...")

st.markdown("---")

st.subheader("Docker Projects")

# Project 1: DND
st.markdown("**1. DND (Docker-in-Docker)**")
st.write("A project demonstrating how to run the Docker daemon inside a Docker container.")
if st.button("View Source Code", key="dnd_source_code"):
    webbrowser.open_new_tab("https://github.com/Riya-1702/dind-docker.git")
    st.info("Opening DND source code...")

st.markdown("---")

# Project 2: Firefox
st.markdown("**2. Firefox Container**")
st.write("Running a graphical application like Firefox inside a Docker container.")
if st.button("View Source Code", key="firefox_source_code"):
    webbrowser.open_new_tab("https://github.com/Riya-1702/firefox-docker.git")
    st.info("Opening Firefox source code...")

st.markdown("---")

# Project 3: Linear Regression
st.markdown("**3. Linear Regression Model**")
st.write("Packaging and running a machine learning (linear regression) model inside a Docker container.")
if st.button("View Source Code", key="linear_regression_source_code"):
    source_code_url = "https://github.com/Riya-1702/linear-regression-docker.git"
    webbrowser.open_new_tab(source_code_url)
    st.info("Opening Linear Regression source code...")

st.markdown("---")

# Project 4: Flask Web Application
st.markdown("**4. Flask Web Application**")
st.write("Containerizing and running a Python Flask web application, showcasing web service deployment.")
if st.button("View Source Code", key="flask_source_code"):
    source_code_url = "https://github.com/Riya-1702/flask-docker.git"
    webbrowser.open_new_tab(source_code_url)
    st.info("Opening Flask source code...")

st.markdown("---")

# Project 5: Python Menu Utility
st.markdown("**5. Python Menu Utility**")
st.write("Running a command-line Python menu utility inside a Docker container, ideal for simple interactive tools.")
if st.button("View Source Code", key="python_menu_source_code"):
    source_code_url = "https://github.com/Riya-1702/docker-python_menubased.git"
    webbrowser.open_new_tab(source_code_url)
    st.info("Opening Python Menu source code...")

st.markdown("---")

# --- Footer ---
st.write(
    """
    We hope you find these resources helpful on your Linux and Docker journey!
    """
)

# To run this app, save the code as a Python file (e.g., app.py) and run `streamlit run app.py` in your terminal.

# Function to be called by app.py
def run():
    # This function is intentionally empty as the Streamlit code above will run automatically
    pass
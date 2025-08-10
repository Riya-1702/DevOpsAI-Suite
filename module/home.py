def run():    
    import streamlit as st

    # Page configuration


    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        .contact-links {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .bio-section {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        .social-link {
            display: inline-block;
            margin: 0.5rem 1rem 0.5rem 0;
            padding: 0.5rem 1rem;
            background-color: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        
        .social-link:hover {
            background-color: #764ba2;
            color: white;
            text-decoration: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header Section
    st.markdown("""
    <div class="main-header">
        <h1>👩‍💻 Riya Sharma</h1>
        <h3>Cloud Automation, DevOps, and AI Specialist</h3>
    </div>
    """, unsafe_allow_html=True)

    # Introduction/Bio Section
    st.markdown("""
    <div class="bio-section">
        <h2>🚀 Welcome to My Project Hub!</h2>
        <p style="font-size: 1.1em; line-height: 1.6;">
            I am a passionate and driven engineer specializing in <strong>cloud automation</strong>, 
            <strong>DevOps</strong>, and <strong>machine learning</strong>. My work focuses on creating 
            efficient, scalable solutions using tools like Docker, Kubernetes, AWS, and Python. 
            I enjoy tackling complex challenges and building practical applications that leverage 
            cutting-edge technology.
        </p>
        <p style="font-size: 1.1em; line-height: 1.6;">
            <strong>🏆 Proud member of Team No. 72</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Contact & Social Links Section
    st.markdown("""
    <div class="contact-links">
        <h3>📞 Let's Connect!</h3>
    </div>
    """, unsafe_allow_html=True)

    # Create columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🌐 Portfolio**  
        [Visit My Website](https://iamriya.netlify.app)
        
        **🔗 LinkedIn**  
        [Connect with Me](https://www.linkedin.com/in/riya-sharma-638a6b217)
        """)

    with col2:
        st.markdown("""
        **🐙 GitHub**  
        [View My Code](https://github.com/Riya-1702)
        
        **📧 Email**  
        [riyasharmaabcd334@gmail.com](mailto:riyasharmaabcd334@gmail.com)
        """)

    # Skills Section
    st.markdown("---")
    st.subheader("🛠️ Technical Skills")

    skill_cols = st.columns(4)
    with skill_cols[0]:
        st.markdown("""
        **Cloud & DevOps**
        - AWS
        - Docker
        - Kubernetes
        - CI/CD
        """)

    with skill_cols[1]:
        st.markdown("""
        **Programming**
        - Python
        - Linux/Bash
        - Git
        - Automation Scripts
        """)

    with skill_cols[2]:
        st.markdown("""
        **Machine Learning**
        - Data Analysis
        - Model Development
        - ML Pipelines
        - AI Applications
        """)

    with skill_cols[3]:
        st.markdown("""
        **Web Technologies**
        - Streamlit
        - Web Scraping
        - APIs
        - Dashboard Development
        """)

    # Call to Action
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;">
        <h3>🎯 Explore My Projects</h3>
        <p style="font-size: 1.2em;">
            Please use the sidebar to navigate through my projects and discover the solutions I've built!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Built with ❤️ using Streamlit | © 2024 Riya Sharma</p>
    </div>
    """, unsafe_allow_html=True)

    # Function to be called by app.py

        
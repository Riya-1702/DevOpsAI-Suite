def run():
    import streamlit as st
    import psutil
    import pywhatkit as kit
    import datetime
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import requests
    from bs4 import BeautifulSoup
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    import io
    import base64
    import tempfile
    import os
    # Import for Twilio features
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioRestException
    # Import for Instagram feature
    from instagrapi import Client as InstaClient


    # --- Page Configuration ---


    # --- Sidebar Navigation ---
    st.sidebar.title("🚀 Feature Navigator")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "System Monitor",
            "WhatsApp Sender",
            "Call",
            "SMS",
            "Email Sender",
            "Instagram Poster",
            "Web Search",
            "Website Data Extractor",
            "Image Generator",
            "Face Swap"
        ]
    )

    # --- Page Implementations ---

    # System Monitor Page
    if page == "System Monitor":
        st.title("💻 System Resource Monitor")
        st.markdown("Monitor your system's performance in real-time")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Memory Usage")
            if st.button("Refresh Memory Stats"):
                mem = psutil.virtual_memory()
                st.metric("Total RAM", f"{mem.total / (1024 ** 3):.2f} GB")
                st.metric("Available RAM", f"{mem.available / (1024 ** 3):.2f} GB")
                st.metric("Used RAM", f"{mem.used / (1024 ** 3):.2f} GB")
                st.metric("RAM Usage", f"{mem.percent}%")
                st.progress(mem.percent / 100)

        with col2:
            st.subheader("CPU Usage")
            if st.button("Refresh CPU Stats"):
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                st.metric("CPU Usage", f"{cpu_percent}%")
                st.metric("CPU Cores", cpu_count)
                st.progress(cpu_percent / 100)

        st.subheader("💾 Disk Usage")
        if st.button("Refresh Disk Stats"):
            disk = psutil.disk_usage('/')
            st.metric("Total Disk", f"{disk.total / (1024 ** 3):.2f} GB")
            st.metric("Used Disk", f"{disk.used / (1024 ** 3):.2f} GB")
            st.metric("Free Disk", f"{disk.free / (1024 ** 3):.2f} GB")
            st.progress(disk.percent / 100)

    # WhatsApp Sender Page
    elif page == "WhatsApp Sender":
        st.title("📱 WhatsApp Message Sender")
        tab1, tab2 = st.tabs(["WhatsApp Web Automation", "Twilio API"])

        with tab1:
            st.header("Send via WhatsApp Web")
            st.markdown("Send messages by automating WhatsApp Web in your browser.")
            st.info("⚠️ Make sure you're logged into WhatsApp Web in your default browser.")
            with st.form("whatsapp_form"):
                phone_number = st.text_input(
                    "📞 Phone Number (with country code)",
                    value="+91",
                    help="Include country code (e.g., +91 for India, +1 for USA)"
                )
                message = st.text_area(
                    "💬 Your Message",
                    height=100,
                    help="Type your message here",
                    key="pywhatkit_message"
                )
                col1, col2 = st.columns(2)
                with col1:
                    send_now = st.checkbox("Send Instantly", help="Send immediately (15 sec wait)")
                with col2:
                    delay_minutes = st.number_input("Delay (minutes)", min_value=1, max_value=60, value=2)
                submit_button = st.form_submit_button("🚀 Send via WhatsApp Web", use_container_width=True)

            if submit_button:
                if phone_number and message:
                    try:
                        with st.spinner("Opening WhatsApp Web..."):
                            if send_now:
                                kit.sendwhatmsg_instantly(
                                    phone_no=phone_number,
                                    message=message,
                                    wait_time=15
                                )
                            else:
                                now = datetime.datetime.now()
                                hour = now.hour
                                minute = now.minute + delay_minutes
                                if minute >= 60:
                                    hour += minute // 60
                                    minute = minute % 60
                                kit.sendwhatmsg(
                                    phone_no=phone_number,
                                    message=message,
                                    time_hour=hour,
                                    time_min=minute
                                )
                        st.success("✅ Message scheduled/sent successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please fill in both phone number and message")

        with tab2:
            st.header("Send via Twilio API")
            st.markdown("Send messages directly using the Twilio API (no browser needed).")
            
            with st.form("twilio_whatsapp_form"):
                account_sid = "AC235cb59aa9b6ea74f3a5eacd50650797"
                auth_token = "a182fee850b117d9561d28511efb619b"
                to_number = st.text_input(
                    "📞 Recipient's WhatsApp Number",
                    placeholder="e.g., +91XXXXXXXXXX",
                    help="Format: whatsapp:+[CountryCode][PhoneNumber]"
                )
                message = st.text_area("💬 Message", key="wa_message")
                submit_button_twilio = st.form_submit_button("📲 Send via Twilio", use_container_width=True)

            if submit_button_twilio:
                if all([account_sid, auth_token, to_number, message]):
                    try:
                        with st.spinner("Sending message via Twilio..."):
                            client = Client(account_sid, auth_token)
                            msg = client.messages.create(
                                body=message,
                                from_='whatsapp:+14155238886',  # Twilio's Sandbox Number
                                to=f"whatsapp:{to_number}"
                            )
                        st.success(f"✅ WhatsApp message sent successfully! SID: {msg.sid}")
                        
                    except Exception as e:
                        st.error(f"❌ Error sending message: {e}")
                else:
                    st.warning("⚠️ Please fill in all Twilio fields.")

    # Call Page
    elif page == "Call":
        st.title("📞 Make a Call")
        st.markdown("Use Twilio to make automated voice calls.")

        with st.form("call_form"):
            col1, col2 = st.columns(2)
            with col1:
                account_sid = "AC235cb59aa9b6ea74f3a5eacd50650797"
                auth_token = "a182fee850b117d9561d28511efb619b"
            with col2:
                twilio_number = "+17755499097"
                to_number = st.text_input("📱 Recipient's Number", help="The destination phone number, including the country code.")
            
            message_to_say = st.text_area("💬 Message to Speak", "Hello! This is a test call from Twilio using a Streamlit app. Have a great day!", height=100, help="This text will be converted to speech on the call.")
            submitted = st.form_submit_button("🚀 Place Call", use_container_width=True)

        if submitted:
            if not all([account_sid, auth_token, twilio_number, to_number, message_to_say]):
                st.warning("⚠️ Please fill in all the fields before placing the call.")
            else:
                try:
                    with st.spinner(f"Initiating call to {to_number}..."):
                        client = Client(account_sid, auth_token)
                        twiml_response = f'<Response><Say voice="alice" language="en-US">{message_to_say}</Say></Response>'
                        call = client.calls.create(to=to_number, from_=twilio_number, twiml=twiml_response)
                    st.success(f"✅ Call successfully initiated to {to_number}!")
                    st.info(f"**Call SID:** `{call.sid}`")
                    
                except TwilioRestException as e:
                    st.error(f"❌ Twilio Error: {e.msg}")
                    st.info("Please double-check your Account SID, Auth Token, and phone number formats.")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {e}")

    # SMS Page
    elif page == "SMS":
        st.title("✉️ Send SMS with Twilio")
        st.markdown("Use the Twilio API to send SMS messages.")

        with st.form("sms_form"):
            st.subheader("Twilio Credentials")
            col1, col2 = st.columns(2)
            with col1:
                account_sid = 'AC235cb59aa9b6ea74f3a5eacd50650797'
                auth_token = 'a182fee850b117d9561d28511efb619b'
            with col2:
                    twilio_number = '+17755499097'
            
            st.subheader("Message Details")
            to_number = st.text_input("📱 Recipient's Number")
            message_body = st.text_area("💬 SMS Message")
            
            submitted_sms = st.form_submit_button("🚀 Send SMS", use_container_width=True)

        if submitted_sms:
            if not all([account_sid, auth_token, twilio_number, to_number, message_body]):
                st.warning("⚠️ Please fill in all fields.")
            else:
                try:
                    with st.spinner("Sending SMS..."):
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                            body=message_body,
                            from_=twilio_number,
                            to=to_number
                        )
                    st.success(f"✅ SMS sent successfully! Message SID: {message.sid}")
                    
                
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")

    # Email Sender Page
    elif page == "Email Sender":
        st.title("📧 Email Sender (via Gmail)")
        st.markdown("Send emails securely using your Gmail account.")
        st.info("💡 Use an **App Password** from your Google Account settings, not your regular password.")

        with st.form("gmail_form"):
            col1, col2 = st.columns(2)
            with col1:
                sender_gmail = st.text_input("📤 From (Your Gmail):", help="Your Gmail address")
                password_gmail = st.text_input("🔐 App Password:", type="password", help="Gmail App Password")
            with col2:
                to_gmail = st.text_input("📥 To:", help="Recipient's email")
                subject_gmail = st.text_input("📝 Subject:", help="Email subject line")
            
            message_body_gmail = st.text_area("💬 Message:", height=150, help="Email content", key="gmail_body")
            send_button_gmail = st.form_submit_button("📧 Send via Gmail", use_container_width=True)

        if send_button_gmail:
            if all([sender_gmail, password_gmail, to_gmail, subject_gmail, message_body_gmail]):
                try:
                    with st.spinner("Sending email..."):
                        message = MIMEMultipart()
                        message["From"] = sender_gmail
                        message["To"] = to_gmail
                        message["Subject"] = subject_gmail
                        message.attach(MIMEText(message_body_gmail, "plain"))
                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls()
                            server.login(sender_gmail, password_gmail)
                            server.send_message(message)
                    st.success("✅ Email sent successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Failed to send email: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all required fields")

    # Instagram Poster Page
    elif page == "Instagram Poster":
        st.title("📸 Instagram Post Uploader")

        if 'insta_client' not in st.session_state:
            st.session_state.insta_client = InstaClient()
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        with st.expander("🔐 Login to Instagram", expanded=not st.session_state.logged_in):
            username = st.text_input("Enter Instagram Username")
            password = st.text_input("Enter Password", type="password")
            login_btn = st.button("Login")
            if login_btn:
                if username and password:
                    with st.spinner("Logging in..."):
                        try:
                            st.session_state.insta_client.login(username, password)
                            st.session_state.logged_in = True
                            st.success("✅ Logged in successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Login failed: {e}")
                else:
                    st.warning("Please enter both username and password.")

        if st.session_state.logged_in:
            st.subheader(f"📤 Upload Your Post as @{st.session_state.insta_client.username}")
            uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
            caption = st.text_area("Enter caption for the post")

            if st.button("Post to Instagram"):
                if uploaded_file is not None and caption:
                    image_path = f"temp_{uploaded_file.name}"
                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    with st.spinner("Uploading post..."):
                        try:
                            st.session_state.insta_client.photo_upload(path=image_path, caption=caption)
                            st.success("✅ Post uploaded to Instagram!")
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ Failed to post: {e}")
                        finally:
                            if os.path.exists(image_path):
                                os.remove(image_path)
                else:
                    st.warning("⚠️ Please upload an image and write a caption.")
        else:
            st.info("Please log in first to post.")

    # Web Search Page
    elif page == "Web Search":
        st.title("🔍 Anonymous Web Search")
        st.markdown("Search the web using DuckDuckGo without tracking")
        def duckduckgo_search(query, num_results=10):
            try:
                url = "https://html.duckduckgo.com/html/"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                response = requests.post(url, headers=headers, data={"q": query}, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                results = []
                for link in soup.find_all("a", class_="result__a", href=True)[:num_results]:
                    title = link.get_text().strip()
                    href = link['href']
                    if title and href:
                        results.append({"title": title, "link": href})
                return results
            except Exception as e:
                st.error(f"Search error: {str(e)}")
                return []
        with st.form("search_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                query = st.text_input("🔍 Enter search query:", placeholder="What do you want to search?")
            with col2:
                num_results = st.number_input("Results:", min_value=5, max_value=20, value=10)
            search_button = st.form_submit_button("🚀 Search", use_container_width=True)
        if search_button and query:
            with st.spinner(f"Searching for '{query}'..."):
                results = duckduckgo_search(query, num_results)
            if results:
                st.success(f"✅ Found {len(results)} results for '{query}'")
                for i, result in enumerate(results, 1):
                    with st.expander(f"{i}. {result['title']}", expanded=False):
                        st.write(f"🔗 **Link:** {result['link']}")
                        st.link_button(f"Open Link {i}", url=result['link'])
            else:
                st.warning("❌ No results found or search was blocked")

    # Website Data Extractor Page
    elif page == "Website Data Extractor":
        st.title("🌐 Website Data Extractor")
        st.markdown("Extract and download data from any website")
        def extract_website_data(url):
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                data = {
                    "title": soup.title.string if soup.title else "No title",
                    "paragraphs": [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()],
                    "links": [{"text": a.get_text().strip(), "url": a.get('href')} for a in soup.find_all('a', href=True) if a.get_text().strip()],
                    "images": [img.get('src') for img in soup.find_all('img', src=True)],
                    "headings": [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
                    "raw_html": response.text
                }
                return data
            except Exception as e:
                return {"error": str(e)}
        with st.form("extractor_form"):
            url = st.text_input("🌐 Website URL:", placeholder="https://example.com")
            extract_options = st.multiselect(
                "📊 Data to extract:",
                ["Title", "Paragraphs", "Links", "Images", "Headings", "Raw HTML"],
                default=["Title", "Paragraphs", "Links"]
            )
            extract_button = st.form_submit_button("🔍 Extract Data", use_container_width=True)
        if extract_button and url:
            with st.spinner(f"Extracting data from {url}..."):
                data = extract_website_data(url)
            if "error" in data:
                st.error(f"❌ Error: {data['error']}")
            else:
                st.success("✅ Data extracted successfully!")
                if "Title" in extract_options and data.get("title"):
                    st.subheader("📝 Page Title"); st.write(data["title"])
                if "Paragraphs" in extract_options and data.get("paragraphs"):
                    st.subheader("📄 Paragraphs")
                    for i, p in enumerate(data["paragraphs"][:10], 1): st.write(f"{i}. {p}")
                if "Links" in extract_options and data.get("links"):
                    st.subheader("🔗 Links")
                    for link in data["links"][:20]: st.write(f"• [{link['text']}]({link['url']})")
                if "Images" in extract_options and data.get("images"):
                    st.subheader("🖼️ Images")
                    for img in data["images"][:10]: st.write(f"• {img}")
                if "Headings" in extract_options and data.get("headings"):
                    st.subheader("📋 Headings")
                    for heading in data["headings"]: st.write(f"• {heading}")
                if "Raw HTML" in extract_options and data.get("raw_html"):
                    st.download_button("📥 Download HTML", data["raw_html"], file_name=f"data_{url.replace('https://', '').replace('/', '_')}.html", mime="text/html")

    # Image Generator Page
    elif page == "Image Generator":
        st.title("🎨 Digital Image Creator")
        st.markdown("Create custom digital images using Python")
        def create_gradient_image(width, height, color1, color2, direction):
            img = Image.new('RGB', (width, height)); draw = ImageDraw.Draw(img)
            if direction == "Horizontal":
                for x in range(width):
                    r = int(color1[0] * (1 - x/width) + color2[0] * (x/width)); g = int(color1[1] * (1 - x/width) + color2[1] * (x/width)); b = int(color1[2] * (1 - x/width) + color2[2] * (x/width))
                    draw.line([(x, 0), (x, height)], fill=(r, g, b))
            else:
                for y in range(height):
                    r = int(color1[0] * (1 - y/height) + color2[0] * (y/height)); g = int(color1[1] * (1 - y/height) + color2[1] * (y/height)); b = int(color1[2] * (1 - y/height) + color2[2] * (y/height))
                    draw.line([(0, y), (width, y)], fill=(r, g, b))
            return img
        def create_pattern_image(width, height, pattern_type, color):
            img = Image.new('RGB', (width, height), 'white'); draw = ImageDraw.Draw(img)
            if pattern_type == "Circles":
                for x in range(0, width, 50):
                    for y in range(0, height, 50): draw.ellipse([x, y, x + 40, y + 40], fill=color)
            elif pattern_type == "Squares":
                for x in range(0, width, 60):
                    for y in range(0, height, 60): draw.rectangle([x, y, x + 50, y + 50], fill=color)
            elif pattern_type == "Lines":
                for x in range(0, width, 20): draw.line([(x, 0), (x, height)], fill=color, width=3)
            return img
        tab1, tab2, tab3 = st.tabs(["🌈 Gradient", "🔶 Patterns", "✨ Effects"])
        with tab1:
            st.subheader("Create Gradient Image")
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("Width:", 100, 2000, 800, key="grad_width"); height = st.number_input("Height:", 100, 2000, 600, key="grad_height"); direction = st.selectbox("Direction:", ["Horizontal", "Vertical"])
            with col2:
                color1 = st.color_picker("Start Color:", "#FF0000"); color2 = st.color_picker("End Color:", "#0000FF")
            if st.button("🎨 Generate Gradient", key="grad_btn"):
                c1_rgb = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5)); c2_rgb = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
                img = create_gradient_image(width, height, c1_rgb, c2_rgb, direction)
                st.image(img, caption="Generated Gradient Image"); buf = io.BytesIO(); img.save(buf, format='PNG')
                st.download_button("📥 Download Image", buf.getvalue(), "gradient.png", "image/png")
        with tab2:
            st.subheader("Create Pattern Image")
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("Width:", 100, 2000, 800, key="pat_width"); height = st.number_input("Height:", 100, 2000, 600, key="pat_height")
            with col2:
                pattern_type = st.selectbox("Pattern:", ["Circles", "Squares", "Lines"]); color = st.color_picker("Pattern Color:", "#FF5733")
            if st.button("🔶 Generate Pattern", key="pat_btn"):
                color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                img = create_pattern_image(width, height, pattern_type, color_rgb)
                st.image(img, caption="Generated Pattern Image"); buf = io.BytesIO(); img.save(buf, format='PNG')
                st.download_button("📥 Download Image", buf.getvalue(), "pattern.png", "image/png")
        with tab3:
            st.subheader("Apply Effects to Images")
            uploaded_file = st.file_uploader("Upload an image:", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                img = Image.open(uploaded_file); st.image(img, caption="Original Image", width=300)
                effect = st.selectbox("Choose Effect:", ["Blur", "Sharpen", "Edge Enhance"])
                if st.button("✨ Apply Effect"):
                    if effect == "Blur": processed_img = img.filter(ImageFilter.BLUR)
                    elif effect == "Sharpen": processed_img = img.filter(ImageFilter.SHARPEN)
                    else: processed_img = img.filter(ImageFilter.EDGE_ENHANCE)
                    st.image(processed_img, caption=f"{effect} Effect", width=300); buf = io.BytesIO(); processed_img.save(buf, format='PNG')
                    st.download_button("📥 Download Processed Image", buf.getvalue(), f"{effect.lower()}.png", "image/png")

    # Face Swap Page
    elif page == "Face Swap":
        st.title("🔄 Face Swap Tool")
        st.markdown("Swap faces between two images using OpenCV")
        st.info("⚠️ This is a basic face swap implementation. Upload two clear images with visible faces.")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📸 Image 1 (Source Face)"); img1_file = st.file_uploader("Upload first image:", type=['png', 'jpg', 'jpeg'], key="img1")
        with col2:
            st.subheader("📸 Image 2 (Target Face)"); img2_file = st.file_uploader("Upload second image:", type=['png', 'jpg', 'jpeg'], key="img2")
        if img1_file and img2_file:
            col3, col4 = st.columns(2)
            with col3:
                img1 = Image.open(img1_file); st.image(img1, caption="Image 1", width=300)
            with col4:
                img2 = Image.open(img2_file); st.image(img2, caption="Image 2", width=300)
            if st.button("🔄 Swap Faces"):
                try:
                    img1_cv = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR); img2_cv = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    faces1 = face_cascade.detectMultiScale(img1_cv, 1.3, 5); faces2 = face_cascade.detectMultiScale(img2_cv, 1.3, 5)
                    if len(faces1) > 0 and len(faces2) > 0:
                        x1,y1,w1,h1 = faces1[0]; x2,y2,w2,h2 = faces2[0]
                        face1 = img1_cv[y1:y1+h1, x1:x1+w1]; face2 = img2_cv[y2:y2+h2, x2:x2+w2]
                        face1_resized = cv2.resize(face1, (w2, h2)); face2_resized = cv2.resize(face2, (w1, h1))
                        swapped1 = img1_cv.copy(); swapped2 = img2_cv.copy()
                        swapped1[y1:y1+h1, x1:x1+w1] = face2_resized; swapped2[y2:y2+h2, x2:x2+w2] = face1_resized
                        s1_rgb = cv2.cvtColor(swapped1, cv2.COLOR_BGR2RGB); s2_rgb = cv2.cvtColor(swapped2, cv2.COLOR_BGR2RGB)
                        st.success("✅ Face swap completed!")
                        col5, col6 = st.columns(2)
                        with col5:
                            st.image(s1_rgb, caption="Swapped Image 1", width=300); buf1 = io.BytesIO(); Image.fromarray(s1_rgb).save(buf1, format='PNG')
                            st.download_button("📥 Download Swapped Image 1", buf1.getvalue(), "swap1.png", "image/png", key="d1")
                        with col6:
                            st.image(s2_rgb, caption="Swapped Image 2", width=300); buf2 = io.BytesIO(); Image.fromarray(s2_rgb).save(buf2, format='PNG')
                            st.download_button("📥 Download Swapped Image 2", buf2.getvalue(), "swap2.png", "image/png", key="d2")
                    else:
                        st.error("❌ Could not detect faces in one or both images.")
                except Exception as e:
                    st.error(f"❌ Face swap failed: {e}")
                    st.info("💡 Try using images with clear, front-facing faces.")



    # --- Main App Execution ---
    if __name__ == '__main__':
        # To run the app, save this code as a Python file (e.g., app.py) and run `streamlit run app.py` in your terminal.
        # You will also need to install the required libraries:
        # pip install streamlit psutil pywhatkit beautifulsoup4 opencv-python-headless Pillow twilio instagrapi
        pass



        

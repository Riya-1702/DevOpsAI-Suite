import streamlit as st
import streamlit.components.v1 as components
import json
import requests
import base64
import io
from PIL import Image

def run():

    st.header("🌐 Interactive Web Development Tools")
    st.markdown("""
    Welcome to the Interactive Web Development module!  
    Here you can test live JavaScript functionality directly in your browser.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚀 Quick Start")
        framework = st.selectbox("Choose a framework:", ["Flask", "Django", "FastAPI", "Streamlit"])
        if st.button("Generate Starter Project"):
            st.success(f"Starter project for {framework} generated! (Scaffolding logic to be implemented)")
    with col2:
        st.subheader("🧰 Live Utilities")
        st.write("✅ HTML/CSS/JS Interactive Demos")
        st.write("✅ Working Media Capture")
        st.write("✅ Live Speech Recognition")

    st.subheader("📚 Resources")
    st.markdown("""
    - [MDN Web Docs](https://developer.mozilla.org/)
    - [W3Schools](https://www.w3schools.com/)
    - [FreeCodeCamp](https://www.freecodecamp.org/)
    """)

    tool_category = st.sidebar.selectbox(
        "Select Interactive Demo:",
        ["📷 Media Capture", "🎤 Speech & Audio", "🤖 AI Integration", "📱 Social Media", "🔍 Search & Scraping", "🖱️ Interactive Elements"]
    )
    
    if tool_category == "📷 Media Capture":
        show_media_capture()
    elif tool_category == "🎤 Speech & Audio":
        show_speech_audio()
    elif tool_category == "🤖 AI Integration":
        show_ai_integration()
    elif tool_category == "📱 Social Media":
        show_social_media()
    elif tool_category == "🔍 Search & Scraping":
        show_search_scraping()
    elif tool_category == "🖱️ Interactive Elements":
        show_interactive_elements()

def show_media_capture():
    """Show working media capture tools"""
    st.header("📷 Live Media Capture Demo")
    st.markdown("**This demo provides working camera access and photo capture functionality:**")
    
    # Working Media Capture HTML/JS
    media_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: Arial, sans-serif; }
            .video-container { margin: 20px 0; }
            video { max-width: 100%; height: 300px; background: #000; }
            canvas { max-width: 100%; margin: 10px 0; }
            button { 
                padding: 10px 20px; 
                margin: 5px; 
                background: #ff4b4b; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
            }
            button:hover { background: #ff6b6b; }
            .status { padding: 10px; background: #f0f0f0; margin: 10px 0; border-radius: 5px; }
            .photo-preview { margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>📷 Live Camera Demo</h3>
            <div class="video-container">
                <video id="video" autoplay muted></video>
                <canvas id="canvas" style="display: none;"></canvas>
            </div>
            
            <div>
                <button onclick="startCamera()">Start Camera</button>
                <button onclick="takePhoto()">Take Photo</button>
                <button onclick="stopCamera()">Stop Camera</button>
            </div>
            
            <div id="status" class="status">Click "Start Camera" to begin</div>
            
            <div class="photo-preview">
                <h4>Captured Photo:</h4>
                <img id="photo" style="max-width: 100%; display: none;" />
            </div>
        </div>

        <script>
            let stream = null;
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            const photo = document.getElementById('photo');
            const status = document.getElementById('status');

            async function startCamera() {
                try {
                    stream = await navigator.mediaDevices.getUserMedia({ 
                        video: { width: 640, height: 480 } 
                    });
                    video.srcObject = stream;
                    status.innerHTML = '✅ Camera started successfully!';
                    status.style.background = '#d4edda';
                } catch (error) {
                    status.innerHTML = '❌ Error: ' + error.message;
                    status.style.background = '#f8d7da';
                }
            }

            function takePhoto() {
                if (!stream) {
                    status.innerHTML = '⚠️ Please start camera first';
                    status.style.background = '#fff3cd';
                    return;
                }
                
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0);
                
                const dataUrl = canvas.toDataURL('image/png');
                photo.src = dataUrl;
                photo.style.display = 'block';
                
                status.innerHTML = '📸 Photo captured successfully!';
                status.style.background = '#d1ecf1';
            }

            function stopCamera() {
                if (stream) {
                    stream.getTracks().forEach(track => track.stop());
                    video.srcObject = null;
                    stream = null;
                    status.innerHTML = '🔴 Camera stopped';
                    status.style.background = '#f0f0f0';
                }
            }
        </script>
    </body>
    </html>
    """
    
    components.html(media_html, height=700)
    
    st.markdown("---")
    st.subheader("📹 Video Recording Demo")
    
    video_record_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: Arial, sans-serif; }
            video { max-width: 100%; height: 250px; background: #000; margin: 10px 0; }
            button { 
                padding: 10px 20px; 
                margin: 5px; 
                background: #ff4b4b; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
            }
            button:hover { background: #ff6b6b; }
            .recording { background: #dc3545 !important; }
            .status { padding: 10px; background: #f0f0f0; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>📹 Video Recording Demo</h3>
            <video id="liveVideo" autoplay muted></video>
            
            <div>
                <button id="startBtn" onclick="startRecording()">Start Recording</button>
                <button id="stopBtn" onclick="stopRecording()" disabled>Stop Recording</button>
            </div>
            
            <div id="recordStatus" class="status">Ready to record</div>
            
            <h4>Recorded Video:</h4>
            <video id="recordedVideo" controls style="display: none;"></video>
        </div>

        <script>
            let mediaRecorder;
            let recordedChunks = [];
            let stream;

            const liveVideo = document.getElementById('liveVideo');
            const recordedVideo = document.getElementById('recordedVideo');
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            const status = document.getElementById('recordStatus');

            async function startRecording() {
                try {
                    stream = await navigator.mediaDevices.getUserMedia({ 
                        video: true, 
                        audio: true 
                    });
                    liveVideo.srcObject = stream;

                    mediaRecorder = new MediaRecorder(stream);
                    recordedChunks = [];

                    mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            recordedChunks.push(event.data);
                        }
                    };

                    mediaRecorder.onstop = () => {
                        const blob = new Blob(recordedChunks, { type: 'video/webm' });
                        const url = URL.createObjectURL(blob);
                        recordedVideo.src = url;
                        recordedVideo.style.display = 'block';
                        
                        // Stop camera stream
                        stream.getTracks().forEach(track => track.stop());
                        liveVideo.srcObject = null;
                    };

                    mediaRecorder.start();
                    
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                    startBtn.classList.add('recording');
                    status.innerHTML = '🔴 Recording in progress...';
                    status.style.background = '#f8d7da';

                } catch (error) {
                    status.innerHTML = '❌ Error: ' + error.message;
                    status.style.background = '#f8d7da';
                }
            }

            function stopRecording() {
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                    
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                    startBtn.classList.remove('recording');
                    status.innerHTML = '✅ Recording saved! Check video below.';
                    status.style.background = '#d4edda';
                }
            }
        </script>
    </body>
    </html>
    """
    
    components.html(video_record_html, height=600)

def show_speech_audio():
    """Show working speech and audio tools"""
    st.header("🎤 Live Speech & Audio Demo")
    st.markdown("**Working speech recognition and text-to-speech functionality:**")
    
    # Working Speech Recognition HTML/JS
    speech_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: Arial, sans-serif; }
            button { 
                padding: 12px 24px; 
                margin: 8px; 
                background: #ff4b4b; 
                color: white; 
                border: none; 
                border-radius: 6px; 
                cursor: pointer; 
                font-size: 16px;
            }
            button:hover { background: #ff6b6b; }
            button:disabled { background: #ccc; cursor: not-allowed; }
            .listening { background: #28a745 !important; }
            .output { 
                padding: 15px; 
                background: #f8f9fa; 
                margin: 15px 0; 
                border-radius: 8px; 
                border-left: 4px solid #007bff;
                min-height: 60px;
            }
            .interim { color: #666; font-style: italic; }
            .final { color: #000; font-weight: bold; }
            .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
            input[type="text"] { 
                width: 70%; 
                padding: 10px; 
                margin: 5px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>🎤 Speech Recognition Demo</h3>
            <div>
                <button id="startSpeech" onclick="startSpeechRecognition()">Start Listening</button>
                <button id="stopSpeech" onclick="stopSpeechRecognition()" disabled>Stop Listening</button>
            </div>
            
            <div id="speechStatus" class="status">Click "Start Listening" to begin</div>
            
            <div class="output">
                <h4>Live Transcript:</h4>
                <p id="interimResults" class="interim">Interim results will appear here...</p>
                <p id="finalResults" class="final">Final results will appear here...</p>
            </div>

            <hr style="margin: 30px 0;">
            
            <h3>🔊 Text-to-Speech Demo</h3>
            <div>
                <input type="text" id="textToSpeak" placeholder="Enter text to speak..." value="Hello! This is a text-to-speech demo.">
                <button onclick="speakText()">Speak Text</button>
                <button onclick="stopSpeaking()">Stop Speaking</button>
            </div>
            
            <div>
                <label>Voice: </label>
                <select id="voiceSelect" onchange="updateVoice()"></select>
                <label>Speed: </label>
                <input type="range" id="speedRange" min="0.5" max="2" step="0.1" value="1" onchange="updateSpeed()">
                <span id="speedValue">1</span>
            </div>
        </div>

        <script>
            let recognition;
            let isListening = false;
            let voices = [];
            let selectedVoice = null;
            let speechRate = 1;

            // Initialize speech recognition
            function initSpeechRecognition() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    
                    recognition.continuous = true;
                    recognition.interimResults = true;
                    recognition.lang = 'en-US';
                    
                    recognition.onresult = (event) => {
                        let interimTranscript = '';
                        let finalTranscript = '';
                        
                        for (let i = event.resultIndex; i < event.results.length; i++) {
                            const transcript = event.results[i][0].transcript;
                            if (event.results[i].isFinal) {
                                finalTranscript += transcript + ' ';
                            } else {
                                interimTranscript += transcript;
                            }
                        }
                        
                        document.getElementById('interimResults').textContent = interimTranscript;
                        if (finalTranscript) {
                            document.getElementById('finalResults').textContent += finalTranscript;
                        }
                    };
                    
                    recognition.onstart = () => {
                        document.getElementById('speechStatus').innerHTML = '🎤 Listening... Speak now!';
                        document.getElementById('speechStatus').style.background = '#d4edda';
                    };
                    
                    recognition.onend = () => {
                        isListening = false;
                        document.getElementById('startSpeech').disabled = false;
                        document.getElementById('stopSpeech').disabled = true;
                        document.getElementById('startSpeech').classList.remove('listening');
                        document.getElementById('speechStatus').innerHTML = 'Speech recognition stopped';
                        document.getElementById('speechStatus').style.background = '#f0f0f0';
                    };
                    
                    recognition.onerror = (event) => {
                        document.getElementById('speechStatus').innerHTML = '❌ Error: ' + event.error;
                        document.getElementById('speechStatus').style.background = '#f8d7da';
                    };
                } else {
                    document.getElementById('speechStatus').innerHTML = '❌ Speech recognition not supported in this browser';
                    document.getElementById('speechStatus').style.background = '#f8d7da';
                }
            }

            function startSpeechRecognition() {
                if (recognition && !isListening) {
                    recognition.start();
                    isListening = true;
                    document.getElementById('startSpeech').disabled = true;
                    document.getElementById('stopSpeech').disabled = false;
                    document.getElementById('startSpeech').classList.add('listening');
                    document.getElementById('finalResults').textContent = '';
                    document.getElementById('interimResults').textContent = '';
                }
            }

            function stopSpeechRecognition() {
                if (recognition && isListening) {
                    recognition.stop();
                }
            }

            // Initialize text-to-speech
            function initTextToSpeech() {
                if ('speechSynthesis' in window) {
                    voices = speechSynthesis.getVoices();
                    if (voices.length === 0) {
                        speechSynthesis.onvoiceschanged = () => {
                            voices = speechSynthesis.getVoices();
                            populateVoices();
                        };
                    } else {
                        populateVoices();
                    }
                }
            }

            function populateVoices() {
                const voiceSelect = document.getElementById('voiceSelect');
                voiceSelect.innerHTML = '';
                
                voices.forEach((voice, index) => {
                    const option = document.createElement('option');
                    option.value = index;
                    option.textContent = voice.name + ' (' + voice.lang + ')';
                    voiceSelect.appendChild(option);
                });
                
                selectedVoice = voices[0];
            }

            function updateVoice() {
                const voiceSelect = document.getElementById('voiceSelect');
                selectedVoice = voices[voiceSelect.value];
            }

            function updateSpeed() {
                const speedRange = document.getElementById('speedRange');
                speechRate = speedRange.value;
                document.getElementById('speedValue').textContent = speechRate;
            }

            function speakText() {
                if ('speechSynthesis' in window) {
                    const text = document.getElementById('textToSpeak').value;
                    if (text.trim() === '') return;
                    
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.voice = selectedVoice;
                    utterance.rate = speechRate;
                    
                    speechSynthesis.speak(utterance);
                } else {
                    alert('Text-to-speech not supported in this browser');
                }
            }

            function stopSpeaking() {
                if ('speechSynthesis' in window) {
                    speechSynthesis.cancel();
                }
            }

            // Initialize everything
            window.onload = function() {
                initSpeechRecognition();
                initTextToSpeech();
            };
        </script>
    </body>
    </html>
    """
    
    components.html(speech_html, height=800)

def show_ai_integration():
    """Show AI integration demo updated for Google Gemini API."""
    st.header("🤖 AI Integration Demo")
    st.markdown("**AI Integration Interface (Now configured for Google Gemini API):**")
    
    ai_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: Arial, sans-serif; }
            .chat-container { 
                background: #f8f9fa; 
                border-radius: 8px; 
                padding: 20px; 
                margin: 20px 0; 
                min-height: 200px;
                border: 1px solid #dee2e6;
            }
            .input-group { margin: 15px 0; }
            input[type="password"], input[type="text"], textarea { 
                width: 90%; 
                padding: 10px; 
                margin: 5px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
                font-size: 14px;
            }
            textarea { height: 80px; resize: vertical; }
            button { 
                padding: 10px 20px; 
                margin: 5px; 
                background: #ff4b4b; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
            }
            button:hover { background: #ff6b6b; }
            .response { 
                background: white; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 10px 0; 
                border-left: 4px solid #007bff;
                white-space: pre-wrap; 
                max-height: 400px;
                overflow-y: auto;
            }
            .api-status {
                background: #d4edda;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                border-left: 4px solid #28a745;
            }
            .loading {
                background: #fff3cd;
                padding: 10px;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
            }
            .error {
                background: #f8d7da;
                padding: 10px;
                border-radius: 5px;
                border-left: 4px solid #dc3545;
            }
            .image-container {
                text-align: center;
                margin: 10px 0;
            }
            .generated-image {
                max-width: 100%;
                max-height: 400px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="api-status">
                <strong>API Status:</strong> Gemini API key is configured and ready to use!
            </div>
            
            <h3>💬 Gemini Integration</h3>
            <div class="input-group">
                <input type="password" id="geminiApiKey" value="AIzaSyDWNLYg0mwmAt2gHWKO6Nea0GhnXBgMtec" placeholder="Your Gemini API Key">
                <small style="color: #666;">API key is pre-configured</small>
            </div>
            
            <div class="input-group">
                <textarea id="promptInput" placeholder="Enter your prompt here...">Explain quantum computing in simple terms</textarea>
                <button onclick="sendToGemini()">Send to Gemini</button>
                <button onclick="voicePrompt()">Voice Input</button>
            </div>
            
            <div class="chat-container">
                <h4>Gemini Response:</h4>
                <div id="chatResponse" class="response">Response will appear here...</div>
            </div>
            
            <h3>🖼️ AI Image Generation</h3>
            <div class="input-group">
                <input type="text" id="imagePrompt" placeholder="Describe the image you want to generate..." value="A beautiful sunset over mountains">
                <button onclick="generateImage()">Generate Image</button>
            </div>
            
            <div class="chat-container">
                <h4>Generated Image:</h4>
                <div id="imageContainer" class="image-container">
                    <div id="imageStatus">Click "Generate Image" to create an AI-generated image</div>
                </div>
            </div>
             
            <h3>🎤 Voice + AI Integration</h3>
            <div class="input-group">
                <button onclick="startVoiceToAI()">Start Voice Recognition & Send</button>
                <button onclick="stopVoiceToAI()">Stop</button>
            </div>
            <div id="voiceTranscript" class="response">Voice input will appear here...</div>
        </div>

        <script>
            let recognition;
            let isVoiceActive = false;

            // --- Gemini API Call ---
            async function sendToGemini() {
                const prompt = document.getElementById('promptInput').value;
                const apiKey = document.getElementById('geminiApiKey').value;
                const responseDiv = document.getElementById('chatResponse');
                
                if (!prompt.trim()) {
                    responseDiv.innerHTML = '<div class="error">Please enter a prompt.</div>';
                    return;
                }
                
                if (!apiKey || !apiKey.trim()) {
                    responseDiv.innerHTML = '<div class="error">Please enter your Google Gemini API key.</div>';
                    return;
                }

                responseDiv.innerHTML = '<div class="loading">🤖 Generating response...</div>';
                
                // Updated Gemini API endpoint for the latest version
                const apiURL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${apiKey.trim()}`;

                try {
                    const response = await fetch(apiURL, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            "contents": [{
                                "parts": [{
                                    "text": prompt
                                }]
                            }],
                            "generationConfig": {
                                "temperature": 0.9,
                                "topK": 1,
                                "topP": 1,
                                "maxOutputTokens": 2048
                            },
                            "safetySettings": [
                                {
                                    "category": "HARM_CATEGORY_HARASSMENT",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                },
                                {
                                    "category": "HARM_CATEGORY_HATE_SPEECH",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                },
                                {
                                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                },
                                {
                                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                }
                            ]
                        })
                    });
                    
                    if (!response.ok) {
                        const errorText = await response.text();
                        console.error('API Error Response:', errorText);
                        throw new Error(`API Error: ${response.status} - ${errorText}`);
                    }

                    const data = await response.json();
                    console.log('Full API Response:', data);
                    
                    // Extract the text from the Gemini response structure
                    if (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0]) {
                        const text = data.candidates[0].content.parts[0].text;
                        responseDiv.innerHTML = `<div style="color: #333;">${text}</div>`;
                    } else if (data.candidates && data.candidates[0] && data.candidates[0].finishReason) {
                        responseDiv.innerHTML = `<div class="error">Response blocked due to: ${data.candidates[0].finishReason}</div>`;
                    } else {
                        responseDiv.innerHTML = `<div class="error">Unexpected response format. Check console for details.</div>`;
                        console.error('Unexpected response structure:', data);
                    }

                } catch (error) {
                    console.error("Error:", error);
                    responseDiv.innerHTML = `<div class="error">Error: ${error.message}<br><br>💡 Tips:<br>• Make sure your API key is valid<br>• Enable the Gemini API in Google AI Studio<br>• Check your internet connection</div>`;
                }
            }

            // --- AI Image Generation using Picsum (placeholder) + AI enhancement ---
            async function generateImage() {
                const prompt = document.getElementById('imagePrompt').value;
                const imageContainer = document.getElementById('imageContainer');
                const imageStatus = document.getElementById('imageStatus');
                
                if (!prompt.trim()) {
                    imageStatus.innerHTML = '<div class="error">Please enter an image description.</div>';
                    return;
                }
                
                imageStatus.innerHTML = '<div class="loading">🎨 Generating AI image...</div>';
                
                try {
                    // For demonstration, we'll use a combination of approaches:
                    // 1. Generate a placeholder image
                    // 2. Show how you would integrate with actual AI image services
                    
                    // Simulate AI image generation delay
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    
                    // Generate a random image from Picsum with specific dimensions
                    const imageId = Math.floor(Math.random() * 1000) + 1;
                    const imageUrl = `https://picsum.photos/512/512?random=${imageId}`;
                    
                    // Create image element
                    const img = document.createElement('img');
                    img.src = imageUrl;
                    img.alt = prompt;
                    img.className = 'generated-image';
                    
                    // Clear container and add new image
                    imageContainer.innerHTML = '';
                    imageContainer.appendChild(img);
                    
                    // Add caption
                    const caption = document.createElement('div');
                    caption.style.marginTop = '10px';
                    caption.style.fontStyle = 'italic';
                    caption.style.color = '#666';
                    caption.innerHTML = `📸 Generated for: "${prompt}"<br><small>Note: This is a demo using placeholder images. In production, you would integrate with services like DALL-E, Midjourney API, or Stable Diffusion.</small>`;
                    imageContainer.appendChild(caption);
                    
                    // Add download button
                    const downloadBtn = document.createElement('button');
                    downloadBtn.textContent = 'Download Image';
                    downloadBtn.style.marginTop = '10px';
                    downloadBtn.onclick = () => {
                        const link = document.createElement('a');
                        link.href = imageUrl;
                        link.download = `ai-generated-${Date.now()}.jpg`;
                        link.click();
                    };
                    imageContainer.appendChild(downloadBtn);
                    
                } catch (error) {
                    imageStatus.innerHTML = `<div class="error">Error generating image: ${error.message}</div>`;
                }
            }

            // --- Voice Recognition Functions ---
            function voicePrompt() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition();
                    
                    recognition.onresult = (event) => {
                        const transcript = event.results[0][0].transcript;
                        document.getElementById('promptInput').value = transcript;
                    };
                    
                    recognition.onerror = (event) => {
                        alert('Speech recognition error: ' + event.error);
                    };
                    
                    recognition.start();
                } else {
                    alert('Speech recognition not supported in this browser.');
                }
            }

            function startVoiceToAI() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.continuous = true;
                    recognition.interimResults = true;
                    
                    recognition.onresult = (event) => {
                        const transcript = Array.from(event.results)
                            .map(result => result[0])
                            .map(result => result.transcript)
                            .join('');
                        
                        document.getElementById('voiceTranscript').textContent = 'Voice: ' + transcript;
                        
                        // Check if the result is final
                        if (event.results[event.results.length - 1].isFinal) {
                            document.getElementById('promptInput').value = transcript;
                            // Automatically send the final transcript to Gemini
                            setTimeout(() => {
                                sendToGemini();
                            }, 500);
                        }
                    };
                    
                    recognition.onstart = () => {
                         document.getElementById('voiceTranscript').innerHTML = '<div class="loading">🎤 Listening...</div>';
                    };
                    
                    recognition.onerror = (event) => {
                        document.getElementById('voiceTranscript').innerHTML = `<div class="error">Speech recognition error: ${event.error}</div>`;
                        isVoiceActive = false;
                    };

                    recognition.onend = () => {
                        isVoiceActive = false;
                    };

                    recognition.start();
                    isVoiceActive = true;
                } else {
                    alert('Speech recognition not supported in this browser.');
                }
            }

            function stopVoiceToAI() {
                if (recognition && isVoiceActive) {
                    recognition.stop();
                    isVoiceActive = false;
                    document.getElementById('voiceTranscript').textContent = 'Recognition stopped.';
                }
            }

            // Initialize on page load
            window.onload = function() {
                console.log('AI Integration Demo loaded successfully!');
            };
        </script>
    </body>
    </html>
    """
    
    components.html(ai_html, height=1200, scrolling=True)

def show_social_media():
    """Show social media integration demos"""
    st.header("📱 Social Media Integration Demo")
    st.markdown("**Working social media sharing functionality:**")
    
    social_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: Arial, sans-serif; }
            .share-section { 
                background: #f8f9fa; 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 8px; 
                border: 1px solid #dee2e6;
            }
            button { 
                padding: 10px 20px; 
                margin: 8px; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
                font-size: 14px;
            }
            .whatsapp { background: #25d366; }
            .whatsapp:hover { background: #128c7e; }
            .telegram { background: #0088cc; }
            .telegram:hover { background: #006699; }
            .twitter { background: #1da1f2; }
            .twitter:hover { background: #0d8bd9; }
            .facebook { background: #4267b2; }
            .facebook:hover { background: #365899; }
            .linkedin { background: #0077b5; }
            .linkedin:hover { background: #005885; }
            input[type="text"], textarea { 
                width: 90%; 
                padding: 10px; 
                margin: 5px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
            }
            textarea { height: 60px; resize: vertical; }
            .status { 
                padding: 10px; 
                margin: 10px 0; 
                border-radius: 5px; 
                background: #e9ecef;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>📱 Social Media Sharing</h3>
            
            <div class="share-section">
                <h4>📝 Content to Share</h4>
                <textarea id="shareText" placeholder="Enter text to share...">Check out this amazing web development tool!</textarea>
                <br>
                <input type="text" id="shareUrl" placeholder="URL to share (optional)" value="https://streamlit.io">
            </div>
            
            <div class="share-section">
                <h4>💬 WhatsApp</h4>
                <input type="text" id="whatsappNumber" placeholder="Phone number (optional, with country code)" value="">
                <br>
                <button class="whatsapp" onclick="shareToWhatsApp()">Share to WhatsApp</button>
                <button class="whatsapp" onclick="shareToWhatsAppWeb()">WhatsApp Web</button>
            </div>
            
            <div class="share-section">
                <h4>✈️ Telegram</h4>
                <input type="text" id="telegramUsername" placeholder="Telegram username (optional)" value="">
                <br>
                <button class="telegram" onclick="shareToTelegram()">Share to Telegram</button>
            </div>
            
            <div class="share-section">
                <h4>🐦 Twitter</h4>
                <button class="twitter" onclick="shareToTwitter()">Share to Twitter</button>
            </div>
            
            <div class="share-section">
                <h4>📘 Facebook</h4>
                <button class="facebook" onclick="shareToFacebook()">Share to Facebook</button>
            </div>
            
            <div class="share-section">
                <h4>💼 LinkedIn</h4>
                <button class="linkedin" onclick="shareToLinkedIn()">Share to LinkedIn</button>
            </div>
            
            <div class="share-section">
                <h4>📧 Email</h4>
                <input type="email" id="emailTo" placeholder="Recipient email (optional)" value="">
                <br>
                <button onclick="shareViaEmail()" style="background: #dc3545;">Send via Email</button>
            </div>
            
            <div id="status" class="status">Ready to share!</div>
        </div>

        <script>
            function updateStatus(message) {
                document.getElementById('status').textContent = message;
            }

            function shareToWhatsApp() {
                const text = document.getElementById('shareText').value;
                const url = document.getElementById('shareUrl').value;
                const number = document.getElementById('whatsappNumber').value;
                
                const message = url ? `${text} ${url}` : text;
                const whatsappUrl = number ? 
                    `https://wa.me/${number.replace(/\D/g, '')}?text=${encodeURIComponent(message)}` :
                    `whatsapp://send?text=${encodeURIComponent(message)}`;
                
                window.open(whatsappUrl, '_blank');
                updateStatus('Opening WhatsApp...');
            }

            function shareToWhatsAppWeb() {
                const text = document.getElementById('shareText').value;
                const url = document.getElementById('shareUrl').value;
                const message = url ? `${text} ${url}` : text;
                
                const whatsappWebUrl = `https://web.whatsapp.com/send?text=${encodeURIComponent(message)}`;
                window.open(whatsappWebUrl, '_blank');
                updateStatus('Opening WhatsApp Web...');
            }

            function shareToTelegram() {
                const text = document.getElementById('shareText').value;
                const url = document.getElementById('shareUrl').value;
                const username = document.getElementById('telegramUsername').value;
                
                const message = url ? `${text} ${url}` : text;
                const telegramUrl = username ?
                    `https://t.me/${username}?text=${encodeURIComponent(message)}` :
                    `https://t.me/share/url?url=${encodeURIComponent(url || '')}&text=${encodeURIComponent(text)}`;
                
                window.open(telegramUrl, '_blank');
                updateStatus('Opening Telegram...');
            }

            function shareToTwitter() {
                const text = document.getElementById('shareText').value;
                const url = document.getElementById('shareUrl').value;
                
                const tweetText = url ? `${text} ${url}` : text;
                const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}`;
                
                window.open(twitterUrl, '_blank');
                updateStatus('Opening Twitter...');
            }

            function shareToFacebook() {
                const url = document.getElementById('shareUrl').value || window.location.href;
                const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
                
                window.open(facebookUrl, '_blank');
                updateStatus('Opening Facebook...');
            }

            function shareToLinkedIn() {
                const text = document.getElementById('shareText').value;
                const url = document.getElementById('shareUrl').value || window.location.href;
                
                const linkedinUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
                
                window.open(linkedinUrl, '_blank');
                updateStatus('Opening LinkedIn...');
            }

            function shareViaEmail() {
                const text = document.getElementById('shareText').value;
                const url = document.getElementById('shareUrl').value;
                const to = document.getElementById('emailTo').value;
                
                const subject = 'Check this out!';
                const body = url ? `${text}\n\n${url}` : text;
                const emailUrl = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
                
                window.location.href = emailUrl;
                updateStatus('Opening email client...');
            }

            // Native sharing API (if supported)
            function nativeShare() {
                if (navigator.share) {
                    const text = document.getElementById('shareText').value;
                    const url = document.getElementById('shareUrl').value;
                    
                    navigator.share({
                        title: 'Shared Content',
                        text: text,
                        url: url
                    }).then(() => {
                        updateStatus('Content shared successfully!');
                    }).catch((error) => {
                        updateStatus('Error sharing: ' + error.message);
                    });
                } else {
                    updateStatus('Native sharing not supported in this browser');
                }
            }

            // Add native share button if supported
            window.onload = function() {
                if (navigator.share) {
                    const container = document.querySelector('.container');
                    const nativeSection = document.createElement('div');
                    nativeSection.className = 'share-section';
                    nativeSection.innerHTML = `
                        <h4>📤 Native Sharing</h4>
                        <button onclick="nativeShare()" style="background: #28a745;">Use Device Share Menu</button>
                    `;
                    container.appendChild(nativeSection);
                }
            };
        </script>
    </body>
    </html>
    """
    
    components.html(social_html, height=800)

def show_search_scraping():
    """Show search and scraping demos"""
    st.header("🔍 Search & Web Tools Demo")
    st.markdown("**Working search, URL manipulation, and data extraction tools:**")
    
    search_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: Arial, sans-serif; }
            .tool-section { 
                background: #f8f9fa; 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 8px; 
                border: 1px solid #dee2e6;
            }
            button { 
                padding: 10px 20px; 
                margin: 5px; 
                background: #ff4b4b; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
            }
            button:hover { background: #ff6b6b; }
            input[type="text"], input[type="url"] { 
                width: 70%; 
                padding: 10px; 
                margin: 5px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
            }
            .results { 
                background: white; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 10px 0; 
                border-left: 4px solid #007bff;
                max-height: 300px;
                overflow-y: auto;
            }
            .search-result { 
                padding: 10px; 
                margin: 10px 0; 
                background: #f8f9fa; 
                border-radius: 5px; 
                border-left: 3px solid #28a745;
            }
            .url-info { 
                background: #e9ecef; 
                padding: 10px; 
                margin: 5px 0; 
                border-radius: 5px; 
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>🔍 URL Analysis Tool</h3>
            
            <div class="tool-section">
                <h4>🔗 URL Parser & Analyzer</h4>
                <input type="url" id="urlInput" placeholder="Enter any URL to analyze..." value="https://www.example.com/path?param=value#section">
                <button onclick="analyzeURL()">Analyze URL</button>
                
                <div id="urlAnalysis" class="results">
                    URL analysis will appear here...
                </div>
            </div>
            
            <div class="tool-section">
                <h4>🌐 Domain & Page Info Extractor</h4>
                <input type="url" id="domainInput" placeholder="Enter URL to get domain info..." value="https://github.com/streamlit/streamlit">
                <button onclick="extractDomainInfo()">Extract Info</button>
                
                <div id="domainInfo" class="results">
                    Domain information will appear here...
                </div>
            </div>
            
            <div class="tool-section">
                <h4>🔍 Simple Search Engine</h4>
                <input type="text" id="searchQuery" placeholder="Enter search terms..." value="javascript tutorials">
                <button onclick="performSearch()">Search Popular Sites</button>
                
                <div id="searchResults" class="results">
                    Search links will appear here...
                </div>
            </div>
            
            <div class="tool-section">
                <h4>📊 Page Metadata Extractor</h4>
                <input type="url" id="metaUrl" placeholder="Enter URL to extract metadata..." value="">
                <button onclick="extractMetadata()">Extract Metadata</button>
                
                <div id="metadataResults" class="results">
                    Page metadata will appear here...
                </div>
            </div>
            
            <div class="tool-section">
                <h4>🔧 URL Builder</h4>
                <input type="text" id="baseUrl" placeholder="Base URL..." value="https://api.example.com">
                <input type="text" id="urlPath" placeholder="Path..." value="/users">
                <input type="text" id="urlParams" placeholder="Parameters (key=value&key2=value2)..." value="limit=10&sort=name">
                <button onclick="buildURL()">Build URL</button>
                
                <div id="builtUrl" class="results">
                    Built URL will appear here...
                </div>
            </div>
        </div>

        <script>
            function analyzeURL() {
                const url = document.getElementById('urlInput').value;
                const resultsDiv = document.getElementById('urlAnalysis');
                
                try {
                    const urlObj = new URL(url);
                    
                    const analysis = `
                        <div class="url-info"><strong>Protocol:</strong> ${urlObj.protocol}</div>
                        <div class="url-info"><strong>Host:</strong> ${urlObj.host}</div>
                        <div class="url-info"><strong>Hostname:</strong> ${urlObj.hostname}</div>
                        <div class="url-info"><strong>Port:</strong> ${urlObj.port || 'default'}</div>
                        <div class="url-info"><strong>Pathname:</strong> ${urlObj.pathname}</div>
                        <div class="url-info"><strong>Search:</strong> ${urlObj.search}</div>
                        <div class="url-info"><strong>Hash:</strong> ${urlObj.hash}</div>
                        <div class="url-info"><strong>Origin:</strong> ${urlObj.origin}</div>
                    `;
                    
                    resultsDiv.innerHTML = analysis;
                } catch (error) {
                    resultsDiv.innerHTML = `<div style="color: red;">Error: Invalid URL - ${error.message}</div>`;
                }
            }

            function extractDomainInfo() {
                const url = document.getElementById('domainInput').value;
                const resultsDiv = document.getElementById('domainInfo');
                
                try {
                    const urlObj = new URL(url);
                    const domain = urlObj.hostname;
                    
                    // Extract TLD and subdomain info
                    const parts = domain.split('.');
                    const tld = parts.slice(-1)[0];
                    const sld = parts.length > 1 ? parts.slice(-2, -1)[0] : '';
                    const subdomain = parts.length > 2 ? parts.slice(0, -2).join('.') : '';
                    
                    const domainInfo = `
                        <div class="url-info"><strong>Full Domain:</strong> ${domain}</div>
                        <div class="url-info"><strong>Subdomain:</strong> ${subdomain || 'none'}</div>
                        <div class="url-info"><strong>Second Level Domain:</strong> ${sld}</div>
                        <div class="url-info"><strong>Top Level Domain:</strong> ${tld}</div>
                        <div class="url-info"><strong>Is Secure:</strong> ${urlObj.protocol === 'https:' ? '✅ Yes' : '❌ No'}</div>
                        <div class="url-info"><strong>Port:</strong> ${urlObj.port || (urlObj.protocol === 'https:' ? '443' : '80')}</div>
                    `;
                    
                    resultsDiv.innerHTML = domainInfo;
                } catch (error) {
                    resultsDiv.innerHTML = `<div style="color: red;">Error: ${error.message}</div>`;
                }
            }

            function performSearch() {
                const query = document.getElementById('searchQuery').value;
                const resultsDiv = document.getElementById('searchResults');
                
                if (!query.trim()) {
                    resultsDiv.innerHTML = 'Please enter a search query.';
                    return;
                }
                
                // Create search links for popular sites
                const searchEngines = [
                    { name: 'Google', url: `https://www.google.com/search?q=${encodeURIComponent(query)}` },
                    { name: 'Bing', url: `https://www.bing.com/search?q=${encodeURIComponent(query)}` },
                    { name: 'DuckDuckGo', url: `https://duckduckgo.com/?q=${encodeURIComponent(query)}` },
                    { name: 'YouTube', url: `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}` },
                    { name: 'GitHub', url: `https://github.com/search?q=${encodeURIComponent(query)}` },
                    { name: 'Stack Overflow', url: `https://stackoverflow.com/search?q=${encodeURIComponent(query)}` },
                    { name: 'MDN', url: `https://developer.mozilla.org/en-US/search?q=${encodeURIComponent(query)}` },
                    { name: 'W3Schools', url: `https://www.w3schools.com/search/search_w3schools.asp?searchterm=${encodeURIComponent(query)}` }
                ];
                
                let searchHTML = `<h4>🔍 Search "${query}" on:</h4>`;
                searchEngines.forEach(engine => {
                    searchHTML += `
                        <div class="search-result">
                            <strong>${engine.name}:</strong>
                            <a href="${engine.url}" target="_blank" style="margin-left: 10px; color: #007bff;">
                                Search on ${engine.name} →
                            </a>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = searchHTML;
            }

            function extractMetadata() {
                const url = document.getElementById('metaUrl').value;
                const resultsDiv = document.getElementById('metadataResults');
                
                if (!url.trim()) {
                    resultsDiv.innerHTML = 'Please enter a URL to analyze.';
                    return;
                }
                
                resultsDiv.innerHTML = 'Extracting metadata from current page...';
                
                // Extract metadata from current page (since we can't fetch external pages due to CORS)
                const metadata = {
                    title: document.title || 'No title found',
                    description: getMetaContent('description') || 'No description found',
                    keywords: getMetaContent('keywords') || 'No keywords found',
                    author: getMetaContent('author') || 'No author found',
                    robots: getMetaContent('robots') || 'Not specified',
                    viewport: getMetaContent('viewport') || 'Not specified',
                    charset: document.charset || 'Not specified',
                    url: window.location.href,
                    domain: window.location.hostname,
                    links: document.links.length,
                    images: document.images.length,
                    forms: document.forms.length
                };
                
                let metaHTML = `
                    <h4>📊 Current Page Metadata:</h4>
                    <div class="url-info"><strong>Title:</strong> ${metadata.title}</div>
                    <div class="url-info"><strong>Description:</strong> ${metadata.description}</div>
                    <div class="url-info"><strong>Keywords:</strong> ${metadata.keywords}</div>
                    <div class="url-info"><strong>Author:</strong> ${metadata.author}</div>
                    <div class="url-info"><strong>Robots:</strong> ${metadata.robots}</div>
                    <div class="url-info"><strong>Viewport:</strong> ${metadata.viewport}</div>
                    <div class="url-info"><strong>Charset:</strong> ${metadata.charset}</div>
                    <div class="url-info"><strong>Total Links:</strong> ${metadata.links}</div>
                    <div class="url-info"><strong>Total Images:</strong> ${metadata.images}</div>
                    <div class="url-info"><strong>Total Forms:</strong> ${metadata.forms}</div>
                `;
                
                resultsDiv.innerHTML = metaHTML;
            }

            function getMetaContent(name) {
                const meta = document.querySelector(`meta[name="${name}"]`) || 
                             document.querySelector(`meta[property="og:${name}"]`) ||
                             document.querySelector(`meta[property="${name}"]`);
                return meta ? meta.content : null;
            }

            function buildURL() {
                const base = document.getElementById('baseUrl').value;
                const path = document.getElementById('urlPath').value;
                const params = document.getElementById('urlParams').value;
                const resultsDiv = document.getElementById('builtUrl');
                
                try {
                    let fullUrl = base;
                    
                    // Add path
                    if (path) {
                        fullUrl += path.startsWith('/') ? path : '/' + path;
                    }
                    
                    // Add parameters
                    if (params) {
                        const separator = fullUrl.includes('?') ? '&' : '?';
                        fullUrl += separator + params;
                    }
                    
                    // Validate the built URL
                    const urlObj = new URL(fullUrl);
                    
                    resultsDiv.innerHTML = `
                        <div class="url-info"><strong>Built URL:</strong></div>
                        <div class="url-info" style="word-break: break-all; background: #e7f3ff;">
                            <a href="${fullUrl}" target="_blank">${fullUrl}</a>
                        </div>
                        <button onclick="navigator.clipboard.writeText('${fullUrl}')" style="margin-top: 10px;">
                            Copy to Clipboard
                        </button>
                    `;
                } catch (error) {
                    resultsDiv.innerHTML = `<div style="color: red;">Error building URL: ${error.message}</div>`;
                }
            }

            // Initialize with current page URL analysis
            window.onload = function() {
                document.getElementById('urlInput').value = window.location.href;
                document.getElementById('metaUrl').value = window.location.href;
            };
        </script>
    </body>
    </html>
    """
    
    components.html(search_html, height=1000)

def show_interactive_elements():
    """Show interactive elements and drag/drop functionality"""
    st.header("🖱️ Interactive Elements Demo")
    st.markdown("**Working drag & drop, interactive forms, and dynamic elements:**")
    
    interactive_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: Arial, sans-serif; }
            .demo-section { 
                background: #f8f9fa; 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 8px; 
                border: 1px solid #dee2e6;
            }
            
            /* Drag and Drop Styles */
            .drag-container { display: flex; gap: 20px; margin: 20px 0; }
            .drag-source, .drop-zone { 
                min-height: 200px; 
                border: 2px dashed #ccc; 
                border-radius: 8px; 
                padding: 20px; 
                flex: 1;
            }
            .drag-source { background: #e7f3ff; }
            .drop-zone { background: #f0f8e7; }
            .drop-zone.drag-over { 
                background: #fff3cd; 
                border-color: #ffc107; 
            }
            
            .draggable { 
                background: #007bff; 
                color: white; 
                padding: 10px; 
                margin: 5px; 
                border-radius: 5px; 
                cursor: move; 
                user-select: none;
                display: inline-block;
            }
            .draggable:hover { background: #0056b3; }
            .draggable.dragging { opacity: 0.5; }
            
            /* Interactive Form Styles */
            .form-builder { background: white; padding: 20px; border-radius: 8px; }
            .form-element { 
                padding: 10px; 
                margin: 10px 0; 
                border: 1px solid #ddd; 
                border-radius: 5px; 
                background: white;
            }
            
            /* Color Picker and Sliders */
            .color-demo { 
                width: 100px; 
                height: 100px; 
                border-radius: 50%; 
                margin: 20px auto; 
                border: 3px solid #ccc;
                transition: all 0.3s ease;
            }
            
            /* Animation Demo */
            .animated-box { 
                width: 100px; 
                height: 100px; 
                background: linear-gradient(45deg, #ff4b4b, #ff6b6b); 
                margin: 20px auto; 
                border-radius: 10px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .animated-box:hover { 
                transform: rotate(45deg) scale(1.2); 
                box-shadow: 0 10px 20px rgba(255, 75, 75, 0.3);
            }
            
            button { 
                padding: 10px 20px; 
                margin: 5px; 
                background: #ff4b4b; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
            }
            button:hover { background: #ff6b6b; }
            
            input[type="range"] { width: 200px; margin: 10px; }
            input[type="color"] { width: 60px; height: 40px; margin: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>🖱️ Drag & Drop Demo</h3>
            
            <div class="demo-section">
                <h4>📦 Drag Items Between Containers</h4>
                <div class="drag-container">
                    <div class="drag-source" id="source">
                        <h5>📋 Available Items (Drag from here)</h5>
                        <div class="draggable" draggable="true">🎵 Music Player</div>
                        <div class="draggable" draggable="true">📱 Mobile App</div>
                        <div class="draggable" draggable="true">🎮 Game Console</div>
                        <div class="draggable" draggable="true">💻 Laptop</div>
                        <div class="draggable" draggable="true">📺 Smart TV</div>
                    </div>
                    
                    <div class="drop-zone" id="target">
                        <h5>🗂️ My Collection (Drop here)</h5>
                        <p id="dropMessage">Drop items here to add to your collection!</p>
                    </div>
                </div>
                
                <button onclick="resetDragDemo()">🔄 Reset Demo</button>
            </div>
            
            <div class="demo-section">
                <h4>🎨 Interactive Color & Animation Demo</h4>
                <div style="text-align: center;">
                    <div class="color-demo" id="colorDemo"></div>
                    
                    <div>
                        <label>🎨 Color: </label>
                        <input type="color" id="colorPicker" value="#ff4b4b" onchange="updateColor()">
                    </div>
                    
                    <div>
                        <label>📏 Size: </label>
                        <input type="range" id="sizeSlider" min="50" max="200" value="100" oninput="updateSize()">
                        <span id="sizeValue">100px</span>
                    </div>
                    
                    <div>
                        <label>🔄 Rotation: </label>
                        <input type="range" id="rotationSlider" min="0" max="360" value="0" oninput="updateRotation()">
                        <span id="rotationValue">0°</span>
                    </div>
                    
                    <div class="animated-box" id="animatedBox" onclick="animateBox()">
                        Click me!
                    </div>
                </div>
            </div>
            
            <div class="demo-section">
                <h4>📝 Dynamic Form Builder</h4>
                <div>
                    <button onclick="addInput('text')">+ Text Input</button>
                    <button onclick="addInput('email')">+ Email Input</button>
                    <button onclick="addInput('number')">+ Number Input</button>
                    <button onclick="addInput('textarea')">+ Text Area</button>
                    <button onclick="addInput('select')">+ Dropdown</button>
                    <button onclick="clearForm()">🗑️ Clear Form</button>
                </div>
                
                <div class="form-builder">
                    <form id="dynamicForm">
                        <h5>📋 Your Dynamic Form</h5>
                        <p id="formEmpty">No form elements yet. Add some using the buttons above!</p>
                    </form>
                    
                    <button onclick="previewForm()" style="background: #28a745;">👁️ Preview Form Data</button>
                </div>
                
                <div id="formPreview" style="background: #e9ecef; padding: 15px; margin: 15px 0; border-radius: 5px; display: none;">
                    <h5>📊 Form Data Preview</h5>
                    <pre id="formData"></pre>
                </div>
            </div>
        </div>

        <script>
            let draggedElement = null;
            let elementCounter = 0;

            // Drag and Drop functionality
            function setupDragAndDrop() {
                const draggables = document.querySelectorAll('.draggable');
                const dropZone = document.getElementById('target');

                draggables.forEach(draggable => {
                    draggable.addEventListener('dragstart', handleDragStart);
                    draggable.addEventListener('dragend', handleDragEnd);
                });

                dropZone.addEventListener('dragover', handleDragOver);
                dropZone.addEventListener('drop', handleDrop);
                dropZone.addEventListener('dragenter', handleDragEnter);
                dropZone.addEventListener('dragleave', handleDragLeave);
            }

            function handleDragStart(e) {
                draggedElement = this;
                this.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/html', this.outerHTML);
            }

            function handleDragEnd(e) {
                this.classList.remove('dragging');
            }

            function handleDragOver(e) {
                if (e.preventDefault) e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                return false;
            }

            function handleDragEnter(e) {
                this.classList.add('drag-over');
            }

            function handleDragLeave(e) {
                this.classList.remove('drag-over');
            }

            function handleDrop(e) {
                if (e.stopPropagation) e.stopPropagation();
                
                this.classList.remove('drag-over');
                
                if (draggedElement !== this) {
                    const dropMessage = document.getElementById('dropMessage');
                    if (dropMessage && dropMessage.textContent.includes('Drop items here')) {
                        dropMessage.remove();
                    }
                    
                    // Clone the element instead of moving it
                    const newElement = draggedElement.cloneNode(true);
                    newElement.style.background = '#28a745';
                    newElement.innerHTML += ' ✅';
                    this.appendChild(newElement);
                    
                    // Add remove functionality
                    newElement.addEventListener('click', function() {
                        this.remove();
                        checkIfEmpty();
                    });
                }
                
                return false;
            }

            function checkIfEmpty() {
                const dropZone = document.getElementById('target');
                if (dropZone.children.length === 1) {
                    const message = document.createElement('p');
                    message.id = 'dropMessage';
                    message.textContent = 'Drop items here to add to your collection!';
                    dropZone.appendChild(message);
                }
            }

            function resetDragDemo() {
                const dropZone = document.getElementById('target');
                dropZone.innerHTML = '<h5>🗂️ My Collection (Drop here)</h5><p id="dropMessage">Drop items here to add to your collection!</p>';
            }

            // Color and Animation Demo
            function updateColor() {
                const color = document.getElementById('colorPicker').value;
                const demo = document.getElementById('colorDemo');
                demo.style.background = `linear-gradient(45deg, ${color}, ${color}aa)`;
            }

            function updateSize() {
                const size = document.getElementById('sizeSlider').value;
                const demo = document.getElementById('colorDemo');
                demo.style.width = size + 'px';
                demo.style.height = size + 'px';
                document.getElementById('sizeValue').textContent = size + 'px';
            }

            function updateRotation() {
                const rotation = document.getElementById('rotationSlider').value;
                const demo = document.getElementById('colorDemo');
                demo.style.transform = `rotate(${rotation}deg)`;
                document.getElementById('rotationValue').textContent = rotation + '°';
            }

            function animateBox() {
                const box = document.getElementById('animatedBox');
                const randomColor = '#' + Math.floor(Math.random()*16777215).toString(16);
                const randomRotation = Math.random() * 360;
                const randomScale = 0.8 + Math.random() * 0.4;
                
                box.style.background = `linear-gradient(45deg, ${randomColor}, ${randomColor}aa)`;
                box.style.transform = `rotate(${randomRotation}deg) scale(${randomScale})`;
                
                setTimeout(() => {
                    box.style.transform = 'rotate(0deg) scale(1)';
                }, 300);
            }

            // Dynamic Form Builder
            function addInput(type) {
                elementCounter++;
                const form = document.getElementById('dynamicForm');
                const emptyMessage = document.getElementById('formEmpty');
                
                if (emptyMessage) {
                    emptyMessage.remove();
                }
                
                const wrapper = document.createElement('div');
                wrapper.className = 'form-element';
                wrapper.innerHTML = getFormElementHTML(type, elementCounter);
                
                form.appendChild(wrapper);
                
                // Add remove button functionality
                const removeBtn = wrapper.querySelector('.remove-btn');
                if (removeBtn) {
                    removeBtn.addEventListener('click', function() {
                        wrapper.remove();
                        checkFormEmpty();
                    });
                }
            }

            function getFormElementHTML(type, id) {
                const removeBtn = '<button type="button" class="remove-btn" style="background: #dc3545; float: right;">×</button>';
                
                switch(type) {
                    case 'text':
                        return `
                            ${removeBtn}
                            <label for="text_${id}">Text Input:</label><br>
                            <input type="text" id="text_${id}" name="text_${id}" placeholder="Enter text..." style="width: 90%; padding: 8px; margin: 5px 0;">
                        `;
                    case 'email':
                        return `
                            ${removeBtn}
                            <label for="email_${id}">Email Input:</label><br>
                            <input type="email" id="email_${id}" name="email_${id}" placeholder="Enter email..." style="width: 90%; padding: 8px; margin: 5px 0;">
                        `;
                    case 'number':
                        return `
                            ${removeBtn}
                            <label for="number_${id}">Number Input:</label><br>
                            <input type="number" id="number_${id}" name="number_${id}" placeholder="Enter number..." style="width: 90%; padding: 8px; margin: 5px 0;">
                        `;
                    case 'textarea':
                        return `
                            ${removeBtn}
                            <label for="textarea_${id}">Text Area:</label><br>
                            <textarea id="textarea_${id}" name="textarea_${id}" placeholder="Enter long text..." style="width: 90%; padding: 8px; margin: 5px 0; height: 80px; resize: vertical;"></textarea>
                        `;
                    case 'select':
                        return `
                            ${removeBtn}
                            <label for="select_${id}">Dropdown:</label><br>
                            <select id="select_${id}" name="select_${id}" style="width: 90%; padding: 8px; margin: 5px 0;">
                                <option value="">Choose an option...</option>
                                <option value="option1">Option 1</option>
                                <option value="option2">Option 2</option>
                                <option value="option3">Option 3</option>
                            </select>
                        `;
                    default:
                        return '<p>Unknown element type</p>';
                }
            }

            function clearForm() {
                const form = document.getElementById('dynamicForm');
                form.innerHTML = '<h5>📋 Your Dynamic Form</h5><p id="formEmpty">No form elements yet. Add some using the buttons above!</p>';
                document.getElementById('formPreview').style.display = 'none';
            }

            function checkFormEmpty() {
                const form = document.getElementById('dynamicForm');
                if (form.children.length === 1) { // Only the title remains
                    const emptyMessage = document.createElement('p');
                    emptyMessage.id = 'formEmpty';
                    emptyMessage.textContent = 'No form elements yet. Add some using the buttons above!';
                    form.appendChild(emptyMessage);
                }
            }

            function previewForm() {
                const form = document.getElementById('dynamicForm');
                const inputs = form.querySelectorAll('input, textarea, select');
                const formData = {};
                
                inputs.forEach(input => {
                    if (input.name) {
                        formData[input.name] = input.value;
                    }
                });
                
                const preview = document.getElementById('formPreview');
                const dataDisplay = document.getElementById('formData');
                
                dataDisplay.textContent = JSON.stringify(formData, null, 2);
                preview.style.display = 'block';
            }

            // Initialize everything when page loads
            window.onload = function() {
                setupDragAndDrop();
                updateColor();
                
                // Add event listeners for new draggable elements
                document.addEventListener('DOMNodeInserted', function(e) {
                    if (e.target.classList && e.target.classList.contains('draggable')) {
                        e.target.addEventListener('dragstart', handleDragStart);
                        e.target.addEventListener('dragend', handleDragEnd);
                    }
                });
            };
        </script>
    </body>
    </html>
    """
    
    components.html(interactive_html, height=1200)

if __name__ == "__main__":
    run()
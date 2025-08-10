import streamlit as st
import cv2
import numpy as np
import subprocess
import time
from collections import deque

# --- Dependency Imports with Error Handling ---

# Attempt to import the custom finger_guide module for the visual guide
try:
    from finger_guide import get_finger_guide_html
    finger_guide_available = True
except ImportError:
    finger_guide_available = False

# Attempt to import mediapipe and handle potential errors
try:
    import mediapipe as mp
    mediapipe_available = True
    mediapipe_error = None
except Exception as e:
    mediapipe_available = False
    mediapipe_error = str(e)


# --- Helper Function to Check Docker Availability ---

def check_docker():
    """Checks if the Docker daemon is installed and running."""
    try:
        # Use 'docker info' as it's a reliable way to check daemon connectivity
        result = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "Docker is available"
        else:
            return False, "Docker daemon is not running. Please start Docker Desktop or the Docker service."
    except FileNotFoundError:
        return False, "Docker is not installed. Please install Docker to use this application."
    except subprocess.TimeoutExpired:
        return False, "Docker command timed out. It might be starting up or unresponsive."
    except Exception as e:
        return False, f"An unexpected error occurred while checking Docker: {str(e)}"


# --- Main Controller Class ---

class FingerDockerController:
    """Manages Docker commands and hand gesture processing."""
    def __init__(self):
        # Container settings
        self.container_name = "finger_controlled_container"
        self.container_image = "nginx:latest"
        
        # History for stabilizing finger count detection
        self.finger_history = deque(maxlen=10)
        
        # Initialize MediaPipe Hands solution if available
        if mediapipe_available:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.mp_drawing = mp.solutions.drawing_utils
        else:
            self.mp_hands = None
            self.hands = None
            self.mp_drawing = None
            
    def count_fingers(self, landmarks):
        """Counts the number of extended fingers from hand landmarks."""
        if not landmarks or not mediapipe_available:
            return 0
            
        tip_ids = [4, 8, 12, 16, 20]  # Landmarks for the tip of each finger
        pip_ids = [3, 6, 10, 14, 18]  # Landmarks for the PIP joint of each finger
        
        fingers = []
        
        # Logic for the thumb (based on x-coordinate)
        if landmarks[tip_ids[0]].x > landmarks[pip_ids[0]].x:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # Logic for the other four fingers (based on y-coordinate)
        for i in range(1, 5):
            if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return sum(fingers)
    
    def execute_docker_command(self, command):
        """Executes a given Docker command and returns success status and a message."""
        try:
            if command == "pull":
                st.toast(f"Pulling image {self.container_image}...", icon="🔄")
                result = subprocess.run(["docker", "pull", self.container_image], capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    return True, f"✅ Image {self.container_image} pulled"
                return False, f"❌ Failed to pull image: {result.stderr.strip()}"

            elif command == "run":
                # Check if container already exists
                check_result = subprocess.run(["docker", "ps", "-a", "--filter", f"name={self.container_name}"], capture_output=True, text=True)
                if self.container_name in check_result.stdout:
                    return False, "❌ Container already exists. Use Start or Remove."
                
                st.toast(f"Launching container {self.container_name}...", icon="🚀")
                result = subprocess.run(["docker", "run", "-d", "--name", self.container_name, "-p", "8080:80", self.container_image], capture_output=True, text=True)
                if result.returncode == 0:
                    return True, f"✅ Container {self.container_name} launched on port 8080"
                return False, f"❌ Failed to launch container: {result.stderr.strip()}"

            elif command == "stop":
                st.toast(f"Stopping container {self.container_name}...", icon="⏹️")
                result = subprocess.run(["docker", "stop", self.container_name], capture_output=True, text=True)
                if result.returncode == 0:
                    return True, f"✅ Container {self.container_name} stopped"
                return False, f"❌ Container not found or already stopped: {result.stderr.strip()}"

            elif command == "start":
                st.toast(f"Starting container {self.container_name}...", icon="▶️")
                result = subprocess.run(["docker", "start", self.container_name], capture_output=True, text=True)
                if result.returncode == 0:
                    return True, f"✅ Container {self.container_name} started"
                return False, f"❌ Container not found or failed to start: {result.stderr.strip()}"

            elif command == "remove":
                st.toast(f"Removing container {self.container_name}...", icon="🗑️")
                # Ensure it's stopped before removing
                subprocess.run(["docker", "stop", self.container_name], capture_output=True, text=True)
                result = subprocess.run(["docker", "rm", self.container_name], capture_output=True, text=True)
                if result.returncode == 0:
                    return True, f"✅ Container {self.container_name} removed"
                return False, f"❌ Container not found or failed to remove: {result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            return False, "❌ Command timed out. Docker may be busy."
        except Exception as e:
            return False, f"❌ Error executing command: {str(e)}"

    def get_container_info(self):
        """Retrieves the current status and details of the managed container."""
        try:
            result = subprocess.run(["docker", "ps", "-a", "--filter", f"name={self.container_name}", "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"], capture_output=True, text=True)
            if result.stdout.strip():
                parts = result.stdout.strip().split('\t')
                status = parts[1] if len(parts) > 1 else "Unknown"
                ports = parts[2] if len(parts) > 2 else "N/A"
                return {'exists': True, 'status': status, 'ports': ports, 'running': "Up" in status}
            else:
                return {'exists': False, 'status': 'Not found', 'ports': 'N/A', 'running': False}
        except Exception as e:
            return {'exists': False, 'status': f'Error: {str(e)}', 'ports': 'N/A', 'running': False}
    
    def process_frame(self, frame):
        """Processes a video frame to detect hands and count fingers."""
        if frame is None:
            return np.zeros((480, 640, 3), dtype=np.uint8), 0

        if not mediapipe_available or self.hands is None:
            cv2.putText(frame, "MediaPipe not available", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return frame, 0

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        finger_count = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                finger_count = self.count_fingers(hand_landmarks.landmark)
        
        self.finger_history.append(finger_count)
        
        # Use the most common finger count from the recent history for stability
        if len(self.finger_history) > 0:
            stable_count = max(set(self.finger_history), key=self.finger_history.count)
        else:
            stable_count = 0
            
        return frame, stable_count


# --- Main Application Function ---

def run():
    """The main function that sets up and runs the Streamlit application page."""
    
    # 1. Check for critical dependencies first
    docker_available, docker_message = check_docker()
    if not docker_available:
        st.error(f"🚨 {docker_message}")
        st.info("Please ensure Docker Desktop is installed and running, then refresh this page.")
        if st.button("🔄 Check Again"):
            st.rerun()
        st.stop()

    if not mediapipe_available:
        st.error("⚠️ MediaPipe library is not available or has compatibility issues.")
        st.warning(f"Error details: {mediapipe_error}")
        st.info("Please install or fix the required dependencies.")
        st.code("pip install mediapipe opencv-python", language="bash")
        st.stop()

    # 2. Initialize Session State
    if 'controller' not in st.session_state:
        st.session_state.controller = FingerDockerController()
    if 'camera_active' not in st.session_state:
        st.session_state.camera_active = False
    if 'last_command_time' not in st.session_state:
        st.session_state.last_command_time = 0
    if 'last_finger_count' not in st.session_state:
        st.session_state.last_finger_count = 0
    if 'command_results' not in st.session_state:
        st.session_state.command_results = []
    
    # 3. Page Title and UI Setup
    st.title("🐋 Finger Docker Controller")
    
    # Display finger command guide
    if finger_guide_available:
        st.markdown(get_finger_guide_html(), unsafe_allow_html=True)
    else:
        st.info("Visual finger guide not found. Displaying text guide.")
        st.markdown("#### Finger Commands:\n- **1 Finger:** Pull Image\n- **2 Fingers:** Launch Container\n- **3 Fingers:** Stop Container\n- **4 Fingers:** Start Container\n- **5 Fingers:** Remove Container")

    # 4. Sidebar for Settings and Manual Controls
    with st.sidebar:
        st.header("📋 Controls")
        
        st.subheader("🐳 Docker Settings")
        st.session_state.controller.container_name = st.text_input("Container Name", st.session_state.controller.container_name)
        st.session_state.controller.container_image = st.text_input("Docker Image", st.session_state.controller.container_image)
        
        st.divider()
        st.subheader("🎮 Manual Controls")
        if st.button("🔄 Pull Image"):
            success, msg = st.session_state.controller.execute_docker_command("pull")
            st.session_state.command_results.append((time.time(), success, msg))
        if st.button("🚀 Launch"):
            success, msg = st.session_state.controller.execute_docker_command("run")
            st.session_state.command_results.append((time.time(), success, msg))
        if st.button("⏹️ Stop"):
            success, msg = st.session_state.controller.execute_docker_command("stop")
            st.session_state.command_results.append((time.time(), success, msg))
        if st.button("▶️ Start"):
            success, msg = st.session_state.controller.execute_docker_command("start")
            st.session_state.command_results.append((time.time(), success, msg))
        if st.button("🗑️ Remove"):
            success, msg = st.session_state.controller.execute_docker_command("remove")
            st.session_state.command_results.append((time.time(), success, msg))
        
    # 5. Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Camera Feed")
        if st.toggle("Activate Camera", key="camera_active"):
            frame_placeholder = st.empty()
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Could not open camera. Please check camera permissions and connection.")
                st.session_state.camera_active = False
            
            while st.session_state.camera_active:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to capture frame from camera.")
                    break
                
                processed_frame, finger_count = st.session_state.controller.process_frame(frame)
                frame_placeholder.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), caption="Live Feed", use_column_width=True)
                
                # Command execution logic based on finger count
                current_time = time.time()
                if finger_count > 0 and finger_count != st.session_state.last_finger_count and (current_time - st.session_state.last_command_time > 3.0):
                    st.session_state.last_finger_count = finger_count
                    st.session_state.last_command_time = current_time
                    command_map = {1: "pull", 2: "run", 3: "stop", 4: "start", 5: "remove"}
                    if finger_count in command_map:
                        success, message = st.session_state.controller.execute_docker_command(command_map[finger_count])
                        st.session_state.command_results.append((current_time, success, message))
            
            cap.release()
        else:
            st.info("Camera is off. Toggle the switch above to start.")

    with col2:
        st.subheader("📊 Container Status")
        if st.button("🔄 Refresh"):
            st.rerun()
            
        info = st.session_state.controller.get_container_info()
        if info['running']:
            st.success(f"🟢 Running: {info['status']}")
        elif info['exists']:
            st.warning(f"🟡 Stopped: {info['status']}")
        else:
            st.error(f"🔴 {info['status']}")
            
        st.write(f"**Ports:** {info['ports']}")
        if info['running'] and '8080' in info['ports']:
            st.link_button("🌐 Open Web UI", "http://localhost:8080")
            
        st.divider()
        st.subheader("📜 Command History")
        if st.button("🧹 Clear History"):
            st.session_state.command_results = []
            st.rerun()
            
        for t, success, msg in reversed(st.session_state.command_results[-5:]):
            st.toast(msg, icon="✅" if success else "❌")
            if success:
                st.success(f"[{time.strftime('%H:%M:%S', time.localtime(t))}] {msg}")
            else:
                st.error(f"[{time.strftime('%H:%M:%S', time.localtime(t))}] {msg}")


# This allows the script to be run directly for testing purposes
if __name__ == "__main__":
    run()
def run():
    import streamlit as st
    import subprocess
    import os

    # Custom CSS for beautiful styling
    st.markdown("""
    <style>
        /* Main app styling */
        .main > div {
            padding-top: 2rem;
        }
        
        /* Custom title styling */
        .title-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .title-text {
            color: white;
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle-text {
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin-top: 0.5rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 15px;
            border: 2px solid #e1e5e9;
            padding: 0.75rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Success message styling */
        .stSuccess {
            background: linear-gradient(45deg, #d4edda, #c3e6cb);
            border: none;
            border-radius: 15px;
            padding: 1rem;
        }
        
        /* Error message styling */
        .stError {
            background: linear-gradient(45deg, #f8d7da, #f1aeb5);
            border: none;
            border-radius: 15px;
            padding: 1rem;
        }
        
        /* Info message styling */
        .stInfo {
            background: linear-gradient(45deg, #cce7ff, #b3d9ff);
            border: none;
            border-radius: 15px;
            padding: 1rem;
        }
        
        /* Code/text output styling */
        .stText {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            border-left: 4px solid #667eea;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        
        /* Section headers */
        .section-header {
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        /* Card-like containers */
        .card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            margin-top: 3rem;
            color: #6c757d;
            font-weight: 500;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            border-radius: 15px;
            border: 2px solid #e1e5e9;
        }
        
        /* Container status indicators */
        .status-running {
            color: #28a745;
            font-weight: bold;
        }
        
        .status-stopped {
            color: #dc3545;
            font-weight: bold;
        }
        
        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 2s infinite;
        }
    </style>
    """, unsafe_allow_html=True)

    # Custom title with beautiful styling
    st.markdown("""
    <div class="title-container">
        <h1 class="title-text">🐳 Docker Manager</h1>
        <p class="subtitle-text">Manage your Docker containers, images, networks & volumes with style</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for context management
    if 'context' not in st.session_state:
        st.session_state.context = 'default'  # 'default' for local docker daemon

    def run_command(cmd):
        """Enhanced command runner with better error handling and OS detection"""
        try:
            # The docker CLI automatically uses the current context. No special handling needed here.
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, check=False)
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out after 60 seconds", 1
        except Exception as e:
            return "", f"Error running command: {str(e)}", 1

    # http://local.dock.user""/8501
    def get_docker_info():
        """Get Docker system information based on the current context"""
        try:
            version_output, _, _ = run_command("docker --version")
            # The 'docker info' command can be slow on remote connections, so we add a friendly message
            with st.spinner(f"Fetching info from `{st.session_state.context}` context..."):
                info_output, _, _ = run_command("docker info --format '{{.ServerVersion}}'")
            return version_output.strip(), info_output.strip()
        except Exception as e:
            return "Docker not found", f"Error: {e}"

    # --- Sidebar ---

    # Docker info section
    docker_version, server_version = get_docker_info()
    st.sidebar.markdown("### 🐳 Docker Info")
    st.sidebar.info(f"**Client:** {docker_version}")
    if server_version:
        st.sidebar.info(f"**Server:** {server_version}")

    st.sidebar.markdown("---")

    # SSH Remote Connection Section
    st.sidebar.header("🔗 Remote Connection (SSH)")
    st.sidebar.info(f"**Current Context:** `{st.session_state.context}`")

    ssh_target = st.sidebar.text_input("SSH Target (e.g. root@192.168.1.100)", key="ssh_target_input")

    c1, c2 = st.sidebar.columns(2)
    with c1:
        if st.button("Connect"):
            if ssh_target:
                context_name = "remote-ssh"
                create_cmd = f'docker context create {context_name} --docker "host=ssh://{ssh_target}"'
                
                with st.spinner(f"Creating context for {ssh_target}..."):
                    _, err, ret = run_command(create_cmd)
                
                if ret == 0:
                    use_cmd = f'docker context use {context_name}'
                    with st.spinner(f"Switching context to {context_name}..."):
                        _, err_use, ret_use = run_command(use_cmd)
                    
                    if ret_use == 0:
                        st.session_state.context = context_name
                        st.sidebar.success(f"Connected to {ssh_target}")
                        st.rerun()
                    else:
                        st.sidebar.error(f"Failed to use context: {err_use}")
                else:
                    st.sidebar.error(f"Failed to create context: {err}")
            else:
                st.sidebar.warning("Please enter an SSH target.")

    with c2:
        if st.button("Disconnect"):
            with st.spinner("Switching back to local context..."):
                _, err, ret = run_command('docker context use default')
            if ret == 0:
                st.session_state.context = 'default'
                st.sidebar.success("Using local Docker.")
                st.rerun()
            else:
                st.sidebar.error(f"Failed to disconnect: {err}")


    st.sidebar.markdown("---")
    st.sidebar.header("🎯 Choose What To Do")

    option = st.sidebar.selectbox("Pick One:", [
        "List Containers", 
        "▶️ Start Container", 
        "Run Container",
        "⏹️ Stop Container", 
        "🗑️ Remove Container",
        "🖼️ List Images",
        "📥 Pull Image",
        "🗑️ Remove Image",
        "🕸️ List Networks",
        "➕ Create Network",
        "➖ Remove Network",
        "💾 List Volumes",
        "➕ Create Volume", 
        "➖ Remove Volume",
        "🧹 System Cleanup"
    ])

    # --- Main content area ---
    if option == "List Containers":
        st.markdown('<h2 class="section-header">All Containers</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            auto_refresh = st.checkbox("Auto-refresh")
        
        if st.button("Show Containers") or auto_refresh:
            with st.spinner("Loading containers..."):
                output, error, return_code = run_command("docker ps -a --format 'table {{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}'")
                
                if return_code == 0 and output:
                    st.success("Containers loaded successfully!")
                    st.code(output, language='text')
                elif error:
                    st.error(f" Error: {error}")
                else:
                    st.warning("⚠️ No containers found or Docker not running")

    elif option == "▶️ Start Container":
        st.markdown('<h2 class="section-header">Start a Container</h2>', unsafe_allow_html=True)
        
        # Show available stopped containers
        with st.expander("View Stopped Containers"):
            stopped_output, _, _ = run_command("docker ps -a --filter 'status=exited' --format 'table {{.Names}}\\t{{.Image}}\\t{{.Status}}'")
            if stopped_output:
                st.code(stopped_output, language='text')
            else:
                st.info("No stopped containers found")
        
        container_name = st.text_input("Enter container name or ID:", placeholder="e.g., my-container or 1a2b3c4d")
        
        if st.button("Start Container"):
            if container_name:
                with st.spinner(f"Starting {container_name}..."):
                    output, error, return_code = run_command(f"docker start {container_name}")
                    
                    if return_code == 0:
                        st.success(f"Successfully started container: {container_name}")
                        if output:
                            st.code(output, language='text')
                    else:
                        st.error(f"Failed to start container: {error}")
            else:
                st.warning("⚠️ Please enter a container name or ID")

    elif option == "Run Container":
        st.markdown('<h2 class="section-header">Run a New Container</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            image_name = st.text_input("Image name:", placeholder="e.g., nginx, ubuntu:20.04")
            container_name_new = st.text_input("Container name (optional):", placeholder="e.g., my-web-server")
        
        with col2:
            port_mapping = st.text_input("Port mapping (optional):", placeholder="e.g., 8080:80")
            detached = st.checkbox("Run in background (detached)", value=True)
        
        advanced_options = st.expander("⚙️ Advanced Options")
        with advanced_options:
            environment_vars = st.text_area("Environment variables:", placeholder="ENV1=value1\nENV2=value2")
            volume_mapping = st.text_input("Volume mapping:", placeholder="e.g., /host/path:/container/path")
        
        if st.button("Run Container"):
            if image_name:
                cmd = "docker run"
                
                if detached:
                    cmd += " -d"
                if container_name_new:
                    cmd += f" --name {container_name_new}"
                if port_mapping:
                    cmd += f" -p {port_mapping}"
                if volume_mapping:
                    cmd += f" -v {volume_mapping}"
                
                if environment_vars:
                    for env_var in environment_vars.strip().split('\n'):
                        if '=' in env_var:
                            cmd += f" -e {env_var.strip()}"
                
                cmd += f" {image_name}"
                
                with st.spinner(f"Running container from {image_name}..."):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success(f"Successfully started container from {image_name}")
                        if output:
                            st.code(output, language='text')
                    else:
                        st.error(f"Failed to run container: {error}")
            else:
                st.warning("⚠️ Please enter an image name")

    elif option == "⏹️ Stop Container":
        st.markdown('<h2 class="section-header">Stop a Container</h2>', unsafe_allow_html=True)
        
        with st.expander("View Running Containers"):
            running_output, _, _ = run_command("docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Status}}'")
            if running_output:
                st.code(running_output, language='text')
            else:
                st.info("No running containers found")
        
        container_name = st.text_input("Enter container name or ID:", placeholder="e.g., my-container")
        
        if st.button("Stop Container"):
            if container_name:
                with st.spinner(f"Stopping {container_name}..."):
                    output, error, return_code = run_command(f"docker stop {container_name}")
                    
                    if return_code == 0:
                        st.success(f"Successfully stopped container: {container_name}")
                    else:
                        st.error(f"Failed to stop container: {error}")
            else:
                st.warning("⚠️ Please enter a container name or ID")

    elif option == "🗑️ Remove Container":
        st.markdown('<h2 class="section-header">Remove a Container</h2>', unsafe_allow_html=True)
        
        container_name = st.text_input("Enter container name or ID:", placeholder="e.g., my-container")
        force_remove = st.checkbox("Force remove (for running containers)")
        
        if st.button("Remove Container"):
            if container_name:
                cmd = f"docker rm {container_name}"
                if force_remove:
                    cmd += " -f"
                
                with st.spinner(f"Removing {container_name}..."):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success(f"Successfully removed container: {container_name}")
                    else:
                        st.error(f"❌ Failed to remove container: {error}")
            else:
                st.warning("⚠️ Please enter a container name or ID")

    elif option == "🖼️ List Images":
        st.markdown('<h2 class="section-header">All Images</h2>', unsafe_allow_html=True)
        
        if st.button("Show Images"):
            with st.spinner("Loading images..."):
                output, error, return_code = run_command("docker images --format 'table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}\\t{{.CreatedAt}}'")
                
                if return_code == 0 and output:
                    st.success("Images loaded successfully!")
                    st.code(output, language='text')
                elif error:
                    st.error(f"Error: {error}")
                else:
                    st.warning("No images found")

    elif option == "📥 Pull Image":
        st.markdown('<h2 class="section-header">Pull an Image</h2>', unsafe_allow_html=True)
        
        image_name = st.text_input("📦 Enter image name:", placeholder="e.g., nginx, ubuntu:20.04")
        
        if st.button("Pull Image"):
            if image_name:
                with st.spinner(f"Pulling {image_name}... This might take a while"):
                    output, error, return_code = run_command(f"docker pull {image_name}")
                    
                    if return_code == 0:
                        st.success(f"Successfully pulled image: {image_name}")
                        st.code(output, language='text')
                    else:
                        st.error(f"Failed to pull image: {error}")
            else:
                st.warning("⚠️ Please enter an image name")

    elif option == "🗑️ Remove Image":
        st.markdown('<h2 class="section-header">Remove an Image</h2>', unsafe_allow_html=True)
        
        image_name = st.text_input("Enter image name or ID:", placeholder="e.g., nginx, ubuntu:20.04")
        force_remove = st.checkbox("Force remove (remove even if used by containers)")
        
        if st.button("Remove Image"):
            if image_name:
                cmd = f"docker rmi {image_name}"
                if force_remove:
                    cmd += " -f"
                
                with st.spinner(f"Removing {image_name}..."):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success(f"Successfully removed image: {image_name}")
                    else:
                        st.error(f"Failed to remove image: {error}")
            else:
                st.warning("⚠️ Please enter an image name or ID")

    elif option == "🕸️ List Networks":
        st.markdown('<h2 class="section-header">All Networks</h2>', unsafe_allow_html=True)
        
        if st.button("Show Networks"):
            with st.spinner("Loading networks..."):
                output, error, return_code = run_command("docker network ls")
                
                if return_code == 0 and output:
                    st.success("✅ Networks loaded successfully!")
                    st.code(output, language='text')
                elif error:
                    st.error(f"❌ Error: {error}")

    elif option == "➕ Create Network":
        st.markdown('<h2 class="section-header">Create a Network</h2>', unsafe_allow_html=True)
        
        network_name = st.text_input("🌐 Enter network name:", placeholder="e.g., my-network")
        driver = st.selectbox("🔧 Network driver:", ["bridge", "overlay", "host", "none"])
        
        if st.button("Create Network"):
            if network_name:
                cmd = f"docker network create --driver {driver} {network_name}"
                # Use sudo only on Unix-like systems and for local context
                if os.name != 'nt' and st.session_state.get('context', 'default') == 'default':
                    cmd = f"sudo {cmd}"
                
                with st.spinner(f"Creating network {network_name}..."):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success(f"Successfully created network: {network_name}")
                        if output: st.code(output, language='text')
                    else:
                        st.error(f"Failed to create network: {error}")
            else:
                st.warning("⚠️ Please enter a network name")

    elif option == "➖ Remove Network":
        st.markdown('<h2 class="section-header">Remove a Network</h2>', unsafe_allow_html=True)
        
        network_name = st.text_input("Enter network name:", placeholder="e.g., my-network")
        
        if st.button("Remove Network"):
            if network_name:
                cmd = f"docker network rm {network_name}"
                # Use sudo only on Unix-like systems and for local context
                if os.name != 'nt' and st.session_state.get('context', 'default') == 'default':
                    cmd = f"sudo {cmd}"
                
                with st.spinner(f"Removing network {network_name}..."):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success(f"Successfully removed network: {network_name}")
                    else:
                        st.error(f"Failed to remove network: {error}")
            else:
                st.warning("⚠️ Please enter a network name")

    elif option == "💾 List Volumes":
        st.markdown('<h2 class="section-header">All Volumes</h2>', unsafe_allow_html=True)
        
        if st.button("Show Volumes"):
            with st.spinner("Loading volumes..."):
                cmd = "docker volume ls"
                # Use sudo only on Unix-like systems and for local context
                if os.name != 'nt' and st.session_state.get('context', 'default') == 'default':
                    cmd = f"sudo {cmd}"
                
                output, error, return_code = run_command(cmd)
                
                if return_code == 0 and output:
                    st.success("✅ Volumes loaded successfully!")
                    st.code(output, language='text')
                elif error:
                    st.error(f"❌ Error: {error}")

    elif option == "➕ Create Volume":
        st.markdown('<h2 class="section-header">Create a Volume</h2>', unsafe_allow_html=True)
        
        volume_name = st.text_input("💾 Enter volume name:", placeholder="e.g., my-volume")
        
        if st.button("Create Volume"):
            if volume_name:
                cmd = f"docker volume create {volume_name}"
                # Use sudo only on Unix-like systems and for local context
                if os.name != 'nt' and st.session_state.get('context', 'default') == 'default':
                    cmd = f"sudo {cmd}"
                
                with st.spinner(f"Creating volume {volume_name}..."):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success(f"Successfully created volume: {volume_name}")
                        if output: st.code(output, language='text')
                    else:
                        st.error(f"Failed to create volume: {error}")
            else:
                st.warning("⚠️ Please enter a volume name")

    elif option == "➖ Remove Volume":
        st.markdown('<h2 class="section-header">Remove a Volume</h2>', unsafe_allow_html=True)
        
        volume_name = st.text_input("💾 Enter volume name:", placeholder="e.g., my-volume")
        
        if st.button("Remove Volume"):
            if volume_name:
                cmd = f"docker volume rm {volume_name}"
                # Use sudo only on Unix-like systems and for local context
                if os.name != 'nt' and st.session_state.get('context', 'default') == 'default':
                    cmd = f"sudo {cmd}"
                
                with st.spinner(f"Removing volume {volume_name}..."):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success(f"Successfully removed volume: {volume_name}")
                    else:
                        st.error(f"Failed to remove volume: {error}")
            else:
                st.warning("⚠️ Please enter a volume name")

    elif option == "🧹 System Cleanup":
        st.markdown('<h2 class="section-header">Clean Up Docker System</h2>', unsafe_allow_html=True)
        
        st.info("This operation will remove all unused items based on your selection.")
        
        cleanup_type = st.radio("Choose cleanup type:", [
            "Standard cleanup (stopped containers, dangling images, unused networks)",
            "Aggressive cleanup (also removes unused images)",
            "Complete cleanup (aggressive + unused volumes)"
        ])
        
        if st.button("Start Cleanup"):
            if st.checkbox("Confirm you want to start the cleanup process."):
                if cleanup_type == "Standard cleanup (stopped containers, dangling images, unused networks)":
                    cmd = "docker system prune -f"
                elif cleanup_type == "Aggressive cleanup (also removes unused images)":
                    cmd = "docker system prune -a -f"
                else:  # Complete cleanup
                    cmd = "docker system prune -a -f --volumes"

                # Use sudo only on Unix-like systems and for local context
                if os.name != 'nt' and st.session_state.get('context', 'default') == 'default':
                    cmd = f"sudo {cmd}"
                
                with st.spinner("🧹 Cleaning up Docker system... This might take a while"):
                    output, error, return_code = run_command(cmd)
                    
                    if return_code == 0:
                        st.success("Docker system cleanup completed successfully!")
                        if output:
                            st.code(output, language='text')
                    else:
                        st.error(f"Cleanup failed: {error}")
            else:
                st.warning("Please check the confirmation box to proceed.")


    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🐳 <strong>Docker Manager</strong> | Made with ❤️ using Streamlit</p>
        <p>💡 <em>Tip: Use the sidebar to connect to a remote Docker host via SSH!</em></p>
    </div>
    """, unsafe_allow_html=True)



        
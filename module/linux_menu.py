def run():
    import streamlit as st
    import subprocess
    import os
    import sys
    import tempfile
    import shlex
    from datetime import datetime

    # Configure page

    # Initialize session state
    if 'command_history' not in st.session_state:
        st.session_state.command_history = []

    if 'current_directory' not in st.session_state:
        st.session_state.current_directory = '/home/user'

    if 'directory_structure' not in st.session_state:
        # Simulate a directory structure
        st.session_state.directory_structure = {
            '/home/user': ['Documents', 'Downloads', 'Pictures', 'Desktop', 'Music', 'Videos'],
            '/home/user/Documents': ['file1.txt', 'file2.pdf', 'Projects'],
            '/home/user/Documents/Projects': ['project1', 'project2', 'project3'],
            '/home/user/Downloads': ['download1.zip', 'download2.tar.gz'],
            '/home/user/Pictures': ['photo1.jpg', 'photo2.png', 'vacation'],
            '/home/user/Pictures/vacation': ['beach.jpg', 'mountain.jpg'],
            '/home/user/Desktop': ['shortcut1.lnk', 'readme.txt'],
            '/home/user/Music': ['song1.mp3', 'song2.mp3', 'albums'],
            '/home/user/Music/albums': ['album1', 'album2'],
            '/home/user/Videos': ['video1.mp4', 'video2.avi'],
            '/': ['home', 'usr', 'var', 'etc', 'bin', 'tmp'],
            '/usr': ['bin', 'lib', 'share', 'local'],
            '/var': ['log', 'tmp', 'www'],
            '/etc': ['passwd', 'hosts', 'fstab']
        }

    def get_directories_in_current_path():
        """Get directories in the current path"""
        current_path = st.session_state.current_directory
        items = st.session_state.directory_structure.get(current_path, [])
        # Filter out files (simplified: assume items without extensions are directories)
        directories = [item for item in items if '.' not in item or item.startswith('.')]
        return directories

    def get_all_items_in_current_path():
        """Get all items (files and directories) in the current path"""
        current_path = st.session_state.current_directory
        return st.session_state.directory_structure.get(current_path, [])

    def change_directory(target_dir):
        """Change to the specified directory"""
        current_path = st.session_state.current_directory
        
        if target_dir == '..':
            # Go to parent directory
            if current_path != '/':
                parent_path = '/'.join(current_path.rstrip('/').split('/')[:-1])
                if not parent_path:
                    parent_path = '/'
                st.session_state.current_directory = parent_path
                return f"Changed directory to: {st.session_state.current_directory}"
            else:
                return "Already at root directory"
        elif target_dir == '~':
            # Go to home directory
            st.session_state.current_directory = '/home/user'
            return f"Changed directory to: {st.session_state.current_directory}"
        elif target_dir == '/':
            # Go to root directory
            st.session_state.current_directory = '/'
            return f"Changed directory to: {st.session_state.current_directory}"
        else:
            # Check if target directory exists in current path
            available_dirs = get_directories_in_current_path()
            if target_dir in available_dirs:
                new_path = os.path.join(current_path, target_dir).replace('\\', '/')
                # Normalize path
                if current_path == '/':
                    new_path = '/' + target_dir
                st.session_state.current_directory = new_path
                return f"Changed directory to: {st.session_state.current_directory}"
            else:
                return f"Directory '{target_dir}' not found in current location"

    def execute_safe_command(command):
        """Execute safe Linux commands and return output"""
        # List of safe commands that can be executed
        safe_commands = {
            'ls', 'pwd', 'whoami', 'date', 'cal', 'uptime', 'id', 'w', 'who',
            'df', 'free', 'uname', 'ps', 'echo', 'cat', 'head', 'tail', 'wc',
            'sort', 'uniq', 'grep', 'find', 'which', 'locate', 'history', 'cd'
        }
        
        try:
            # Parse the command
            cmd_parts = shlex.split(command.strip())
            if not cmd_parts:
                return "No command entered"
            
            base_cmd = cmd_parts[0]
            
            # Handle special cases
            if base_cmd == 'clear':
                return "Terminal cleared (simulated)"
            
            if base_cmd == 'history':
                return "\n".join([f"{i+1}: {cmd}" for i, cmd in enumerate(st.session_state.command_history[-10:])])
            
            if base_cmd == 'help':
                return "Available commands: " + ", ".join(sorted(safe_commands))
            
            if base_cmd == 'pwd':
                return st.session_state.current_directory
            
            if base_cmd == 'ls':
                items = get_all_items_in_current_path()
                if not items:
                    return "Directory is empty"
                
                # Add directory indicators
                formatted_items = []
                directories = get_directories_in_current_path()
                for item in items:
                    if item in directories:
                        formatted_items.append(f"{item}/")
                    else:
                        formatted_items.append(item)
                
                if '-la' in cmd_parts or '-l' in cmd_parts:
                    # Long format
                    result = []
                    for item in formatted_items:
                        if item.endswith('/'):
                            result.append(f"drwxr-xr-x 2 user user 4096 Jan 1 12:00 {item}")
                        else:
                            result.append(f"-rw-r--r-- 1 user user 1024 Jan 1 12:00 {item}")
                    return "\n".join(result)
                else:
                    # Simple format
                    return "  ".join(formatted_items)
            
            if base_cmd == 'cd':
                if len(cmd_parts) == 1:
                    # Show available directories and ask user to choose
                    directories = get_directories_in_current_path()
                    if directories:
                        dir_list = "\n".join([f"  {d}/" for d in directories])
                        return f"Available directories in {st.session_state.current_directory}:\n{dir_list}\n\nSpecial options:\n  .. (parent directory)\n  ~ (home directory)\n  / (root directory)\n\nUsage: cd <directory_name>"
                    else:
                        return f"No subdirectories found in {st.session_state.current_directory}\n\nSpecial options:\n  .. (parent directory)\n  ~ (home directory)\n  / (root directory)\n\nUsage: cd <directory_name>"
                else:
                    target_dir = cmd_parts[1]
                    return change_directory(target_dir)
            
            # Check if command is in safe list
            if base_cmd not in safe_commands:
                return f"Command '{base_cmd}' is not available in this simulator for security reasons.\nUse 'help' to see available commands."
            
            # Special handling for some commands
            if base_cmd == 'cat':
                if len(cmd_parts) > 1:
                    filename = cmd_parts[1]
                    all_items = get_all_items_in_current_path()
                    directories = get_directories_in_current_path()
                    files = [item for item in all_items if item not in directories]
                    
                    if filename in files:
                        # Simulate file content based on extension
                        if filename.endswith('.txt'):
                            return f"Content of {filename}:\nThis is a sample text file.\nLine 2 of the file.\nLine 3 of the file."
                        elif filename.endswith('.pdf'):
                            return f"Cannot display binary file {filename}"
                        elif filename.endswith('.jpg') or filename.endswith('.png'):
                            return f"Cannot display image file {filename}"
                        else:
                            return f"Content of {filename}:\nSample file content for {filename}"
                    else:
                        return f"File '{filename}' not found in current directory"
                else:
                    return "Usage: cat [filename]"
            
            if base_cmd == 'echo':
                return ' '.join(cmd_parts[1:]) if len(cmd_parts) > 1 else ""
            
            # For other safe commands, provide simulated output
            if base_cmd == 'whoami':
                return "user"
            
            if base_cmd == 'date':
                return datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
            
            if base_cmd == 'uptime':
                return "12:34:56 up 1 day, 2:34, 1 user, load average: 0.15, 0.10, 0.05"
            
            if base_cmd == 'df':
                if '-h' in cmd_parts:
                    return "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        20G  8.5G   10G  46% /\ntmpfs           2.0G     0  2.0G   0% /dev/shm"
                else:
                    return "Filesystem     1K-blocks    Used Available Use% Mounted on\n/dev/sda1       20971520 8912896  10485760  46% /"
            
            if base_cmd == 'free':
                if '-h' in cmd_parts:
                    return "              total        used        free      shared  buff/cache   available\nMem:           4.0G        1.2G        1.8G         64M        1.0G        2.6G\nSwap:          2.0G          0B        2.0G"
                else:
                    return "              total        used        free      shared  buff/cache   available\nMem:        4194304     1228800     1843200       65536     1024000     2662400\nSwap:       2097152           0     2097152"
            
            # Try to execute actual command as fallback (for remaining safe commands)
            try:
                result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return result.stdout.strip() if result.stdout.strip() else "Command executed successfully (no output)"
                else:
                    return f"Error: {result.stderr.strip()}"
            except:
                return f"Command '{base_cmd}' simulated - not available in this environment"
                
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error executing command: {str(e)}"

    # Main page - Interactive Terminal
    st.title("Interactive Linux Terminal")
    st.write("Practice Linux commands in a safe environment!")

    # Show current directory
    st.info(f"Current Directory: {st.session_state.current_directory}")

    # Create two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Terminal")
        
        # Command input
        command = st.text_input(
            "Enter Linux command:",
            placeholder="e.g., ls -la, pwd, cd, whoami",
            help="Type a Linux command and press Enter to execute"
        )
        
        if st.button("Execute Command") or command:
            if command.strip():
                # Add to history
                st.session_state.command_history.append(command)
                
                # Execute command
                with st.spinner("Executing command..."):
                    output = execute_safe_command(command)
                
                # Display command and output
                st.code(f"$ {command}", language="bash")
                st.text_area("Output:", output, height=200, disabled=True)
        
        # Command history
        if st.session_state.command_history:
            st.subheader("Command History")
            with st.expander("View recent commands"):
                for i, cmd in enumerate(reversed(st.session_state.command_history[-10:]), 1):
                    if st.button(f"{cmd}", key=f"history_{i}"):
                        st.rerun()

    with col2:
        st.subheader("Quick Commands")
        st.write("Click to try these commands:")
        
        quick_commands = [
            "pwd", "whoami", "date", "ls", "ls -la", "cd", "df -h", "free -h", 
            "uname -a", "uptime", "ps aux", "echo 'Hello Linux!'"
        ]
        
        for cmd in quick_commands:
            if st.button(f"`{cmd}`", key=f"quick_{cmd}".replace(" ", "_").replace("-", "_").replace("`", "")):
                st.session_state.command_history.append(cmd)
                output = execute_safe_command(cmd)
                st.code(f"$ {cmd}", language="bash")
                st.text(output)
        
        # Directory navigation helper
        st.subheader("Directory Navigation")
        st.write("Available directories:")
        directories = get_directories_in_current_path()
        if directories:
            for directory in directories:
                if st.button(f"📁 {directory}", key=f"nav_{directory}"):
                    cd_command = f"cd {directory}"
                    st.session_state.command_history.append(cd_command)
                    output = execute_safe_command(cd_command)
                    st.success(output)
                    st.rerun()
        
        # Quick navigation buttons
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("🏠 Home", key="nav_home"):
                cd_command = "cd ~"
                st.session_state.command_history.append(cd_command)
                output = execute_safe_command(cd_command)
                st.success(output)
                st.rerun()
        
        with col_nav2:
            if st.button("⬆️ Parent", key="nav_parent"):
                cd_command = "cd .."
                st.session_state.command_history.append(cd_command)
                output = execute_safe_command(cd_command)
                st.success(output)
                st.rerun()






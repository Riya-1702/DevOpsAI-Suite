import streamlit as st
import base64
from PIL import Image, ImageDraw, ImageFont
import io

def create_finger_guide():
    """Create a visual guide for finger gestures"""
    # Create a guide image
    width, height = 800, 400
    image = Image.new('RGB', (width, height), color=(30, 30, 50))
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fall back to default if not available
    try:
        font = ImageFont.truetype("Arial", 24)
        small_font = ImageFont.truetype("Arial", 18)
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw title
    draw.text((width//2-150, 20), "Finger Gesture Guide", fill=(255, 255, 255), font=font)
    
    # Draw finger guides
    gestures = [
        ("1 Finger", "Pull Docker Image", (100, 100)),
        ("2 Fingers", "Launch Container", (250, 100)),
        ("3 Fingers", "Stop Container", (400, 100)),
        ("4 Fingers", "Start Container", (550, 100)),
        ("5 Fingers", "Remove Container", (650, 100))
    ]
    
    for i, (gesture, action, position) in enumerate(gestures):
        # Draw finger icon
        icon_x, icon_y = position
        icon_size = 80
        
        # Draw hand outline
        draw.rectangle(
            (icon_x, icon_y, icon_x + icon_size, icon_y + icon_size),
            outline=(200, 200, 200),
            width=2
        )
        
        # Draw fingers (simplified)
        finger_width = 12
        finger_spacing = 16
        finger_height = 60
        
        # Base of palm
        draw.rectangle(
            (icon_x + 10, icon_y + icon_size - 30, 
             icon_x + icon_size - 10, icon_y + icon_size - 5),
            fill=(255, 220, 200),
            outline=(200, 150, 130),
            width=1
        )
        
        # Draw fingers based on count
        finger_count = i + 1
        for f in range(5):
            finger_x = icon_x + 15 + (f * finger_spacing)
            
            # Only draw the active fingers
            if f < finger_count:
                draw.rectangle(
                    (finger_x, icon_y + 20, 
                     finger_x + finger_width, icon_y + icon_size - 30),
                    fill=(255, 220, 200),
                    outline=(200, 150, 130),
                    width=1
                )
            else:
                # Draw bent finger (shorter)
                draw.rectangle(
                    (finger_x, icon_y + icon_size - 60, 
                     finger_x + finger_width, icon_y + icon_size - 30),
                    fill=(255, 220, 200),
                    outline=(200, 150, 130),
                    width=1
                )
        
        # Draw text labels
        draw.text(
            (icon_x + icon_size//2 - 30, icon_y + icon_size + 10),
            gesture,
            fill=(0, 0, 0),  # Changed to black
            font=small_font
        )
        
        draw.text(
            (icon_x + icon_size//2 - 40, icon_y + icon_size + 35),
            action,
            fill=(0, 0, 0),  # Changed to black
            font=small_font
        )
    
    # Add instructions
    instructions = [
        "1. Start the camera using the 'Start Camera' button",
        "2. Show your hand clearly to the camera",
        "3. Hold the gesture steady for 2 seconds",
        "4. Check the command history to confirm execution"
    ]
    
    for i, instruction in enumerate(instructions):
        draw.text(
            (width//2 - 200, height - 120 + (i * 25)),
            instruction,
            fill=(200, 255, 200),
            font=small_font
        )
    
    # Convert to bytes for Streamlit
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

def get_finger_guide_html():
    """Get HTML for the finger guide to embed in the main app"""
    img_bytes = create_finger_guide()
    img_base64 = base64.b64encode(img_bytes.read()).decode()
    
    html = f"""
    <div style="text-align: center; margin: 20px 0; padding: 15px; 
              background: rgba(0,0,0,0.2); border-radius: 10px;">
        <img src="data:image/png;base64,{img_base64}" 
             style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);" />
    </div>
    """
    
    return html

# For testing the guide independently
if __name__ == "__main__":
    st.title("Finger Gesture Guide")
    st.markdown(get_finger_guide_html(), unsafe_allow_html=True)
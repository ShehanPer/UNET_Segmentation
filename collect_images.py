import cv2
import os
from datetime import datetime

# Set Raspberry Pi IP Address
RPI_IP = "192.168.43.127"  # Change this to your Pi's actual IP
STREAM_URL = f"http://{RPI_IP}:8000/video_feed"

# Create a folder to save images
save_dir = "collected_images"
os.makedirs(save_dir, exist_ok=True)

# Open video stream
cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Error: Cannot connect to the Raspberry Pi camera stream.")
    exit()

def capture_image(frame):
    """Captures a frame and saves it in RGB format."""
    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Save the image with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"image_{timestamp}.jpg")
    cv2.imwrite(filename, rgb_frame)
    print(f"Image saved: {filename}")
    return filename

def show_video_stream():
    """Shows the video stream and captures images on space key press."""
    cv2.namedWindow('Video Stream')  # Create the window first
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Resize the frame to 1/4 of the original size
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_frame = cv2.resize(frame_rgb, (width // 3, height // 3))
        
        cv2.imshow('Video Stream', resized_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # Space key to capture image
            capture_image(frame)
        elif key == ord('q'):  # 'q' key to quit
            break

    cap.release()
    cv2.destroyAllWindows()

# Show video stream and capture images on space key press
show_video_stream()
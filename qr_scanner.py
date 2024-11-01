import tkinter as tk
import numpy as np
import cv2
from pyzbar import pyzbar
from PIL import ImageGrab
from threading import Thread
import time
import socketio

# Set up the SocketIO client to communicate with the Flask server
sio = socketio.Client()

# Function to capture the screen area under the overlay
def capture_screen(overlay_position):
    x1, y1, x2, y2 = overlay_position
    print(f"[DEBUG] Capturing screen area: ({x1}, {y1}, {x2}, {y2})")
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # Capture the overlay area
    frame = np.array(image)  # Convert to a NumPy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to OpenCV BGR format
    return frame

# Function to detect QR codes and send the detected QR code to the website
def detect_qr_codes(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    qr_codes = pyzbar.decode(gray_frame)  # Detect QR codes

    if qr_codes:
        print(f"[DEBUG] Detected QR Code(s): {len(qr_codes)}")
        for qr_code in qr_codes:
            qr_data = qr_code.data.decode('utf-8')
            print(f"[DEBUG] QR Code data: {qr_data}")

            # Send the detected QR code to the website via SocketIO
            sio.emit('qr_code_detected', {'qr_data': qr_data})
        return True
    else:
        print("[DEBUG] No QR code detected")
        return False

# Function to continuously capture and detect QR codes
def start_scanning(root):
    while True:
        x1 = root.winfo_rootx()
        y1 = root.winfo_rooty()
        x2 = x1 + root.winfo_width()
        y2 = y1 + root.winfo_height()

        frame = capture_screen((x1, y1, x2, y2))  # Capture the screen area
        detect_qr_codes(frame)  # Detect QR code and send data

        time.sleep(0.001)

# Create a purple overlay window
def create_overlay():
    root = tk.Tk()
    root.geometry("400x400")  # Size of overlay
    root.title("QR Code Scanner Overlay")
    root.configure(bg="purple")
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 0.3)  # Transparent

    label = tk.Label(root, text="Move this overlay to scan QR code", bg='purple', fg='white')
    label.pack()

    # Start scanning thread
    scan_thread = Thread(target=start_scanning, args=(root,))
    scan_thread.daemon = True  # Close when window closes
    scan_thread.start()

    root.mainloop()

if __name__ == "__main__":
    # Connect to the Flask server via SocketIO
    sio.connect('http://127.0.0.1:5000')

    create_overlay()

import tkinter as tk
import subprocess
import threading
import time
import os
import signal

# Variables to hold the processes
flask_process = None
qr_process = None

def start_app():
    """Function to start both the Flask server and QR scanner."""
    global flask_process, qr_process

    def run_flask_server():
        global flask_process
        flask_process = subprocess.Popen(["python", "server.py"])

    def run_qr_scanner():
        global qr_process
        qr_process = subprocess.Popen(["python", "qr_scanner.py"])

    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.start()

    # Give the server time to start
    time.sleep(2)

    # Start the QR scanner in another thread
    qr_thread = threading.Thread(target=run_qr_scanner)
    qr_thread.start()

def stop_app():
    """Function to stop both the Flask server and QR scanner."""
    global flask_process, qr_process

    # Terminate Flask server
    if flask_process is not None:
        os.kill(flask_process.pid, signal.SIGTERM)
        flask_process = None

    # Terminate QR scanner
    if qr_process is not None:
        os.kill(qr_process.pid, signal.SIGTERM)
        qr_process = None

# Function to enhance the GUI layout
def enhance_gui():
    # Set a modern window background color
    window.configure(bg='#2C3E50')

    # Styling for the buttons
    start_button.config(
        bg="#1ABC9C",
        fg="black",
        font=("Helvetica", 14, "bold"),
        relief="flat",
        activebackground="#16A085",
        padx=20, pady=10
    )
    stop_button.config(
        bg="#E74C3C",
        fg="black",
        font=("Helvetica", 14, "bold"),
        relief="flat",
        activebackground="#C0392B",
        padx=20, pady=10
    )

    # Styling for the header label
    header_label.config(
        bg="#2C3E50",
        fg="white",
        font=("Helvetica", 18, "bold")
    )

# Create a Tkinter window
window = tk.Tk()
window.title("QR Code Application Control")
window.geometry("400x300")
window.resizable(False, False)

# Add a header label
header_label = tk.Label(window, text="QR Code Application", padx=10, pady=20)
header_label.pack()

# Create a Start button to start the Flask server and QR scanner
start_button = tk.Button(window, text="Start Application", command=start_app)
start_button.pack(pady=20)

# Create a Stop button to stop the Flask server and QR scanner
stop_button = tk.Button(window, text="Stop Application", command=stop_app)
stop_button.pack(pady=20)

# Enhance the GUI layout
enhance_gui()

# Run the Tkinter window loop
window.mainloop()

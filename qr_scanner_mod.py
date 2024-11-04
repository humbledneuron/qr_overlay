# import tkinter as tk
# import numpy as np
# import cv2
# from pyzbar import pyzbar
# from PIL import ImageGrab
# from threading import Thread
# import time
# import socketio

# # Set up the SocketIO client
# sio = socketio.Client()

# def capture_screen(overlay_position):
#     x1, y1, x2, y2 = overlay_position
#     print(f"[DEBUG] Capturing screen area: ({x1}, {y1}, {x2}, {y2})")
#     image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
#     frame = np.array(image)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#     return frame

# def detect_qr_codes(frame):
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     qr_codes = pyzbar.decode(gray_frame)

#     if qr_codes:
#         print(f"[DEBUG] Detected QR Code(s): {len(qr_codes)}")
#         for qr_code in qr_codes:
#             qr_data = qr_code.data.decode('utf-8')
#             print(f"[DEBUG] QR Code data: {qr_data}")
#             sio.emit('qr_code_detected', {'qr_data': qr_data})
#         return True
#     else:
#         print("[DEBUG] No QR code detected")
#         return False

# stop_scanning = False

# def start_scanning(root):
#     global stop_scanning
#     while not stop_scanning:
#         x1 = root.winfo_rootx()
#         y1 = root.winfo_rooty()
#         x2 = x1 + root.winfo_width()
#         y2 = y1 + root.winfo_height()

#         frame = capture_screen((x1, y1, x2, y2))
#         detect_qr_codes(frame)

#         time.sleep(0.1)

# def create_overlay():
#     global stop_scanning
    
#     # Create main window
#     root = tk.Tk()
#     root.geometry("400x500")  # Increased height for buttons
#     root.title("QR Code Scanner Overlay")
    
#     # Make the main window semi-transparent purple
#     root.configure(bg="purple")
#     root.wm_attributes("-alpha", 0.3)
#     root.wm_attributes("-topmost", True)

#     # Create a separate window for buttons that isn't transparent
#     button_window = tk.Toplevel(root)
#     button_window.geometry("400x200")
#     button_window.title("Control Panel")
#     button_window.configure(bg="#f0f0f0")
#     button_window.wm_attributes("-topmost", True)
    
#     # Keep button window aligned with main window
#     def align_windows(event=None):
#         x = root.winfo_x()
#         y = root.winfo_y() + root.winfo_height()
#         button_window.geometry(f"+{x}+{y}")
    
#     root.bind("<Configure>", align_windows)

#     # Frame for buttons
#     button_frame = tk.Frame(button_window, bg="#f0f0f0", padx=20, pady=10)
#     button_frame.pack(expand=True, fill="both")

#     # Instructions label
#     label = tk.Label(button_frame, 
#                      text="Move the purple overlay to scan QR code",
#                      font=('Arial', 12),
#                      bg="#f0f0f0",
#                      fg='black')
#     label.pack(pady=10)

#     def step_clicked(step_number):
#         print(f"[DEBUG] Step {step_number} completed")
#         sio.emit('step_completed', {'step': step_number})

#     # Create styled buttons
#     button_style = {
#         'font': ('Arial', 12, 'bold'),
#         'width': 20,
#         'height': 2,
#         'relief': 'raised',
#         'cursor': 'hand2'
#     }

#     btn1 = tk.Button(button_frame, 
#                      text="Complete Step 1",
#                      command=lambda: step_clicked(1),
#                      bg='#8B5CF6',
#                      fg='white',
#                      activebackground='#7C3AED',
#                      **button_style)
#     btn1.pack(pady=5)

#     btn2 = tk.Button(button_frame,
#                      text="Complete Step 2",
#                      command=lambda: step_clicked(2),
#                      bg='#8B5CF6',
#                      fg='white',
#                      activebackground='#7C3AED',
#                      **button_style)
#     btn2.pack(pady=5)

#     btn3 = tk.Button(button_frame,
#                      text="Complete Step 3",
#                      command=lambda: step_clicked(3),
#                      bg='#8B5CF6',
#                      fg='white',
#                      activebackground='#7C3AED',
#                      **button_style)
#     btn3.pack(pady=5)

#     # Start scanning thread
#     scan_thread = Thread(target=start_scanning, args=(root,))
#     scan_thread.daemon = True
#     scan_thread.start()

#     def on_close():
#         global stop_scanning
#         stop_scanning = True
#         root.destroy()
#         button_window.destroy()

#     root.protocol("WM_DELETE_WINDOW", on_close)
#     button_window.protocol("WM_DELETE_WINDOW", on_close)
    
#     # Initial alignment of windows
#     align_windows()
    
#     root.mainloop()

# if __name__ == "__main__":
#     connected = False
#     while not connected:
#         try:
#             sio.connect('http://127.0.0.1:5000')
#             connected = True
#         except socketio.exceptions.ConnectionError:
#             print("Retrying connection to server...")
#             time.sleep(5)
    
#     create_overlay()


# new but not beautiful

# import tkinter as tk
# from tkinter import ttk
# import numpy as np
# import cv2
# from pyzbar import pyzbar
# from PIL import ImageGrab, Image, ImageTk
# from threading import Thread
# import time
# import socketio
# import os

# # Set up the SocketIO client
# sio = socketio.Client()

# # Global control variable
# stop_scanning = False

# class ModernButton(tk.Button):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)
#         self.bind("<Enter>", self.on_enter)
#         self.bind("<Leave>", self.on_leave)
        
#     def on_enter(self, e):
#         self['background'] = '#7C3AED'
        
#     def on_leave(self, e):
#         self['background'] = '#8B5CF6'

# def scan_for_qr_codes(frame):
#     # Convert frame to grayscale
#     gray = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2GRAY)
#     # Decode QR codes
#     qr_codes = pyzbar.decode(gray)
#     return qr_codes

# def start_scanning(root):
#     global stop_scanning
    
#     while not stop_scanning:
#         try:
#             # Get the window position
#             x = root.winfo_x()
#             y = root.winfo_y()
#             width = root.winfo_width()
#             height = root.winfo_height()
            
#             # Capture the screen area within the window
#             screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
#             # Scan for QR codes
#             qr_codes = scan_for_qr_codes(screenshot)
            
#             # Process found QR codes
#             for qr_code in qr_codes:
#                 data = qr_code.data.decode('utf-8')
#                 print(f"QR Code detected: {data}")
#                 # Emit the data through socket
#                 try:
#                     sio.emit('qr_code_scanned', {'data': data})
#                 except Exception as e:
#                     print(f"Socket emission error: {e}")
            
#             # Add a small delay to prevent high CPU usage
#             time.sleep(0.1)
            
#         except Exception as e:
#             print(f"Scanning error: {e}")
#             time.sleep(1)  # Longer delay on error

# def create_overlay():
#     global stop_scanning
#     stop_scanning = False
    
#     # Create main window
#     root = tk.Tk()
#     root.geometry("400x500")
#     root.title("QR Scanner")
    
#     # Configure the main window style
#     root.configure(bg="#4B0082")  # Deep purple background
#     root.attributes("-alpha", 0.3)  # Changed from wm_attributes
#     root.attributes("-topmost", True)

#     # Create control panel window
#     control_panel = tk.Toplevel(root)
#     control_panel.geometry("400x300")
#     control_panel.title("Scanner Controls")
#     control_panel.configure(bg="#F3F4F6")
#     control_panel.attributes("-topmost", True)

#     # Style configuration
#     style = ttk.Style()
#     style.configure("Modern.TFrame", background="#F3F4F6")
#     style.configure("Title.TLabel", 
#                    background="#F3F4F6",
#                    foreground="#1F2937",
#                    font=('Segoe UI', 14, 'bold'))
#     style.configure("Subtitle.TLabel",
#                    background="#F3F4F6",
#                    foreground="#4B5563",
#                    font=('Segoe UI', 10))

#     # Main frame
#     main_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
#     main_frame.pack(expand=True, fill="both")

#     # Title and instructions
#     title = ttk.Label(main_frame, 
#                      text="QR Code Scanner",
#                      style="Title.TLabel")
#     title.pack(pady=(0, 5))

#     subtitle = ttk.Label(main_frame,
#                         text="Move the purple overlay over a QR code",
#                         style="Subtitle.TLabel")
#     subtitle.pack(pady=(0, 20))

#     # Status label to show scanning results
#     status_var = tk.StringVar(value="Scanner Active")
#     status_label = ttk.Label(main_frame,
#                             textvariable=status_var,
#                             style="Subtitle.TLabel")
#     status_label.pack(pady=(0, 10))

#     # Button frame
#     button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
#     button_frame.pack(expand=True, fill="both")

#     def step_clicked(step_number):
#         try:
#             print(f"[DEBUG] Step {step_number} completed")
#             sio.emit('step_completed', {'step': step_number})
#             status_var.set(f"Step {step_number} completed")
#         except Exception as e:
#             status_var.set(f"Error: {str(e)}")

#     # Create buttons with modern styling
#     for i in range(1, 4):
#         ModernButton(
#             button_frame,
#             text=f"Complete Step {i}",
#             command=lambda x=i: step_clicked(x),
#             font=('Segoe UI', 11, 'bold'),
#             fg='white',
#             bg='#8B5CF6',
#             activeforeground='white',
#             activebackground='#7C3AED',
#             relief='flat',
#             pady=10,
#             cursor='hand2'
#         ).pack(fill='x', pady=5)

#     # Keep windows aligned
#     def align_windows(event=None):
#         x = root.winfo_x()
#         y = root.winfo_y() + root.winfo_height()
#         control_panel.geometry(f"+{x}+{y}")
    
#     root.bind("<Configure>", align_windows)

#     # Initialize SocketIO connection
#     try:
#         sio.connect('http://localhost:5000')  # Replace with your server URL
#         status_var.set("Connected to server")
#     except Exception as e:
#         status_var.set(f"Server connection error: {str(e)}")

#     # Start scanning in a separate thread
#     scan_thread = Thread(target=start_scanning, args=(root,))
#     scan_thread.daemon = True
#     scan_thread.start()

#     def on_close():
#         global stop_scanning
#         stop_scanning = True
#         try:
#             sio.disconnect()
#         except:
#             pass
#         root.destroy()
#         control_panel.destroy()

#     root.protocol("WM_DELETE_WINDOW", on_close)
#     control_panel.protocol("WM_DELETE_WINDOW", on_close)
    
#     align_windows()
#     root.mainloop()

# if __name__ == "__main__":
#     create_overlay()


# new from deepseek
import tkinter as tk
from tkinter import ttk
import numpy as np
import cv2
from pyzbar import pyzbar
from PIL import ImageGrab, Image, ImageTk
from threading import Thread
import time
import socketio
import os

# Set up the SocketIO client
sio = socketio.Client()

# Global control variable
stop_scanning = False

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self['background'] = '#7C3AED'
        
    def on_leave(self, e):
        self['background'] = '#8B5CF6'

def scan_for_qr_codes(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2GRAY)
    # Decode QR codes
    qr_codes = pyzbar.decode(gray)
    return qr_codes

def start_scanning(root):
    global stop_scanning
    
    while not stop_scanning:
        try:
            # Get the window position
            x = root.winfo_x()
            y = root.winfo_y()
            width = root.winfo_width()
            height = root.winfo_height()
            
            # Capture the screen area within the window
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
            # Scan for QR codes
            qr_codes = scan_for_qr_codes(screenshot)
            
            # Process found QR codes
            for qr_code in qr_codes:
                data = qr_code.data.decode('utf-8')
                print(f"QR Code detected: {data}")
                # Emit the data through socket
                try:
                    sio.emit('qr_code_scanned', {'data': data})
                except Exception as e:
                    print(f"Socket emission error: {e}")
            
            # Add a small delay to prevent high CPU usage
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Scanning error: {e}")
            time.sleep(1)  # Longer delay on error

def create_overlay():
    global stop_scanning
    stop_scanning = False
    
    # Create main window
    root = tk.Tk()
    root.geometry("400x500")
    root.title("QR Scanner")
    
    # Configure the main window style
    root.configure(bg="#4B0082")  # Deep purple background
    root.attributes("-alpha", 0.3)  # Changed from wm_attributes
    root.attributes("-topmost", True)

    # Create control panel window
    control_panel = tk.Toplevel(root)
    control_panel.geometry("400x300")
    control_panel.title("Scanner Controls")
    control_panel.configure(bg="#F3F4F6")
    control_panel.attributes("-topmost", True)

    # Style configuration
    style = ttk.Style()
    style.configure("Modern.TFrame", background="#F3F4F6")
    style.configure("Title.TLabel", 
                   background="#F3F4F6",
                   foreground="#1F2937",
                   font=('Segoe UI', 14, 'bold'))
    style.configure("Subtitle.TLabel",
                   background="#F3F4F6",
                   foreground="#4B5563",
                   font=('Segoe UI', 10))

    # Main frame
    main_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
    main_frame.pack(expand=True, fill="both")

    # Title and instructions
    title = ttk.Label(main_frame, 
                     text="QR Code Scanner",
                     style="Title.TLabel")
    title.pack(pady=(0, 5))

    subtitle = ttk.Label(main_frame,
                        text="Move the purple overlay over a QR code",
                        style="Subtitle.TLabel")
    subtitle.pack(pady=(0, 20))

    # Status label to show scanning results
    status_var = tk.StringVar(value="Scanner Active")
    status_label = ttk.Label(main_frame,
                            textvariable=status_var,
                            style="Subtitle.TLabel")
    status_label.pack(pady=(0, 10))

    # Button frame
    button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
    button_frame.pack(expand=True, fill="both")

    def step_clicked(step_number):
        try:
            print(f"[DEBUG] Step {step_number} completed")
            sio.emit('step_completed', {'step': step_number})
            status_var.set(f"Step {step_number} completed")
        except Exception as e:
            status_var.set(f"Error: {str(e)}")

    # Create buttons with modern styling
    for i in range(1, 4):
        ModernButton(
            button_frame,
            text=f"Step {i}",
            command=lambda x=i: step_clicked(x),
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#8B5CF6',
            activeforeground='white',
            activebackground='#7C3AED',
            relief='flat',
            cursor='hand2',
            bd=0,
            highlightthickness=1,
            padx=10,
            pady=5,
            highlightbackground="#8B5CF6",
            highlightcolor="#8B5CF6",
            borderwidth=0,
            width=10,
            height=1,
            compound='left',
            image=None,  # Add an icon here if you have one
            anchor='center'
        ).pack(fill='x', pady=5)

    # Keep windows aligned
    def align_windows(event=None):
        x = root.winfo_x()
        y = root.winfo_y() + root.winfo_height()
        control_panel.geometry(f"+{x}+{y}")
    
    root.bind("<Configure>", align_windows)

    # Initialize SocketIO connection
    try:
        sio.connect('http://127.0.0.1:5000')  # Replace with your server URL
        status_var.set("Connected to server")
    except Exception as e:
        status_var.set(f"Server connection error: {str(e)}")

    # Start scanning in a separate thread
    scan_thread = Thread(target=start_scanning, args=(root,))
    scan_thread.daemon = True
    scan_thread.start()

    def on_close():
        global stop_scanning
        stop_scanning = True
        try:
            sio.disconnect()
        except:
            pass
        root.destroy()
        control_panel.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    control_panel.protocol("WM_DELETE_WINDOW", on_close)
    
    align_windows()
    root.mainloop()

if __name__ == "__main__":
    create_overlay()
import tkinter as tk
from tkinter import ttk
import numpy as np
import cv2
from pyzbar import pyzbar
from PIL import ImageGrab, Image, ImageTk
from threading import Thread
import time
import socketio

# Set up the SocketIO client
sio = socketio.Client()

# Global control variable
stop_scanning = False
scanned_data = {}  # Store scanned data

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
    global stop_scanning, scanned_data
    
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
                # Store the scanned data
                scanned_data = {'data': data}
                # Emit the data through socket
                try:
                    sio.emit('qr_code_scanned', scanned_data)
                except Exception as e:
                    print(f"Socket emission error: {e}")
            
            # Add a small delay to prevent high CPU usage
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Scanning error: {e}")
            time.sleep(1)  # Longer delay on error

def create_step1_frame(control_panel, step1_button, step2_button, step3_button):
    global scanned_data

    # Create a new frame for step 1
    step1_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
    step1_frame.pack(expand=True, fill="both")

    # Add "Enter" and "Complete" buttons
    date_label = ttk.Label(step1_frame, text="Date:", style="Subtitle.TLabel")
    date_label.pack(fill='x', pady=5)
    date_entry = ttk.Entry(step1_frame)
    date_entry.pack(fill='x', pady=5)

    address_label = ttk.Label(step1_frame, text="Address:", style="Subtitle.TLabel")
    address_label.pack(fill='x', pady=5)
    address_entry = ttk.Entry(step1_frame)
    address_entry.pack(fill='x', pady=5)

    complete_button = ModernButton(
        step1_frame,
        text="Complete",
        command=lambda: complete_step1(step1_frame, date_entry, address_entry, scanned_data, step1_button, complete_button, step2_button, step3_button),
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
        anchor='center'
    )
    complete_button.pack(fill='x', pady=5)

    return step1_frame

def complete_step1(step1_frame, date_entry, address_entry, scanned_data, step1_button, complete_button, step2_button, step3_button):
    # Get the input data
    date = date_entry.get()
    address = address_entry.get()
    
    # Combine the scanned data and user input
    step1_data = {**scanned_data, 'date': date, 'address': address}
    
    try:
        print(f"[DEBUG] Step 1 completed with data: {step1_data}")
        sio.emit('step_completed', {'step': 1, 'data': step1_data})
        step1_frame.pack_forget()  # Hide the step 1 frame
        step1_button.config(state="disabled")
        complete_button.config(state="disabled")
        step2_button.config(state="normal")
        step3_button.config(state="normal")
    except Exception as e:
        print(f"Error: {str(e)}")

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

    step1_button = ModernButton(
        button_frame,
        text="Step 1",
        command=lambda: step_clicked(1, step1_button, step2_button, step3_button),
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
        anchor='center'
    )
    step1_button.pack(fill='x', pady=5)

    step2_button = ModernButton(
        button_frame,
        text="Step 2",
        command=lambda: step_clicked(2, step1_button, step2_button, step3_button),
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
        anchor='center'
    )
    step2_button.pack(fill='x', pady=5)
    step2_button.config(state="disabled")

    step3_button = ModernButton(
        button_frame,
        text="Step 3",
        command=lambda: step_clicked(3, step1_button, step2_button, step3_button),
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
        anchor='center'
    )
    step3_button.pack(fill='x', pady=5)
    step3_button.config(state="disabled")

    def step_clicked(step_number, step1_button, step2_button, step3_button):
        if step_number == 1:
            step1_frame = create_step1_frame(main_frame, step1_button, step2_button, step3_button)
            button_frame.pack_forget()  # Hide the main button frame
            step1_frame.pack(expand=True, fill="both")
        else:
            try:
                print(f"[DEBUG] Step {step_number} completed")
                sio.emit('step_completed', {'step': step_number, 'data': scanned_data})
                status_var.set(f"Step {step_number} completed")
            except Exception as e:
                status_var.set(f"Error: {str(e)}")

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
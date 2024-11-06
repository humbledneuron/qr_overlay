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
    gray = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2GRAY)
    qr_codes = pyzbar.decode(gray)
    return qr_codes

def start_scanning(root):
    global stop_scanning, scanned_data
    
    while not stop_scanning:
        try:
            x = root.winfo_x()
            y = root.winfo_y()
            width = root.winfo_width()
            height = root.winfo_height()
            
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            qr_codes = scan_for_qr_codes(screenshot)
            
            for qr_code in qr_codes:
                data = qr_code.data.decode('utf-8')
                print(f"QR Code detected: {data}")
                scanned_data = {'data': data}
                try:
                    sio.emit('qr_code_scanned', scanned_data)
                except Exception as e:
                    print(f"Socket emission error: {e}")
            
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Scanning error: {e}")
            time.sleep(1)

def create_step1_frame(control_panel, step1_button, step2_button, step3_button, button_frame):
    global scanned_data

    step1_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
    step1_frame.pack(expand=True, fill="both")

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
        command=lambda: complete_step1(step1_frame, date_entry, address_entry, scanned_data, step1_button, step2_button, step3_button, button_frame),
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

def create_step2_frame(control_panel, step1_button, step2_button, step3_button, button_frame):
    global scanned_data

    step2_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
    step2_frame.pack(expand=True, fill="both")

    owner_label = ttk.Label(step2_frame, text="Owner:", style="Subtitle.TLabel")
    owner_label.pack(fill='x', pady=5)
    owner_entry = ttk.Entry(step2_frame)
    owner_entry.pack(fill='x', pady=5)

    renter_label = ttk.Label(step2_frame, text="Renter:", style="Subtitle.TLabel")
    renter_label.pack(fill='x', pady=5)
    renter_entry = ttk.Entry(step2_frame)
    renter_entry.pack(fill='x', pady=5)

    complete_button = ModernButton(
        step2_frame,
        text="Complete",
        command=lambda: complete_step2(step2_frame, owner_entry, renter_entry, scanned_data, step1_button, step2_button, step3_button, button_frame),
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

    return step2_frame

def complete_step1(step1_frame, date_entry, address_entry, scanned_data, step1_button, step2_button, step3_button, button_frame):
    date = date_entry.get()
    address = address_entry.get()
    step1_data = {**scanned_data, 'date': date, 'address': address}
    
    try:
        print(f"[DEBUG] Step 1 completed with data: {step1_data}")
        sio.emit('step_completed', {'step': 1, 'data': step1_data})
        step1_frame.pack_forget()
        step1_button.config(state="disabled")
        step2_button.config(state="normal")
        step3_button.config(state="disabled")
        button_frame.pack(expand=True, fill="both")
    except Exception as e:
        print(f"Error: {str(e)}")

def complete_step2(step2_frame, owner_entry, renter_entry, scanned_data, step1_button, step2_button, step3_button, button_frame):
    owner = owner_entry.get()
    renter = renter_entry.get()
    step2_data = {**scanned_data, 'owner': owner, 'renter': renter}
    
    try:
        print(f"[DEBUG] Step 2 completed with data: {step2_data}")
        sio.emit('step_completed', {'step': 2, 'data': step2_data})
        step2_frame.pack_forget()
        step1_button.config(state="disabled")
        step2_button.config(state="disabled")
        step3_button.config(state="normal")
        button_frame.pack(expand=True, fill="both")
    except Exception as e:
        print(f"Error: {str(e)}")

def create_overlay():
    global stop_scanning
    stop_scanning = False
    
    root = tk.Tk()
    root.geometry("400x400")
    root.title("QR Scanner")
    root.configure(bg="#4B0082")
    root.attributes("-alpha", 0.3)
    root.attributes("-topmost", True)

    control_panel = tk.Toplevel(root)
    control_panel.geometry("400x400")
    control_panel.title("Scanner Controls")
    control_panel.configure(bg="#F3F4F6")
    control_panel.attributes("-topmost", True)

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

    main_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
    main_frame.pack(expand=True, fill="both")

    title = ttk.Label(main_frame, 
                     text="QR Code Scanner",
                     style="Title.TLabel")
    title.pack(pady=(0, 5))

    subtitle = ttk.Label(main_frame,
                        text="Move the purple overlay over a QR code",
                        style="Subtitle.TLabel")
    subtitle.pack(pady=(0, 20))

    status_var = tk.StringVar(value="Scanner Active")
    status_label = ttk.Label(main_frame,
                            textvariable=status_var,
                            style="Subtitle.TLabel")
    status_label.pack(pady=(0, 10))

    button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
    button_frame.pack(expand=True, fill="both")

    step1_button = ModernButton(
        button_frame,
        text="Step 1",
        command=lambda: step_clicked(1, step1_button, step2_button, step3_button, button_frame),
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
        command=lambda: step_clicked(2, step1_button, step2_button, step3_button, button_frame),
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
        command=lambda: step_clicked(3, step1_button, step2_button, step3_button, button_frame),
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

    def step_clicked(step_number, step1_button, step2_button, step3_button, button_frame):
        if step_number == 1:
            step1_frame = create_step1_frame(main_frame, step1_button, step2_button, step3_button, button_frame)
            button_frame.pack_forget()
            step1_frame.pack(expand=True, fill="both")
        elif step_number == 2:
            step2_frame = create_step2_frame(main_frame, step1_button, step2_button, step3_button, button_frame)
            button_frame.pack_forget()
            step2_frame.pack(expand=True, fill="both")
        else:
            try:
                print(f"[DEBUG] Step {step_number} completed")
                sio.emit('step_completed', {'step': step_number, 'data': scanned_data})
                status_var.set(f"Step {step_number} completed")
            except Exception as e:
                status_var.set(f"Error: {str(e)}")

    def align_windows(event=None):
        x = root.winfo_x()
        y = root.winfo_y() + root.winfo_height()
        control_panel.geometry(f"+{x}+{y}")
    
    root.bind("<Configure>", align_windows)

    try:
        sio.connect('http://127.0.0.1:5000')
        status_var.set("Connected to server")
    except Exception as e:
        status_var.set(f"Server connection error: {str(e)}")

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
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

    # print(f"QR Codes detected: {len(qr_codes)}")
    # print(f"QR Codes detected: {qr_codes}")
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

    step_1_label = ttk.Label(step1_frame, text="Step 1", style="Subtitle.TLabel", font=('Segoe UI', 12, 'bold'))
    step_1_label.pack(side='top', pady=5)

    date_label = ttk.Label(step1_frame, text="Date:", style="Subtitle.TLabel")
    date_label.pack(fill='x', pady=2)
    date_entry = ttk.Entry(step1_frame)
    date_entry.pack(fill='x', pady=2)

    address_label = ttk.Label(step1_frame, text="Address:", style="Subtitle.TLabel")
    address_label.pack(fill='x', pady=2)
    address_entry = ttk.Entry(step1_frame)
    address_entry.pack(fill='x', pady=2)

    validation_label = ttk.Label(step1_frame, text="", style="Subtitle.TLabel")
    validation_label.pack(fill='x', pady=2)

    # Navigation buttons frame
    nav_frame = ttk.Frame(step1_frame, style="Modern.TFrame")
    nav_frame.pack(fill='x', pady=4)

    back_button = ModernButton(
        nav_frame,
        text="Back",
        command=lambda: back_to_steps(step1_frame, step1_button, step2_button, step3_button, button_frame),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    back_button.pack(side='left', padx=5)

    next_button = ModernButton(
        nav_frame,
        text="Next",
        command=lambda: show_completion_page(step1_frame, date_entry, address_entry, scanned_data, 
                                           step1_button, step2_button, step3_button, button_frame, 1),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    next_button.pack(side='right', padx=5)

    return step1_frame

def create_step2_frame(control_panel, step1_button, step2_button, step3_button, button_frame):
    global scanned_data

    step2_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
    step2_frame.pack(expand=True, fill="both")

    step_2_label = ttk.Label(step2_frame, text="Step 2", style="Subtitle.TLabel", font=('Segoe UI', 12, 'bold'))
    step_2_label.pack(side='top', pady=5)

    owner_label = ttk.Label(step2_frame, text="Owner:", style="Subtitle.TLabel")
    owner_label.pack(fill='x', pady=5)
    owner_entry = ttk.Entry(step2_frame)
    owner_entry.pack(fill='x', pady=5)

    renter_label = ttk.Label(step2_frame, text="Renter:", style="Subtitle.TLabel")
    renter_label.pack(fill='x', pady=5)
    renter_entry = ttk.Entry(step2_frame)
    renter_entry.pack(fill='x', pady=5)

    personal_code_label = ttk.Label(step2_frame, text="Personal code:", style="Subtitle.TLabel")
    personal_code_label.pack(fill='x', pady=5)
    personal_code_entry = ttk.Entry(step2_frame)
    personal_code_entry.pack(fill='x', pady=5)

    validation_label = ttk.Label(step2_frame, text="", style="Subtitle.TLabel")
    validation_label.pack(fill='x', pady=5)

    # Navigation buttons frame
    nav_frame = ttk.Frame(step2_frame, style="Modern.TFrame")
    nav_frame.pack(fill='x', pady=10)

    back_button = ModernButton(
        nav_frame,
        text="Back",
        command=lambda: back_to_steps(step2_frame, step1_button, step2_button, step3_button, button_frame),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    back_button.pack(side='left', padx=5)

    next_button = ModernButton(
        nav_frame,
        text="Next",
        command=lambda: show_signing_page(
            step2_frame,
            owner_entry,
            renter_entry,
            personal_code_entry,
            step1_button,
            step2_button,
            step3_button,
            button_frame
        ),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    next_button.pack(side='right', padx=5)

    return step2_frame

def show_signing_page(previous_frame, owner_entry, renter_entry, personal_code_entry, step1_button, step2_button, step3_button, button_frame):
    """Show the signing page for step 2."""
    
    # Validate entries first
    if not all([owner_entry.get(), renter_entry.get(), personal_code_entry.get()]):
        validation_label = ttk.Label(previous_frame, text="Please fill in all fields", style="Subtitle.TLabel", foreground="red")
        validation_label.pack(pady=10)
        return

    signing_frame = ttk.Frame(previous_frame.master, style="Modern.TFrame", padding="20")
    previous_frame.pack_forget()
    signing_frame.pack(expand=True, fill="both")

    title_label = ttk.Label(signing_frame, text="Signatures Required", style="Title.TLabel")
    title_label.pack(pady=20)

    # Owner signing section
    owner_sign_frame = ttk.Frame(signing_frame, style="Modern.TFrame")
    owner_sign_frame.pack(fill='x', pady=10)
    owner_sign_label = ttk.Label(owner_sign_frame, text=f"Is {owner_entry.get()} (Owner) signed in?", style="Subtitle.TLabel")
    owner_sign_label.pack(side='left', padx=5)
    owner_sign_var = tk.StringVar(value="")
    owner_sign_yes = ttk.Radiobutton(owner_sign_frame, text="Yes", variable=owner_sign_var, value="Yes", style="Modern.TRadiobutton")
    owner_sign_yes.pack(side='left', padx=5)
    owner_sign_no = ttk.Radiobutton(owner_sign_frame, text="No", variable=owner_sign_var, value="No", style="Modern.TRadiobutton")
    owner_sign_no.pack(side='left', padx=5)

    # Renter signing section
    renter_sign_frame = ttk.Frame(signing_frame, style="Modern.TFrame")
    renter_sign_frame.pack(fill='x', pady=10)
    renter_sign_label = ttk.Label(renter_sign_frame, text=f"Is {renter_entry.get()} (Renter) signed in?", style="Subtitle.TLabel")
    renter_sign_label.pack(side='left', padx=5)
    renter_sign_var = tk.StringVar(value="")
    renter_sign_yes = ttk.Radiobutton(renter_sign_frame, text="Yes", variable=renter_sign_var, value="Yes", style="Modern.TRadiobutton")
    renter_sign_yes.pack(side='left', padx=5)
    renter_sign_no = ttk.Radiobutton(renter_sign_frame, text="No", variable=renter_sign_var, value="No", style="Modern.TRadiobutton")
    renter_sign_no.pack(side='left', padx=5)

    validation_label = ttk.Label(signing_frame, text="", style="Subtitle.TLabel", foreground="red")
    validation_label.pack(pady=10)

    # Navigation buttons
    nav_frame = ttk.Frame(signing_frame, style="Modern.TFrame")
    nav_frame.pack(fill='x', pady=10)

    back_button = ModernButton(
        nav_frame,
        text="Back",
        command=lambda: back_to_form(signing_frame, previous_frame),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    back_button.pack(side='left', padx=5)

    next_button = ModernButton(
        nav_frame,
        text="Next",
        command=lambda: validate_and_show_completion(
            signing_frame,
            owner_entry,
            renter_entry,
            personal_code_entry,
            owner_sign_var,
            renter_sign_var,
            step1_button,
            step2_button,
            step3_button,
            button_frame,
            validation_label
        ),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    next_button.pack(side='right', padx=5)

def validate_and_show_completion(signing_frame, owner_entry, renter_entry, personal_code_entry, 
                               owner_sign_var, renter_sign_var, step1_button, step2_button, 
                               step3_button, button_frame, validation_label):
    """Validate signatures and show completion page if valid."""
    
    # Validate signatures
    if not owner_sign_var.get() or not renter_sign_var.get():
        validation_label.config(text="Please select signing status for both owner and renter")
        return

    # Store the data in global scanned_data
    global scanned_data
    scanned_data.update({
        'owner': owner_entry.get(),
        'renter': renter_entry.get(),
        'personal_code': personal_code_entry.get(),
        'owner_sign': owner_sign_var.get(),
        'renter_sign': renter_sign_var.get()
    })

    # Show completion page
    show_completion_page(
        signing_frame,
        owner_entry,
        renter_entry,
        personal_code_entry,
        owner_sign_var,
        renter_sign_var,
        scanned_data,
        step1_button,
        step2_button,
        step3_button,
        button_frame,
        2
    )

def create_step3_frame(control_panel, step1_button, step2_button, step3_button, button_frame):
    global scanned_data

    step3_frame = ttk.Frame(control_panel, style="Modern.TFrame", padding="20")
    step3_frame.pack(expand=True, fill="both")

    step_3_label = ttk.Label(step3_frame, text="Step 3", style="Subtitle.TLabel", font=('Segoe UI', 12, 'bold'))
    step_3_label.pack(side='top', pady=5)

    owner_label = ttk.Label(step3_frame, text="Owner:", style="Subtitle.TLabel")
    owner_label.pack(fill='x', pady=2)
    owner_entry = ttk.Entry(step3_frame)
    owner_entry.pack(fill='x', pady=2)
    # Pre-fill owner data if available
    if 'owner' in scanned_data:
        owner_entry.insert(0, scanned_data['owner'])
        owner_entry.config(state='readonly')  # Make it read-only

    renter_label = ttk.Label(step3_frame, text="Renter:", style="Subtitle.TLabel")
    renter_label.pack(fill='x', pady=2)
    renter_entry = ttk.Entry(step3_frame)
    renter_entry.pack(fill='x', pady=2)
    # Pre-fill renter data if available
    if 'renter' in scanned_data:
        renter_entry.insert(0, scanned_data['renter'])
        renter_entry.config(state='readonly')  # Make it read-only

    code_label = ttk.Label(step3_frame, text="Code:", style="Subtitle.TLabel")
    code_label.pack(fill='x', pady=2)
    code_entry = ttk.Entry(step3_frame)
    code_entry.pack(fill='x', pady=2)

    validation_label = ttk.Label(step3_frame, text="", style="Subtitle.TLabel")
    validation_label.pack(fill='x', pady=2)

    # Navigation buttons frame
    nav_frame = ttk.Frame(step3_frame, style="Modern.TFrame")
    nav_frame.pack(fill='x', pady=10)

    back_button = ModernButton(
        nav_frame,
        text="Back",
        command=lambda: back_to_steps(step3_frame, step1_button, step2_button, step3_button, button_frame),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    back_button.pack(side='left', padx=5)

    next_button = ModernButton(
        nav_frame,
        text="Next",
        command=lambda: show_completion_page(
            step3_frame, owner_entry, renter_entry, code_entry,
            scanned_data, step1_button, step2_button, step3_button, button_frame, 3
        ),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=10
    )
    next_button.pack(side='right', padx=5)

    return step3_frame

def complete_step(completion_frame, *args):
    """
    Complete a step in the QR scanner process.
    
    Args structure varies by step:
    Step 1: (entry1, entry2, scanned_data, step1_btn, step2_btn, step3_btn, button_frame, step_number)
    Step 2: (owner_entry, renter_entry, personal_code_entry, owner_sign_var, renter_sign_var, 
             scanned_data, step1_btn, step2_btn, step3_btn, button_frame, step_number)
    Step 3: (owner_entry, renter_entry, code_entry, scanned_data, step1_btn, step2_btn, step3_btn, 
             button_frame, step_number)
    """
    try:
        # Extract step number (always the last argument)
        step_number = args[-1]
        
        # Process data based on step number
        if step_number == 1:
            entry1, entry2, scanned_data, step1_btn, step2_btn, step3_btn, button_frame, _ = args
            data = {
                **scanned_data,
                'date': entry1.get(),
                'address': entry2.get()
            }
            
        elif step_number == 2:
            (owner_entry, renter_entry, personal_code_entry, owner_sign_var, renter_sign_var,
             scanned_data, step1_btn, step2_btn, step3_btn, button_frame, _) = args
            data = {
                **scanned_data,
                'owner': owner_entry.get(),
                'renter': renter_entry.get(),
                'owner_sign': owner_sign_var.get(),
                'renter_sign': renter_sign_var.get(),
                'personal_code': personal_code_entry.get()
            }
            
        elif step_number == 3:
            owner_entry, renter_entry, code_entry, scanned_data, step1_btn, step2_btn, step3_btn, button_frame, _ = args
            data = {
                **scanned_data,
                'owner': owner_entry.get(),
                'renter': renter_entry.get(),
                'code': code_entry.get()
            }
        else:
            raise ValueError(f"Invalid step number: {step_number}")

        # Validation
        if any(value == "" for value in data.values()):
            raise ValueError("Please fill in all required fields")

        # Emit data to server
        print(f"[DEBUG] Step {step_number} completed with data: {data}")
        sio.emit('step_completed', {'step': step_number, 'data': data})
        
        # Update UI
        completion_frame.pack_forget()
        
        # Update button states
        if step_number == 1:
            step1_btn.config(state="disabled")
            step2_btn.config(state="normal")
            step3_btn.config(state="disabled")
        elif step_number == 2:
            step2_btn.config(state="disabled")
            step3_btn.config(state="normal")
        else:
            step3_btn.config(state="disabled")
        
        button_frame.pack(expand=True, fill="both")
        
    except ValueError as ve:
        print(f"Validation Error: {str(ve)}")
        # Show error message to user
        validation_label = ttk.Label(completion_frame, text=str(ve), style="Subtitle.TLabel", foreground="red")
        validation_label.pack(pady=10)
    except Exception as e:
        print(f"Error: {str(e)}")
        # Show error message to user
        validation_label = ttk.Label(completion_frame, text=f"Error: {str(e)}", style="Subtitle.TLabel", foreground="red")
        validation_label.pack(pady=10)

def show_completion_page(previous_frame, *args):
    """
    Show the completion page for a step.
    Args are passed through from the step forms and vary by step.
    """
    step_frame = ttk.Frame(previous_frame.master, style="Modern.TFrame", padding="20")
    previous_frame.pack_forget()
    step_frame.pack(expand=True, fill="both")

    title_label = ttk.Label(step_frame, text="Complete Step", style="Title.TLabel")
    title_label.pack(pady=5)

    # Create validation label
    validation_label = ttk.Label(step_frame, text="", style="Subtitle.TLabel", foreground="red")
    validation_label.pack(pady=10)

    complete_button = ModernButton(
        step_frame,
        text="Complete",
        command=lambda: handle_step_completion(step_frame, validation_label, *args),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=15
    )
    complete_button.pack(pady=20)

    back_button = ModernButton(
        step_frame,
        text="Back",
        command=lambda: back_to_form(step_frame, previous_frame),
        font=('Segoe UI', 10, 'bold'),
        fg='white',
        bg='#8B5CF6',
        activeforeground='white',
        activebackground='#7C3AED',
        relief='flat',
        cursor='hand2',
        width=15
    )
    back_button.pack(pady=10)

def handle_step_completion(step_frame, validation_label, *args):
    """
    Handle the completion of a step, including validation and data submission.
    """
    try:
        # Get step number (last argument)
        step_number = args[-1]
        
        # Process data based on step number
        if step_number == 1:
            entry1, entry2, scanned_data, step1_btn, step2_btn, step3_btn, button_frame, _ = args
            if not entry1.get() or not entry2.get():
                raise ValueError("Please fill in all fields")
            data = {
                **scanned_data,
                'date': entry1.get(),
                'address': entry2.get()
            }
            
        elif step_number == 2:
            (owner_entry, renter_entry, personal_code_entry, owner_sign_var, renter_sign_var,
             scanned_data, step1_btn, step2_btn, step3_btn, button_frame, _) = args
            if not all([owner_entry.get(), renter_entry.get(), personal_code_entry.get(),
                       owner_sign_var.get(), renter_sign_var.get()]):
                raise ValueError("Please fill in all fields")
            data = {
                **scanned_data,
                'owner': owner_entry.get(),
                'renter': renter_entry.get(),
                'owner_sign': owner_sign_var.get(),
                'renter_sign': renter_sign_var.get(),
                'personal_code': personal_code_entry.get()
            }
            
        elif step_number == 3:
            owner_entry, renter_entry, code_entry, scanned_data, step1_btn, step2_btn, step3_btn, button_frame, _ = args
            if not all([owner_entry.get(), renter_entry.get(), code_entry.get()]):
                raise ValueError("Please fill in all fields")
            data = {
                **scanned_data,
                'owner': owner_entry.get(),
                'renter': renter_entry.get(),
                'code': code_entry.get()
            }
        else:
            raise ValueError(f"Invalid step number: {step_number}")

        # Emit data to server
        print(f"[DEBUG] Step {step_number} completed with data: {data}")
        sio.emit('step_completed', {'step': step_number, 'data': data})
        
        # Update UI
        step_frame.pack_forget()
        
        # Update button states
        if step_number == 1:
            step1_btn.config(state="disabled")
            step2_btn.config(state="normal")
            step3_btn.config(state="disabled")
        elif step_number == 2:
            step2_btn.config(state="disabled")
            step3_btn.config(state="normal")
        else:
            step3_btn.config(state="disabled")
        
        button_frame.pack(expand=True, fill="both")
        
    except ValueError as ve:
        validation_label.config(text=str(ve))
        print(f"Validation Error: {str(ve)}")
    except Exception as e:
        validation_label.config(text=f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        
def back_to_form(current_frame, previous_frame):
    current_frame.pack_forget()
    previous_frame.pack(expand=True, fill="both")

def back_to_steps(current_frame, step1_button, step2_button, step3_button, button_frame):
    current_frame.pack_forget()
    button_frame.pack(expand=True, fill="both")

def complete_step(completion_frame, *args):
    if len(args) == 8:  # Step 1
        entry1, entry2, scanned_data, step1_button, step2_button, step3_button, button_frame, step_number = args
        data = {
            **scanned_data,
            'date': entry1.get(),
            'address': entry2.get()
        }
    elif len(args) == 9:  # Step 2
        owner_entry, renter_entry, scanned_data, step1_button, step2_button, step3_button, button_frame, validation_label, step_number = args
        data = {
            **scanned_data,
            'owner': owner_entry.get(),
            'renter': renter_entry.get()
        }
    else:  # Step 3
        owner_entry, renter_entry, code_entry, scanned_data, step1_button, step2_button, step3_button, button_frame, step_number = args
        data = {
            **scanned_data,
            'owner': owner_entry.get(),
            'renter': renter_entry.get(),
            'code': code_entry.get()
        }

    try:
        print(f"[DEBUG] Step {step_number} completed with data: {data}")
        sio.emit('step_completed', {'step': step_number, 'data': data})
        completion_frame.pack_forget()
        
        # Update button states
        if step_number == 1:
            step1_button.config(state="disabled")
            step2_button.config(state="normal")
            step3_button.config(state="disabled")
        elif step_number == 2:
            step2_button.config(state="disabled")
            step3_button.config(state="normal")
        else:
            step3_button.config(state="disabled")
        
        button_frame.pack(expand=True, fill="both")
    except Exception as e:
        print(f"Error: {str(e)}")
        # Show error message to user

def complete_step1(step1_frame, date_entry, address_entry, scanned_data, step1_button, step2_button, step3_button, button_frame, validation_label):
    date = date_entry.get()
    address = address_entry.get()
    
    # Validation checks
    if not date or not address:
        validation_label.config(text="Please fill in all required fields.", foreground="red")
        return
    
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

def complete_step2(step2_frame, owner_entry, renter_entry, personal_code_entry, owner_sign_var, renter_sign_var, scanned_data, step1_button, step2_button, step3_button, button_frame, validation_label):
    owner = owner_entry.get()
    renter = renter_entry.get()
    owner_sign = owner_sign_var.get()  # Assuming you have a variable for owner sign
    renter_sign = renter_sign_var.get()  # Assuming you have a variable for renter sign
    personal_code = personal_code_entry.get()  # Assuming you have an entry for personal code
    
    # Validation checks
    if not owner or not renter or not owner_sign or not renter_sign or not personal_code:
        validation_label.config(text="Please fill in all required fields.", foreground="red")
        return
    
    step2_data = {
        **scanned_data, 
        'owner': owner, 
        'renter': renter, 
        'owner_sign': owner_sign, 
        'renter_sign': renter_sign, 
        'personal_code': personal_code
    }
    
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

def complete_step3(step3_frame, owner_entry, renter_entry, code_entry, scanned_data, step1_button, step2_button, step3_button, button_frame, validation_label):
    owner = owner_entry.get()
    renter = renter_entry.get()
    code = code_entry.get()
    
    # Validation checks
    if not owner or not renter or not code:
        validation_label.config(text="Please fill in all required fields.", foreground="red")
        return
    
    step3_data = {
        **scanned_data, 
        'owner': owner, 
        'renter': renter, 
        'code': code
    }
    
    try:
        print(f"[DEBUG] Step 3 completed with data: {step3_data}")
        sio.emit('step_completed', {'step': 3, 'data': step3_data})
        step3_frame.pack_forget()
        step1_button.config(state="disabled")
        step2_button.config(state="disabled")
        step3_button.config(state="disabled")
        button_frame.pack(expand=True, fill="both")
    except Exception as e:
        print(f"Error: {str(e)}")

def create_overlay():
    global stop_scanning
    stop_scanning = False
    
    root = tk.Tk()
    root.geometry("400x300")
    root.title("QR Scanner")
    root.configure(bg="#4B0082")
    root.attributes("-alpha", 0.3)
    root.attributes("-topmost", True)

    control_panel = tk.Toplevel(root)
    control_panel.geometry("400x500")
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
    status_label.pack(pady=(0, 0))

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
        elif step_number == 3:
            step3_frame = create_step3_frame(main_frame, step1_button, step2_button, step3_button, button_frame)
            button_frame.pack_forget()
            step3_frame.pack(expand=True, fill="both")
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
        sio.connect('https://oneflow-qr.onrender.com/')
        status_var.set("Connected to server")
    except Exception as e:
        status_var.set(f"Server connection error: {str(e)}")
        print(f"Server connection error: {e}")

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
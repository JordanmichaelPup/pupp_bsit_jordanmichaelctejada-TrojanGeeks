from tkinter import *
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry, Calendar
from PIL import Image, ImageTk
import sqlite3
import webbrowser
import json
import os
from datetime import datetime

# Initialize the Tkinter root window first
window = Tk()
window.title("Polytechnic University of the Philippines Parañaque Event Tracker")
window.geometry("1600x800")
window.resizable(True, False)
window.state('zoomed')

# Load the logo image
logo_image_path = "C:/Users/Elthon Mark/OneDrive/Documents/Projects/THE PUP_PET_FINAL/Images/PUP_LOGO.ico"
logo_image = Image.open(logo_image_path)
logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Set the window icon for the main window
window.iconphoto(False, logo_photo)

# Function to select and display the profile picture
def select_profile_picture():
    file_path = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        # Resize the image to fit the main dashboard UI frame
        profile_image = Image.open(file_path).resize((50, 50), Image.Resampling.LANCZOS)
        profile_photo = ImageTk.PhotoImage(profile_image)

        # Update the profile picture label in the main dashboard
        profile_label.config(image=profile_photo)
        profile_label.image = profile_photo

def initialize_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            password TEXT NOT NULL,
            dob TEXT NOT NULL,
            profile_picture TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to check password strength
def check_password_strength(password):
    min_length = 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "@.,_?!|$%^/*+-=><}{][)(#';:" for c in password)

    if len(password) < min_length or not (has_upper and has_lower and has_digit and has_special):
        return False, "Weak Password: Must be at least 8 characters, includes: uppercase, lowercase, digit, and a special character."
    return True, "Strong Password"

# Function to save data to the database
def save_to_db(username, name, contact, password, dob):
    try:
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, name, contact, password, dob) VALUES (?, ?, ?, ?, ?)",
                       (username, name, contact, password, dob))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

# UI Functions
def show_main_menu():
    for widget in window.winfo_children():
        widget.destroy()
    setup_main_menu_ui()

def setup_main_menu_ui():
    bg_image = Image.open("C:/Users/Elthon Mark/OneDrive/Documents/Projects/THE PUP_PET_FINAL/images/ENTRANCE.jpg")
    bg_image = bg_image.resize((1600, 800), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    background_label = Label(window, image=bg_photo)
    background_label.image = bg_photo
    background_label.place(relwidth=1, relheight=1)

    # Load the transparent logo image
    logo_image = Image.open("C:/Users/Elthon Mark/OneDrive/Documents/Projects/THE PUP_PET_FINAL/images/PUP_LOGO.ico").convert("RGBA")
    logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)

    # Create a PhotoImage from the RGBA image
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = Label(window, image=logo_photo, bg="#FFFFFF", bd=0)  # Set bd=0 to eliminate the border
    logo_label.image = logo_photo
    logo_label.place(relx=0.5, rely=0.17, anchor="center")

    frame = Frame(window, bg="#FFFFFF", bd=10, relief=RIDGE)
    frame.place(relx=0.5, rely=0.65, anchor=CENTER, width=340, height=520)

    header = Label(frame, text="Create New Account", font=("Arial", 18, "bold"), bg="#FFFFFF")
    header.grid(row=0, column=0, columnspan=2, pady=10)

    create_entry_fields(frame)

    sign_up_button = Button(frame, text="Sign up", bg="red", fg="white", font=("Arial", 12, "bold"), command=sign_up)
    sign_up_button.grid(row=9, column=0, columnspan=2, pady=10)

    setup_terms_privacy_policy(frame)
    setup_login_buttons(frame)

    # Create the yellow label in the lower right corner
    yellow_label = Label(window, text="V.2.5.1", font=("Arial", 11))
    yellow_label.place(relx=1.0, rely=1.0, anchor="se")  # 'se' means south-east (lower right corner)

def validate_number(P):
    if P == "":  
        return True
    if P == "Contact number":  
        return True
    return P.isdigit()  # String lang pwede

def create_entry_fields(frame):
    fields = ["Please enter your username", "Please enter your name", "Contact number", "Please enter your password", "Date of Birth"]

    global username_entry, name_entry, contact_entry, password_entry, dob_entry, strength_label, eye_icon, eye_open_image, eye_closed_image

    # Register the validation command
    validate_cmd = frame.register(validate_number)

    username_entry = create_entry(frame, fields[0], 3)
    name_entry = create_entry(frame, fields[1], 4)
    
    # Special creation for contact entry with validation
    contact_entry = Entry(frame, width=36, fg="grey")
    contact_entry.insert(0, fields[2])
    contact_entry.bind("<FocusIn>", lambda e: on_focus_in(contact_entry, fields[2]))
    contact_entry.bind("<FocusOut>", lambda e: on_focus_out(contact_entry, fields[2]))
    contact_entry.config(validate="key", validatecommand=(validate_cmd, '%P'))
    contact_entry.grid(row=5, column=0, columnspan=2, pady=10)

    password_frame = Frame(frame, bg="#FFFFFF")
    password_frame.grid(row=6, column=0, columnspan=2, pady=10)

    password_entry = Entry(password_frame, width=31, fg="grey", show="")
    password_entry.insert(0, fields[3])
    password_entry.bind("<FocusIn>", lambda e: on_focus_in(password_entry, fields[3]))
    password_entry.bind("<FocusOut>", lambda e: on_focus_out(password_entry, fields[3]))
    password_entry.pack(side=LEFT)

    eye_open_image = ImageTk.PhotoImage(Image.open("images/Open_Eye.png").resize((20, 20), Image.Resampling.LANCZOS))
    eye_closed_image = ImageTk.PhotoImage(Image.open("images/Closed_Eye.png").resize((20, 20), Image.Resampling.LANCZOS))
    eye_icon = Button(password_frame, image=eye_closed_image, bd=0, command=toggle_password)
    eye_icon.pack(side=LEFT, padx=(5, 0))

    dob_frame = Frame(frame, bg="#FFFFFF")
    dob_frame.grid(row=7, column=0, columnspan=2, pady=10)

    dob_label = Label(dob_frame, text="Date of Birth:", font=("Arial", 10), bg="#FFFFFF", anchor="w")
    dob_label.pack(side=LEFT, padx=(0, 10))

    dob_entry = DateEntry(dob_frame, width=25, background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yyyy')
    dob_entry.pack(side=LEFT)

    strength_label = Label(frame, text="", bg="#FFFFFF", fg="red", font=("Arial", 10), justify="center", anchor="center", wraplength=325)
    strength_label.grid(row=8, column=0, columnspan=2, pady=5, sticky="nsew")

def create_entry(frame, placeholder, row):
    entry = Entry(frame, width=36, fg="grey")
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda e: on_focus_in(entry, placeholder))
    entry.bind("<FocusOut>", lambda e: on_focus_out(entry, placeholder))
    entry.grid(row=row, column=0, columnspan=2, pady=10)
    return entry

def setup_terms_privacy_policy(frame):
    terms_privacy_frame = Frame(frame, bg="#FFFFFF")
    terms_privacy_frame.grid(row=10, column=0, columnspan=2, pady=(0, 10), sticky="s")

    terms_text = Label(terms_privacy_frame, text="By clicking Sign up, you agree to the", font=("Arial", 10), bg="#FFFFFF", fg="black")
    terms_text.pack(side=TOP)

    terms_button = Button(terms_privacy_frame, text="Terms of Use", font=("Arial", 10, "underline"), fg="blue", bg="#FFFFFF", bd=0, cursor="hand2", command=lambda: webbrowser.open("https://www.pup.edu.ph/terms/"))
    terms_button.pack(side=LEFT)

    and_label = Label(terms_privacy_frame, text=" and ", font=("Arial", 10), bg="#FFFFFF", fg="black")
    and_label.pack(side=LEFT)

    privacy_button = Button(terms_privacy_frame, text="Privacy Policy", font=("Arial", 10, "underline"), fg="blue", bg="#FFFFFF", bd=0, cursor="hand2", command=lambda: webbrowser.open("https://www.pup.edu.ph/privacy/"))
    privacy_button.pack(side=RIGHT)

def setup_login_buttons(frame):
    login_text = Label(frame, text="Already Registered?", bg="#FFFFFF", fg="black", font=("Arial", 11))
    login_text.grid(row=1, column=0, padx=40, pady=5)

    login_button = Button(frame, text="Login", fg="blue", bg="#FFFFFF", bd=0, cursor="hand2", command=login_redirect, font=("Arial", 11, "underline"))
    login_button.grid(row=1, column=1, padx=30, pady=2.5)

    forgot_password_button = Button(frame, text="Forgot Password?", fg="blue", bg="#FFFFFF", bd=0, cursor="hand2", command=forgot_password, font=("Arial", 11, "underline"))
    forgot_password_button.grid(row=2, column=0, columnspan=2, pady=5)

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        eye_icon.config(image=eye_open_image)
    else:
        password_entry.config(show="*")
        eye_icon.config(image=eye_closed_image)

# Function to handle focus in event
def on_focus_in(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, END)
        entry['fg'] = "black"
        if placeholder == "Please enter your password":
            entry['show'] = "*"

# Function to handle focus out event
def on_focus_out(entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)
        entry['fg'] = "grey"
        if placeholder == "Please enter your password":
            entry['show'] = ""

def sign_up():
    # Get values and strip whitespace
    username = username_entry.get().strip()
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    password = password_entry.get().strip()
    dob = dob_entry.get_date()

    # Check for placeholder texts
    default_texts = {
        "username": "Please enter your username",
        "name": "Please enter your name",
        "contact": "Contact number",
        "password": "Please enter your password"
    }

    # Validate that fields aren't empty or still containing placeholder text
    if (username == "" or 
        name == "" or 
        contact == "" or 
        password == "" or 
        username == default_texts["username"] or 
        name == default_texts["name"] or 
        contact == default_texts["contact"] or 
        password == default_texts["password"]):
        messagebox.showwarning("Incomplete Details", "Please fill out all fields")
        return

    # Validate username
    if not username.isalnum():
        messagebox.showwarning("Invalid Username", "Username must be alphanumeric.")
        return

    # Validate name (should contain only letters and spaces)
    if not all(char.isalpha() or char.isspace() for char in name):
        messagebox.showwarning("Invalid Name", "Name should only contain letters and spaces.")
        return

    # Validate contact number
    if not contact.isdigit() or len(contact) < 11:
        messagebox.showwarning("Invalid Contact", "Contact number must be at least 11 digits.")
        return

    # Validate password strength
    is_strong, message = check_password_strength(password)
    strength_label.config(text=message, fg="red" if not is_strong else "green")

    if not is_strong:
        messagebox.showwarning("Weak Password", "Please enter a strong password before proceeding.")
        return

    # Check if username already exists
    try:
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            messagebox.showwarning("Username Taken", "This username is already registered. Please choose another.")
            conn.close()
            return
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        conn.close()
        return

    # If all validations pass, save to database
    try:
        save_to_db(username, name, contact, password, dob)
        messagebox.showinfo("Success", "Account Created Successfully! Redirecting to login page...")
        login_redirect()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create account: {str(e)}")

# Function for login redirection
def login_redirect():
    for widget in window.winfo_children():
        widget.destroy()
    setup_login_ui()

def setup_login_ui():
    bg_image = Image.open("C:/Users/Elthon Mark/OneDrive/Documents/Projects/THE PUP_PET_FINAL/images/HALLWAY.jpg")
    bg_image = bg_image.resize((1600, 800), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    background_label = Label(window, image=bg_photo)
    background_label.image = bg_photo
    background_label.place(relwidth=1, relheight=1)

    login_frame = Frame(window, bg="#FFFFFF", bd=10, relief=RIDGE)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=340, height=380)

    Label(login_frame, text="Login To Your Account", font=("Arial", 18, "bold"), bg="#FFFFFF").grid(row=0, column=0, columnspan=2, pady=10)

    Label(login_frame, text="Only valid accounts will be accepted", font=("Arial", 12), bg="#FFFFFF").grid(row=1, column=0, columnspan=2, pady=5)

    Label(login_frame, text="Username:", font=("Arial", 12), bg="#FFFFFF").grid(row=2, column=0, pady=10, padx=10)
    username_entry_login = Entry(login_frame, width=30)
    username_entry_login.grid(row=2, column=1, pady=10, padx=10)

    Label(login_frame, text="Password:", font=("Arial", 12), bg="#FFFFFF").grid(row=3, column=0, pady=10, padx=10)
    password_entry_login = Entry(login_frame, width=30, show="*")
    password_entry_login.grid(row=3, column=1, pady=10, padx=10)

    button_frame = Frame(login_frame, bg="#FFFFFF")
    button_frame.grid(row=4, column=0, columnspan=2, pady=10)

    Button(button_frame, text="Login", bg="red", fg="white", font=("Arial", 12, "bold"), command=lambda: login(username_entry_login.get(), password_entry_login.get())).grid(row=0, column=0, padx=5, pady=20)
    Button(button_frame, text="Back", bg="grey", fg="white", font=("Arial", 12, "bold"), command=show_main_menu).grid(row=0, column=1, padx=5, pady=20)

    setup_terms_privacy_policy_login(login_frame)

def setup_terms_privacy_policy_login(login_frame):
    terms_privacy_frame = Frame(login_frame, bg="#FFFFFF")
    terms_privacy_frame.grid(row=5, column=0, columnspan=2, pady=(25, 10))

    terms_text = Label(terms_privacy_frame, text="By clicking Login, you agree to the", font=("Arial", 11), bg="#FFFFFF", fg="black")
    terms_text.pack(side=TOP)

    terms_button = Button(terms_privacy_frame, text="Terms of Use", font=("Arial", 11, "underline"), fg="blue", bg="#FFFFFF", bd=0, cursor="hand2", command=lambda: webbrowser.open("https://www.pup.edu.ph/terms/"))
    terms_button.pack(side=LEFT)

    and_label = Label(terms_privacy_frame, text=" and ", font=("Arial", 11), bg="#FFFFFF", fg="black")
    and_label.pack(side=LEFT)

    privacy_button = Button(terms_privacy_frame, text="Privacy Policy", font=("Arial", 11, "underline"), fg="blue", bg="#FFFFFF", bd=0, cursor="hand2", command=lambda: webbrowser.open("https://www.pup.edu.ph/privacy/"))
    privacy_button.pack(side=RIGHT)

def login(username, password):
    if not username or not password:
        messagebox.showwarning("Incomplete Details", "Please fill out all fields")
        return

    try:
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login successful!")
            show_dashboard(username)  # Pass the username to the show_dashboard function
        else:
            messagebox.showerror("Error", "Invalid username or password")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

# Global variable to track if the forgot password window is open
forgot_password_open = False

# Function to handle forgot password
def forgot_password():
    global forgot_password_open

    if forgot_password_open:
        messagebox.showwarning("Warning", "The forgot password window is already open.")
        return

    forgot_password_open = True  # Set the flag to indicate the window is open

    def reset_password():
        username = username_entry_fp.get()
        new_password = new_password_entry_fp.get()

        if not username or not new_password:
            messagebox.showwarning("Incomplete Details", "Please fill out all fields")
            return

        is_strong, message = check_password_strength(new_password)
        strength_label_fp.config(text=message, fg="red" if not is_strong else "green")

        if not is_strong:
            messagebox.showwarning("Weak Password", "Please enter a strong password before proceeding.")
            return

        try:
            conn = sqlite3.connect("user_data.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
            if cursor.rowcount == 0:
                messagebox.showwarning("User Not Found", "No user found with the provided username.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Password reset successfully! Redirecting to login page...")
                forgot_password_window.destroy()
                login_redirect()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()
    
    # Forgot Password Window
    forgot_password_window = Toplevel(window)
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("400x300")
    forgot_password_window.resizable(False, False)

    # Set the icon for the forgot password window
    forgot_password_window.iconbitmap("C:/Users/Elthon Mark/OneDrive/Documents/Projects/THE PUP_PET_FINAL/images/PUP_LOGO.ico")

    # Bind the close event to reset the flag
    forgot_password_window.protocol("WM_DELETE_WINDOW", lambda: [forgot_password_window.destroy(), reset_forgot_password_flag()])

    forgot_frame = Frame(forgot_password_window, bg="#FFFFFF", bd=10, relief=RIDGE)
    forgot_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=380, height=280)

    Label(forgot_frame, text="Forgot Password", font=("Arial", 18, "bold"), bg="#FFFFFF").grid(row=0, column=0, columnspan=2, pady=10)

    Label(forgot_frame, text="Input your new password", font=("Arial", 12), bg="#FFFFFF").grid(row=1, column=0, columnspan=2, pady=5)

    Label(forgot_frame, text="Username:", font=("Arial", 12), bg="#FFFFFF").grid(row=2, column=0, pady=10, padx=10, sticky="e")
    username_entry_fp = Entry(forgot_frame, width=30)
    username_entry_fp.grid(row=2, column=1, pady=10, padx=10)

    Label(forgot_frame, text="New Password:", font=("Arial", 12), bg="#FFFFFF").grid(row=3, column=0, pady=10, padx=10, sticky="e")
    new_password_entry_fp = Entry(forgot_frame, width=30, show="*")
    new_password_entry_fp.grid(row=3, column=1, pady=10, padx=10)

    strength_label_fp = Label(forgot_frame, text="", fg="red", font=("Arial", 10), bg="#FFFFFF")
    strength_label_fp.grid(row=4, column=0, columnspan=2, pady=5)

    Button(forgot_frame, text="Confirm", bg="red", fg="white", font=("Arial", 12, "bold"), command=reset_password).grid(row=5, column=0, columnspan=2, padx=(0, 10), pady=(5, 5))
    Button(forgot_frame, text="Back", bg="grey", fg="white", font=("Arial", 12, "bold"), command=lambda: [forgot_password_window.destroy(), reset_forgot_password_flag()]).grid(row=5, column=1, columnspan=2, padx=(10, 10), pady=(5, 5))

    def reset_forgot_password_flag():
        global forgot_password_open
        forgot_password_open = False  # Reset the flag when the window is closed

def show_dashboard(username):
    for widget in window.winfo_children():
        widget.destroy()
    setup_dashboard_ui(username)

def setup_dashboard_ui(username):
    window.title("Polytechnic University of the Philippines Parañaque Event Tracker")
    bg_image = Image.open("C:/Users/Elthon Mark/OneDrive/Documents/Projects/THE PUP_PET_FINAL/Images/PUPP.jpg")
    bg_image = bg_image.resize((1600, 800), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    background_label = Label(window, image=bg_photo)
    background_label.image = bg_photo
    background_label.place(relwidth=1, relheight=1)

    main_frame = Frame(window, bg="#FFFFFF", bd=10, relief=RIDGE)
    main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=500, height=450)

    title_frame = Frame(main_frame, bg="#FFFFFF")
    title_frame.pack(pady=(10, 20))

    greeting_text = f"Hello! {username}"
    title_label = Label(title_frame, text=greeting_text, font=("Arial", 24, "bold"), bg="#FFFFFF")
    title_label.pack(side=LEFT, padx=(0, 10))

    global profile_label
    profile_label = Label(title_frame, bg="#FFFFFF")
    profile_label.pack(side=LEFT)

    # Frame for menu buttons
    menu_frame = Frame(main_frame, bg="#FFFFFF")
    menu_frame.pack(pady=10)

    Button(menu_frame, text="What's New?", command=lambda: display_events_by_status("upcoming"), padx=10, pady=10).pack(side=LEFT, padx=5)
    Button(menu_frame, text="Refresh", command=refresh_events, padx=10, pady=10).pack(side=LEFT, padx=5)  # Add Refresh button
    Button(menu_frame, text="Date Today", command=show_calendar, padx=10, pady=10).pack(side=LEFT, padx=5)
    Button(menu_frame, text="Settings", command=show_settings, padx=10, pady=10).pack(side=LEFT, padx=5)
    Button(menu_frame, text="Add Event", command=show_add_event_form, padx=10, pady=10).pack(side=LEFT, padx=5)

    # Event boxes
    event_frame = Frame(main_frame, bg="#FFFFFF")
    event_frame.pack(pady=(20, 10))

    def create_event_box(text, status):
        box = Label(event_frame, text=text, bg=COLORS[status], fg="white", font=("Arial", 16, "bold"), padx=20, pady=20)
        box.pack(side=TOP, fill=X, padx=10, pady=5)
        box.bind("<Button-1>", lambda e: display_events_by_status(status))

    create_event_box("Upcoming Events", "upcoming")
    create_event_box("Ongoing Events", "ongoing")
    create_event_box("Ended Events", "ended")

    # Status bar
    status_label = Label(window, text="V.2.5.1", font=("Arial", 11), bg="#FFFFFF")
    status_label.place(relx=1.0, rely=1.0, anchor="se")

def refresh_events():
    events = read_json()
    current_date = datetime.now().date()

    for event in events:
        event_date = datetime.strptime(event['date'], "%m/%d/%Y").date()
        if event_date == current_date:
            event['status'] = "ongoing"
        elif event_date < current_date:
            event['status'] = "ended"
        else:
            event['status'] = "upcoming"

    # Sort events by date
    events.sort(key=lambda x: datetime.strptime(x['date'], "%m/%d/%Y"))

    write_json(events)
    messagebox.showinfo("Refreshed", "Events have been refreshed and sorted by date.")
    display_events_by_status("upcoming")

# Global variable to keep track of the currently open edit window
current_edit_window = None

# Function to display events by status (upcoming, ongoing, ended) with delete button
def display_events_by_status(status):
    if status in open_windows:
        open_windows[status].destroy()

    new_window = Toplevel(window)
    new_window.title(f"{status.capitalize()} Events")
    new_window.geometry("400x300")

    # Set the position of the window based on the status
    if status == "upcoming":
        new_window.geometry("+90+90")  # Upper left corner
    elif status == "ongoing":
        new_window.geometry("+90+440")  # Lower left corner
    elif status == "ended":
        new_window.geometry("+1025+380")  # Lower right corner
    new_window.resizable(False, False)  # Disable the maximize button

    open_windows[status] = new_window  # Track the open window

    new_window.iconphoto(False, logo_photo)  # Set the icon for new windows

    events = read_json()
    filtered_events = [event for event in events if event['status'] == status]

    # Sort filtered events by date
    filtered_events.sort(key=lambda x: datetime.strptime(x['date'], "%m/%d/%Y"), reverse=(status == "ended"))

    scrollable_frame = Frame(new_window)
    scrollable_frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(scrollable_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar_y = Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview, width=20)
    scrollbar_y.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar_y.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    event_frame = Frame(canvas)
    canvas.create_window((0, 0), window=event_frame, anchor="nw")

    if filtered_events:
        for event in filtered_events:
            event_info = (f"Name: {event['name']}\n"
                          f"Date: {event['date']}\n"
                          f"Location: {event['location']}\n"
                          f"Description: {event['description']}\n"
                          f"Tags: {event['tags']}\n\n")

            # Use Text widget to allow text wrapping with Arial font
            event_text = Text(event_frame, wrap=WORD, padx=10, pady=10, font=("Arial", 9), width=50, height=15)  # Fixed height for Text widget
            event_text.insert(END, event_info)

            # Define bold tags
            event_text.tag_configure("bold", font=("Arial", 9, "bold"))

            # Apply bold tags to titles
            event_text.tag_add("bold", "1.0", "1.4")  # Name
            event_text.tag_add("bold", "2.0", "2.4")  # Date
            event_text.tag_add("bold", "3.0", "3.8")  # Location
            event_text.tag_add("bold", "4.0", "4.11")  # Description
            event_text.tag_add("bold", "5.0", "5.4")  # Tags

            event_text.config(state=DISABLED)  # Make the text widget read-only
            event_text.pack(fill=BOTH, expand=True)

            button_frame = Frame(event_frame)
            button_frame.pack(pady=5)

            edit_button = Button(button_frame, text="Edit", command=lambda e=event: edit_event(e, new_window), bg="blue", fg="white", padx=10, pady=5)
            edit_button.pack(side=LEFT, padx=5)

            delete_button = Button(button_frame, text="Delete", command=lambda e=event: delete_event(e, new_window), bg="red", fg="white", padx=10, pady=5)
            delete_button.pack(side=LEFT, padx=5)
    else:
        event_label = Label(event_frame, text="No events available.", padx=10, pady=10, font=("Arial", 12))
        event_label.pack(fill=BOTH, expand=True)

    # Update the scrollregion after adding widgets
    event_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def edit_event(event, parent_window):
    global current_edit_window
    
    # Close the current edit window if it exists
    if current_edit_window is not None:
        current_edit_window.destroy()

    edit_window = Toplevel(parent_window)
    edit_window.title("Edit Event")
    edit_window.geometry("350x250+585+325")
    edit_window.resizable(False, False)

    edit_window.iconphoto(False, logo_photo)

    labels = ["Event Name:", "Date (MM/DD/YYYY):", "Location:", "Description:", "Tags:"]
    entries = []

    # Pre-fill entries with current event information
    values = [event['name'], event['date'], event['location'], event['description'], event['tags']]

    for i, (label, value) in enumerate(zip(labels, values)):
        Label(edit_window, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=5)
        entry = Entry(edit_window, width=30)
        entry.insert(0, value)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def save_edits():
        name, date_str, location, description, tags = [entry.get() for entry in entries]

        try:
            event_date = datetime.strptime(date_str, "%m/%d/%Y")
            current_date = datetime.now()
            current_date_only = current_date.date()

            if event_date.date() == current_date_only:
                status = "ongoing"
            elif event_date < current_date:
                status = "ended"
            else:
                status = "upcoming"
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in MM/DD/YYYY format.")
            return

        events = read_json()
        for e in events:
            if e['id'] == event['id']:
                e['name'] = name
                e['date'] = date_str
                e['location'] = location
                e['description'] = description
                e['tags'] = tags
                e['status'] = status
                break
        write_json(events)
        edit_window.destroy()
        parent_window.destroy()
        display_events_by_status(status)

    def go_back():
        edit_window.destroy()

    save_button = Button(edit_window, text="Save", command=save_edits, bg="red", fg="white", padx=20, pady=10, font=("Arial", 10))
    save_button.grid(row=len(labels), column=0, pady=20, padx=(10, 5), sticky='e')

    back_button = Button(edit_window, text="Back", command=go_back, bg="gray", fg="white", padx=20, pady=10, font=("Arial", 10))
    back_button.grid(row=len(labels), column=1, pady=20, padx=(5, 10), sticky='w')

    # Update the global variable to the current edit window
    current_edit_window = edit_window
    
# Function to delete an event
def delete_event(event, window):
    events = read_json()
    events = [e for e in events if e['id'] != event['id']]
    write_json(events)
    window.destroy()
    display_events_by_status(event['status'])

# Function to show today's date
def show_calendar():
    if 'calendar' in open_windows:
        open_windows['calendar'].destroy()

    new_window = Toplevel(window)
    new_window.title("Date Today")
    new_window.geometry("400x300")
    new_window.resizable(False, False)  # Disable the maximize button

    open_windows['calendar'] = new_window  # Track the open window

    new_window.iconphoto(False, logo_photo)  # Set the icon for new windows

    calendar = Calendar(new_window, background='maroon', foreground='white', selectbackground='darkred')
    calendar.pack(expand=True, fill='both')

def logout():
    for widget in window.winfo_children():
        widget.destroy()
    show_main_menu()

def show_settings():
    if 'settings' in open_windows:
        open_windows['settings'].destroy()

    new_window = Toplevel(window)
    new_window.title("Settings")
    new_window.geometry("300x230+1075+100")  # Upper right corner on a 1600x800 screen
    new_window.resizable(False, False)  # Disable the maximize button

    open_windows['settings'] = new_window  # Track the open window

    new_window.iconphoto(False, logo_photo)  # Set the icon for new windows

    settings_options = [
        ("Terms of Use", "https://www.pup.edu.ph/terms/"),
        ("Privacy and Policy", "https://www.pup.edu.ph/privacy/"),
        ("Change Profile Picture", select_profile_picture),
        ("Logout", logout)
    ]
    
    button_width = 20  # Set a fixed width for all buttons
    
    for text, info in settings_options:
        if text in ["Terms of Use", "Privacy and Policy"]:
            button = Button(new_window, text=text, width=button_width, padx=10, pady=10, command=lambda url=info: webbrowser.open(url))
        else:
            button = Button(new_window, text=text, width=button_width, padx=10, pady=10, command=info)
        button.pack(pady=5)

open_windows = {}

# Function to show the form to add a new event
def show_add_event_form():
    if 'add_event' in open_windows:
        open_windows['add_event'].destroy()

    form = Toplevel(window)
    form.title("Add Event")
    form.geometry("350x250+585+325")  # Center the window on a 1600x800 screen
    form.resizable(False, False)  # Disable the maximize button

    open_windows['add_event'] = form  # Track the open window

    form.iconphoto(False, logo_photo)  # Set the icon for new windows

    labels = ["Event Name:", "Date (MM/DD/YYYY):", "Location:", "Description:", "Tags:"]
    entries = []

    for i, label in enumerate(labels):
        Label(form, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=5)
        entry = Entry(form, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def save_event():
        name, date_str, location, description, tags = [entry.get() for entry in entries]

        try:
            event_date = datetime.strptime(date_str, "%m/%d/%Y")
            current_date = datetime.now()
            current_date_only = current_date.date()

            if event_date.date() == current_date_only:
                status = "ongoing"
            elif event_date < current_date:
                status = "ended"
            else:
                status = "upcoming"
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in MM/DD/YYYY format.")
            return

        events = read_json()
        event_id = max((event['id'] for event in events), default=0) + 1
        new_event = {
            'id': event_id,
            'name': name,
            'date': date_str,
            'location': location,
            'description': description,
            'tags': tags,
            'status': status
        }
        events.append(new_event)
        write_json(events)
        form.destroy()
        display_events_by_status("upcoming")

    def go_back():
        form.destroy()

    save_button = Button(form, text="Save", command=save_event, bg="red", fg="white", padx=20, pady=10, font=("Arial", 10))
    save_button.grid(row=len(labels), column=0, pady=20, padx=(10, 5), sticky='e')

    back_button = Button(form, text="Back", command=go_back, bg="gray", fg="white", padx=20, pady=10, font=("Arial", 10))
    back_button.grid(row=len(labels), column=1, pady=20, padx=(5, 10), sticky='w')

# Function to read events from JSON file
def read_json():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# Function to write events to JSON file
def write_json(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Constants
JSON_FILE = 'users.json'
BACKGROUND_IMAGE_PATH = "c:/Users/Elthon Mark/OneDrive/Documents/Projects/THE PUP_PET/Images/PUPP.jpg"
WINDOW_SIZE = "800x600"
COLORS = {
    'upcoming': "#4caf50",
    'ongoing': "#2196f3",
    'ended': "#f44336",
}

# Initialize the database and UI
initialize_db()
# Show main menu initially
show_main_menu()

window.mainloop()
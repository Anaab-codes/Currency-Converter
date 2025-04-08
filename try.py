import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageSequence
import random
from tkinter import messagebox

# ---------------------------
# UI Components
# ---------------------------
app = ctk.CTk()
app.title("Real-Time Currency Converter")
app.geometry("800x500")
app.resizable(True, True)
app.configure(bg="#FCFBFB")

# App Icon
# icon = ctk.CTkImage(light_image=Image.open("images/currency_converter_icon.png"), size=(32, 32))
# icon_label = ctk.CTkLabel(app, image=icon, text="")

# # # Load the background image
bg_image = ctk.CTkImage(light_image=Image.open("images/background_icon.jpg"), 
                        dark_image=Image.open("images/background_icon.jpg"), 
                        size=(800, 500))

# # Create a label to hold the background image
bg_label = ctk.CTkLabel(app, image=bg_image, text="")  
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover full window

# # Add other widgets on top of the background
# label = ctk.CTkLabel(app, text="Welcome!", font=("Arial", 24))
# label.place(relx=0.5, rely=0.3, anchor="center")

# button = ctk.CTkButton(app, text="Click Me")
# button.place(relx=0.5, rely=0.5, anchor="center")

# Create Canvas for Background Animation
# canvas = tk.Canvas(app, width=700, height=400, bg="#F4F4F4", highlightthickness=0)
# canvas.pack(fill="both", expand=True)

# # List of Currency Symbols
# currency_symbols = ["$", "€", "¥", "£", "₿", "₹", "₩", "₦"]

# # Store floating items with direction values
# floating_icons = []

# for _ in range(25):  # Number of icons
#     x = random.randint(50, 650)
#     y = random.randint(50, 350)
#     size = random.randint(25, 50)
#     color = random.choice(["#FFD700", "#C0C0C0", "#DAA520"])  # Expensive colors
    
#     symbol = random.choice(currency_symbols)
#     text_id = canvas.create_text(x, y, text=symbol, font=("Arial", size, "bold"), fill=color)
    
#     dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
#     dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
    
#     floating_icons.append({"id": text_id, "dx": dx, "dy": dy})

# # Animate Floating Icons
# def animate_icons():
#     for icon in floating_icons:
#         text_id = icon["id"]
#         dx = icon["dx"]
#         dy = icon["dy"]
        
#         canvas.move(text_id, dx, dy)
#         x, y = canvas.coords(text_id)

#         # Bounce horizontally
#         if x < 0 or x > 700:
#             icon["dx"] *= -1
#         # Bounce vertically
#         if y < 0 or y > 400:
#             icon["dy"] *= -1

#     app.after(30, animate_icons)  # Persistent animation loop

# animate_icons()

# ---------------------------
# Load Custom Data from JSON file
# ---------------------------
with open('custom_rates.json', 'r') as f:  # Load the JSON data
    custom_rates_data = json.load(f)

# ------------------------------------
# API Configuration (unchanged aside from removing refresh)
# ------------------------------------
load_dotenv()
API_KEY = os.getenv("API_KEY1")
BASE_URL = "https://api.currencyapi.com/v3/latest"
# flag_base_url ="https://flagsapi.com/:country_code/:style/:size.png"

# Fetch available currencies dynamically
def get_available_currencies():
    try:
        response = requests.get(f"{BASE_URL}?apikey={API_KEY}")
        response.raise_for_status()
        data = response.json()

        if "data" not in data:
            messagebox.showerror("API Error", "Failed to fetch currency list.\nInvalid response format.")
            return []

        return list(data["data"].keys())  # Extract currency codes like 'USD', 'EUR', etc.

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to fetch currency list.\nError: {e}")
        return []

def get_exchange_rates():
    try:
        response = requests.get(f"{BASE_URL}?apikey={API_KEY}")
        response.raise_for_status()
        data = response.json()
        return data["data"]  # Contains the currency rates
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to fetch exchange rates.\nError: {e}")
        return None





# ---------------------------
# Global variable for Data Source
# ---------------------------
use_custom_data = False

# ---------------------------
# Currency List
# ---------------------------
currency_list = get_available_currencies()


# ---------------------------
# Conversion History
# ---------------------------
history_file = "history.json"
def load_history():
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is corrupted
    return []

def save_history():
    with open(history_file, "w") as file:
        json.dump(conversion_history, file, indent=4)

conversion_history = load_history()

# ---------------------------
# Global variable to track last-focused entry
# ---------------------------
last_focused = None

def on_focus_in_initial(event):
    global last_focused
    last_focused = "initial"

def on_focus_in_target(event):
    global last_focused
    last_focused = "target"

# ---------- ANIMATION SETUP ----------
# Create frame label but hide it initially
frame_label = tk.Label(app, bg="#F4F4F4")
frame_label.pack(expand=True)
frame_label.place(x=0, y=70)
frame_label.lower()  # Hide below all widgets

# Load animated GIF (transparent spinning coin)
gif_path = "images/bitcoin_spinner.gif"
gif = Image.open(gif_path)
# Resize to your preferred dimensions (e.g., 100x100)
new_size = (200,200)

frames = [
    ImageTk.PhotoImage(frame.copy().convert("RGBA").resize(new_size, Image.Resampling.LANCZOS))
    for frame in ImageSequence.Iterator(gif)
]
frame_index = 0

# Animation loop
def update_gif():
    global frame_index
    if frame_label.winfo_ismapped():
        frame_label.configure(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        app.after(100, update_gif)



def convert(event=None, store_history=False):
    try:
        # Disable the convert button
        convert_button.configure(state="disabled")

        # Show animation
        frame_label.lift()
        frame_label.place(relx=0.5, rely=0.5, anchor="center")
        update_gif()

        def process_conversion():
            try:
                initial_currency = initial_currency_var.get()
                target_currency = target_currency_var.get()
                if not initial_currency or not target_currency:
                    messagebox.showerror("Selection Error", "Please select both currencies.")
                    return
                if initial_currency == target_currency:
                    messagebox.showwarning("Invalid Selection", "Currencies cannot be the same!")
                    return

                rates = custom_rates_data["data"] if use_custom_data else get_exchange_rates()
                if rates is None or initial_currency not in rates or target_currency not in rates:
                    messagebox.showerror("Data Error", "One of the selected currencies is not available in the current data.")
                    return

                initial_rate = rates[initial_currency]["value"]
                target_rate = rates[target_currency]["value"]

                initial_val = initial_amount_entry.get().strip()
                target_val = target_amount_entry.get().strip()

                if last_focused == "initial" or (initial_val and not target_val):
                    if not initial_val:
                        messagebox.showerror("Input Error", "Please enter a value in the initial amount field.")
                        return
                    amount = float(initial_val)
                    converted = amount * (target_rate / initial_rate)
                    target_amount_entry.delete(0, tk.END)
                    target_amount_entry.insert(0, f"{converted:.2f}")
                elif last_focused == "target" or (target_val and not initial_val):
                    if not target_val:
                        messagebox.showerror("Input Error", "Please enter a value in the target amount field.")
                        return
                    amount = float(target_val)
                    converted = amount * (initial_rate / target_rate)
                    initial_amount_entry.delete(0, tk.END)
                    initial_amount_entry.insert(0, f"{converted:.2f}")
                elif initial_val and target_val:
                    if last_focused == "initial":
                        amount = float(initial_val)
                        converted = amount * (target_rate / initial_rate)
                        target_amount_entry.delete(0, tk.END)
                        target_amount_entry.insert(0, f"{converted:.2f}")
                    elif last_focused == "target":
                        amount = float(target_val)
                        converted = amount * (initial_rate / target_rate)
                        initial_amount_entry.delete(0, tk.END)
                        initial_amount_entry.insert(0, f"{converted:.2f}")
                    else:
                        amount = float(initial_val)
                        converted = amount * (target_rate / initial_rate)
                        target_amount_entry.delete(0, tk.END)
                        target_amount_entry.insert(0, f"{converted:.2f}")
                else:
                    messagebox.showerror("Input Error", "Please enter a value in one of the amount fields.")
                    return

                if store_history:
                    amount = float(initial_amount_entry.get().strip() or 0)
                    converted = amount * (target_rate / initial_rate)
                    conversion_history.append({
                        "amount": amount,
                        "initial_currency": initial_currency,
                        "target_currency": target_currency,
                        "converted_amount": round(converted, 2),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_history()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numerical amount.")
            finally:
                # Hide animation and re-enable the button
                frame_label.lower()
                convert_button.configure(state="normal")

        # Simulate delay before processing
        app.after(200, process_conversion)

    except Exception as e:
        messagebox.showerror("Unexpected Error", str(e))
        frame_label.lower()
        convert_button.configure(state="normal")



# ---------------------------
# Conversion Function
# ---------------------------
# def convert(event=None, store_history=False):
#     try:
#         # Get selected currencies
#         initial_currency = initial_currency_var.get()
#         target_currency = target_currency_var.get()
#         if not initial_currency or not target_currency:
#             messagebox.showerror("Selection Error", "Please select both currencies.")
#             return
#         if initial_currency == target_currency:
#             messagebox.showwarning("Invalid Selection", "Currencies cannot be the same!")
#             return

#         # Choose the rates data source
#         rates = custom_rates_data["data"] if use_custom_data else get_exchange_rates()
#         if rates is None or initial_currency not in rates or target_currency not in rates:
#             messagebox.showerror("Data Error", "One of the selected currencies is not available in the current data.")
#             return

#         initial_rate = rates[initial_currency]["value"]
#         target_rate = rates[target_currency]["value"]

#         # If the conversion is triggered by the button press (no event provided)
#         if event is None:
#             # Determine which field to use as source.
#             # If one is empty, use the other.
#             initial_val = initial_amount_entry.get().strip()
#             target_val = target_amount_entry.get().strip()

#             if last_focused == "initial" or (initial_val and not target_val):
#                 if not initial_val:
#                     messagebox.showerror("Input Error", "Please enter a value in the initial amount field.")
#                     return
#                 amount = float(initial_val)
#                 converted = amount * (target_rate / initial_rate)
#                 target_amount_entry.delete(0, tk.END)
#                 target_amount_entry.insert(0, f"{converted:.2f}")
#             elif last_focused == "target" or (target_val and not initial_val):
#                 if not target_val:
#                     messagebox.showerror("Input Error", "Please enter a value in the target amount field.")
#                     return
#                 amount = float(target_val)
#                 converted = amount * (initial_rate / target_rate)
#                 initial_amount_entry.delete(0, tk.END)
#                 initial_amount_entry.insert(0, f"{converted:.2f}")
                
#             # If both fields have values, default to converting from the last-focused field
#             elif initial_val and target_val:
#                 if last_focused == "initial":
#                     amount = float(initial_val)
#                     converted = amount * (target_rate / initial_rate)
#                     target_amount_entry.delete(0, tk.END)
#                     target_amount_entry.insert(0, f"{converted:.2f}")
#                 elif last_focused == "target":
#                     amount = float(target_val)
#                     converted = amount * (initial_rate / target_rate)
#                     initial_amount_entry.delete(0, tk.END)
#                     initial_amount_entry.insert(0, f"{converted:.2f}")
#                 else:
#                     # Default to initial to target if last_focused is somehow not set
#                     amount = float(initial_val)
#                     converted = amount * (target_rate / initial_rate)
#                     target_amount_entry.delete(0, tk.END)
#                     target_amount_entry.insert(0, f"{converted:.2f}")
#             else:
#                 messagebox.showerror("Input Error", "Please enter a value in one of the amount fields.")
#                 return

#             # Optionally, store the conversion history using the initial field’s amount
#             if store_history:
#                 # Use the initial amount entry as the source for history (could adjust as needed)
#                 amount = float(initial_amount_entry.get().strip() or 0)
#                 converted = amount * (target_rate / initial_rate)
#                 conversion_history.append({
#                     "amount": amount,
#                     "initial_currency": initial_currency,
#                     "target_currency": target_currency,
#                     "converted_amount": round(converted, 2),
#                     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 })
#                 save_history()

#     except ValueError:
#         messagebox.showerror("Input Error", "Please enter a valid numerical amount.")

# ---------------------------
# Toggle Data Source Functionality
# ---------------------------
def toggle_data_source():
    global use_custom_data
    use_custom_data = not use_custom_data

# Function to filter and auto-expand the dropdown
def update_dropdown(event, combobox, currency_var):
    search_term = currency_var.get().upper()
    filtered_currencies = [c for c in currency_list if c.startswith(search_term)]  # Filter list

    if filtered_currencies:
        combobox["values"] = filtered_currencies  # Update dropdown with filtered values
        combobox.event_generate("<Down>")  # Force dropdown to expand
    else:
        combobox["values"] = currency_list  # Reset if no match

# Styling function to match CustomTkinter look
def style_combobox(combobox):
    combobox.option_add("*TCombobox*Listbox.font", ("Arial", 16))
    combobox.option_add("*TCombobox*Listbox.background", "#2C2F33")  # Dark background
    combobox.option_add("*TCombobox*Listbox.foreground", "white")  # White text



# Function to filter and update dropdown
# def update_dropdown(event, combobox, currency_var):
#     search_term = currency_var.get().upper()
#     filtered_currencies = [c for c in currency_list if c.startswith(search_term)]
#     if filtered_currencies:
#         combobox.configure(values=filtered_currencies)
#         combobox.set(search_term)
#         combobox.master.update_idletasks()
#         combobox.event_generate("<FocusIn>")
#     else:
#         combobox.configure(values=currency_list)

# ---------------------------
# History Functionality (unchanged)
# ---------------------------
history_window = None

def show_history():
    global history_window, history_text

    if history_window and history_window.winfo_exists():
        history_window.lift()
        return

    history_window = tk.Toplevel(app)
    history_window.title("Conversion History")
    history_window.geometry("550x450")  

    history_label = tk.Label(history_window, text="Conversion History", font=("Arial", 14, "bold"))
    history_label.pack(pady=10)

    history_text = tk.Text(history_window, wrap="none", height=18, width=70, font=("Courier", 10))
    history_text.pack(pady=5, padx=10)
    
    scrollbar = tk.Scrollbar(history_window, command=history_text.yview)
    scrollbar.pack(side="right", fill="y")
    history_text.configure(yscrollcommand=scrollbar.set)

    if not conversion_history:
        history_text.insert("end", "No conversions have been made yet.\n")
    else:
        history_text.insert("end", f"{'Amount':<10} {'From':<6} {'To':<6} {'Converted':<12} {'Timestamp':<20}\n")
        history_text.insert("end", "-" * 60 + "\n")
        for entry in conversion_history:
            history_text.insert("end", 
                f"{str(entry['amount']):<10} {entry['initial_currency']:<6} {entry['target_currency']:<6} "
                f"{str(entry['converted_amount']):<12} {entry['timestamp']:<20}\n"
            )
    history_text.configure(state="disabled")

    
    icon = ctk.CTkImage(light_image=Image.open("images/delete_icon.png"), size=(20, 20))
    
    # Create a CustomTkinter button
    clear_button = ctk.CTkButton(history_window, text="Clear History", command=clear_history, fg_color="red",image=icon, compound="left")
    clear_button.pack(pady=12)
        
    # clear_button = tk.Button(history_window, text="Clear History", command=clear_history, bg="red")
    # clear_button.pack(pady=12)
    
    
    # # Load the image (ensure the image is in the same directory or provide full path)
    # clear_img = tk.PhotoImage(file="delete_icon.png")  # Replace with your image path

    # # Create a button with an image
    # clear_button = tk.Button(root, text="Clear History", image=clear_img, compound="left",
    #                      command=clear_history, bg="red", fg="white", font=("Arial", 12))
    # clear_button.pack(pady=12)
    

def clear_history():
    global conversion_history, history_text  # Declare conversion_history as global

    # Show confirmation dialog
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to clear all history?")

    if confirm:  # If the user clicks "Yes"
        # Clear in-memory history
        conversion_history.clear()

        # Overwrite JSON file with an empty list
        with open("history.json", "w") as file:
            json.dump(conversion_history, file, indent=4)

        # Clear the history text widget in UI
        if history_window and history_window.winfo_exists():
            history_text.configure(state="normal")  # Allow editing
            history_text.delete("1.0", tk.END)   # Remove all content
            history_text.insert("end", "History cleared.\n")  # Confirmation message
            history_text.configure(state="disabled")  # Make read-only again

        messagebox.showinfo("History Cleared", "Conversion history has been cleared.")
    else:
        # User clicked "No", so do nothing and show a message
        messagebox.showinfo("Action Canceled", "Conversion history was not cleared.")
        
        
    
# ---------------------------
# History Button Setup
# ---------------------------
icon = ctk.CTkImage(light_image=Image.open("images/history_icon.png"), size=(20, 20))
history_button = ctk.CTkButton(app, text="History", command=show_history, fg_color="#FCFBFB",
                               hover_color="darkblue", text_color="black", image=icon, compound="left")
history_button.place(x=0, y=10)

# ---------------------------
# UI Elements
# ---------------------------
initial_currency_var = ctk.StringVar(value="USD")
target_currency_var = ctk.StringVar(value="EUR")

# Initial Currency ComboBox
initial_currency_menu = ttk.Combobox(app, textvariable=initial_currency_var, font=("Arial", 20), width=15, height=10)
initial_currency_menu["values"] = currency_list
initial_currency_menu.place(x=40, y=120)
initial_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, initial_currency_menu, initial_currency_var))

# Entry under Initial Currency (removed KeyRelease conversion)
initial_amount_entry = ctk.CTkEntry(app, width=260, height=60, font=("Arial", 20))
initial_amount_entry.place(x=30, y=210)
initial_amount_entry.bind("<FocusIn>", on_focus_in_initial)

# Target Currency ComboBox
target_currency_menu = ttk.Combobox(app, textvariable=target_currency_var, font=("Arial", 20), width=15, height=10)
target_currency_menu["values"] = currency_list
target_currency_menu.place(x=400, y=120)
target_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, target_currency_menu, target_currency_var))


# Entry under Target Currency (removed KeyRelease conversion)
target_amount_entry = ctk.CTkEntry(app, width=260, height=60, font=("Times New Roman", 20))
target_amount_entry.place(x=390, y=210)
target_amount_entry.bind("<FocusIn>", on_focus_in_target)


icon = ctk.CTkImage(light_image=Image.open("images/arrow_icon.png"), size=(45, 45))

# Convert Button calls convert() when pressed
convert_button = ctk.CTkButton(app, text="", fg_color="#FCFBFB", width = 70,command=lambda: convert(store_history=True), image=icon)
convert_button.place(x=305, y=160)

# Apply styling
style_combobox(app)



app.mainloop()







# # Initialize the CustomTkinter app
# ctk.set_appearance_mode("dark")  # You can use "light" or "system" mode
# app = ctk.CTk()
# app.geometry("800x500")  # Set window size

# # Load the background image
# bg_image = ctk.CTkImage(light_image=Image.open("background.jpg"), 
#                         dark_image=Image.open("background.jpg"), 
#                         size=(800, 500))

# # Create a label to hold the background image
# bg_label = ctk.CTkLabel(app, image=bg_image, text="")  
# bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover full window

# # Add other widgets on top of the background
# label = ctk.CTkLabel(app, text="Welcome!", font=("Arial", 24))
# label.place(relx=0.5, rely=0.3, anchor="center")

# button = ctk.CTkButton(app, text="Click Me")
# button.place(relx=0.5, rely=0.5, anchor="center")

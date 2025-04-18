import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from tkinter import PhotoImage
from PIL import Image
from tkinter import messagebox



# ---------------------------
# UI Components
# ---------------------------
app = ctk.CTk()
app.title("Real-Time Currency Converter")
app.geometry("650x400")
app.resizable(True, True)
app.config(bg="#FCFBFB")


#ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"

# App Icon
#Load image with CTkImage #(supports PNG, JPG, etc.)
icon = ctk.CTkImage(light_image=Image.open("images/currency_icon.png"), size= (20, 20))


#<img src="https://flagsapi.com/{}/:style/:size.png">


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
flag_base_url ="https://flagsapi.com/:country_code/:style/:size.png"



# Fetch available currencies dynamically
def get_available_currencies():
    try:
        response = requests.get(f"{BASE_URL}?apikey={API_KEY}")
        response.raise_for_status()
        data = response.json()
        return list(data["data"].keys())  # Extract currency codes
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to fetch currency list.\nError: {e}")
        return []

def get_exchange_rates():
    try:
        response = requests.get(f"{BASE_URL}?apikey={API_KEY}")
        response.raise_for_status()
        data = response.json()
        cached_rates = data["data"]
        return cached_rates
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to fetch exchange rates.\nError: {e}")
        return None

# ---------------------------
# Global variable for Data Source
# ---------------------------
# If True, use the custom data; if False, use API data.
use_custom_data = True


# ---------------------------
# Currency List
# ---------------------------
# Dynamically fetch the currency list
currency_list = get_available_currencies()


# List to store conversion history
#conversion_history = []


# JSON file to store conversion history
history_file = "history.json"

# Function to load history from JSON file
def load_history():
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is corrupted
    return []



# Function to save history to JSON file
def save_history():
    with open(history_file, "w") as file:
        json.dump(conversion_history, file, indent=4)

# Load existing history
conversion_history = load_history()


# ---------------------------
# Conversion Function
# ---------------------------
def convert_amount(event=None):
    try:
        amount = float(initial_amount_entry.get()) if initial_amount_entry.get().strip() else 0
        initial_currency = initial_currency_var.get()
        target_currency = target_currency_var.get()
        
        if not initial_currency or not target_currency:
            messagebox.showerror("Selection Error", "Please select both currencies.")
            return
        if initial_currency == target_currency:
            messagebox.showwarning("Invalid Selection", "Currencies cannot be the same!")
            return

        # Choose data source based on toggle
        # Choose data source based on toggle
        rates = custom_rates_data["data"] if use_custom_data else get_exchange_rates()
        # if use_custom_data:
        #     rates = custom_rates_data["data"]
        # else:
        #     rates = get_exchange_rates()
        #     if rates is None:
        #         return
        
        if initial_currency not in rates or target_currency not in rates:
            messagebox.showerror("Data Error", "One of the selected currencies is not available in the current data.")
            return
        
        # Conversion: (amount) * (target_rate / initial_rate)
        initial_rate = rates[initial_currency]["value"]
        target_rate = rates[target_currency]["value"]
        conversion_factor = target_rate / initial_rate
        converted_amount = amount * conversion_factor
        
        result_text = f"{amount} {initial_currency} = {converted_amount:.2f} {target_currency}"
        # converted_amount_label.configure(text=result_text)
        
        # Update the target amount entry
        target_amount_entry.delete(0, tk.END)
        target_amount_entry.insert(0, f"{converted_amount:.2f}")
        
        # Store conversion in history
        conversion_history.append({
            "amount": amount,
            "initial_currency": initial_currency,
            "target_currency": target_currency,
            "converted_amount": round(converted_amount, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
            
        })
        save_history()
        
    
    except ValueError:
        print(ValueError)
        messagebox.showerror("Input Error", "Please enter a valid numerical amount.")
        
def reverse_convert_amount(event=None):
    try:
        amount = float(initial_amount_entry.get()) if initial_amount_entry.get().strip() else 0

        amount = float(target_amount_entry.get()) if target_amount_entry.get().strip() else 0
        initial_currency = initial_currency_var.get()
        target_currency = target_currency_var.get()
        
        if not initial_currency or not target_currency:
            messagebox.showerror("Selection Error", "Please select both currencies.")
            return
        if initial_currency == target_currency:
            messagebox.showwarning("Invalid Selection", "Currencies cannot be the same!")
            return

        # if not initial_currency or not target_currency:
        #     return

        rates = custom_rates_data["data"] if use_custom_data else get_exchange_rates()
        
        if initial_currency not in rates or target_currency not in rates:
            messagebox.showerror("Data Error", "One of the selected currencies is not available in the current data.")
            return
        
        # if rates is None or initial_currency not in rates or target_currency not in rates:
        #     return

        # Reverse conversion
        initial_rate = rates[initial_currency]["value"]
        target_rate = rates[target_currency]["value"]
        converted_amount = amount * (initial_rate / target_rate)

        # Update the initial amount entry
        initial_amount_entry.delete(0, tk.END)
        initial_amount_entry.insert(0, f"{converted_amount:.2f}")

    except ValueError:
        print(ValueError)
        messagebox.showerror("Input Error", "Please enter a valid numerical amount.")



# ---------------------------
# Toggle Data Source Functionality
# ---------------------------
def toggle_data_source():
    global use_custom_data
    use_custom_data = not use_custom_data
    # if use_custom_data:
    #     data_source_label.configure(text="Current Data Source: Custom Data")
    #     toggle_button.configure(text="Switch to API Data")
    # else:
    #     data_source_label.configure(text="Current Data Source: API Data")
    #     toggle_button.configure(text="Switch to Custom Data")





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

# Global variable to track history window
history_window = None

def show_history():
    global history_window, history_text  # Make history_text accessible in other functions

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
    
    # Scrollbar for large history
    scrollbar = tk.Scrollbar(history_window, command=history_text.yview)
    scrollbar.pack(side="right", fill="y")
    history_text.config(yscrollcommand=scrollbar.set)

    # Insert previous conversions
    if not conversion_history:
        history_text.insert("end", "No conversions have been made yet.\n")
    else:
        history_text.insert("end", f"{'Amount':<10} {'From':<6} {'To':<6} {'Converted':<12} {'Timestamp':<20}\n")
        history_text.insert("end", "-" * 60 + "\n")  # Separator

        for entry in conversion_history:
            history_text.insert("end", 
                f"{str(entry['amount']):<10} {entry['initial_currency']:<6} {entry['target_currency']:<6} "
                f"{str(entry['converted_amount']):<12} {entry['timestamp']:<20}\n"
            )

    history_text.config(state="disabled")

    def close_window():
        global history_window
        history_window.destroy()
        history_window = None

    close_button = tk.Button(history_window, text="Close", command=close_window, bg="blue")
    close_button.pack(pady=10)

    # Now this button calls the globally defined `clear_history()`
    clear_button = tk.Button(history_window, text="Clear History", command=clear_history, bg="red")
    clear_button.pack(pady=12)


def clear_history():
    global conversion_history, history_text  # Declare conversion_history as global

    # Clear in-memory history
    conversion_history.clear()

    # Overwrite JSON file with an empty list
    with open("history.json", "w") as file:
        json.dump(conversion_history, file, indent=4)

    # Clear the history text widget in UI
    if history_window and history_window.winfo_exists():
        history_text.config(state="normal")  # Allow editing
        history_text.delete("1.0", tk.END)   # Remove all content
        history_text.insert("end", "History cleared.\n")  # Confirmation message
        history_text.config(state="disabled")  # Make read-only again

    messagebox.showinfo("History Cleared", "Conversion history has been cleared.")



# Load the icon image using CTkImage
icon = ctk.CTkImage(light_image=Image.open("images/history_icon.png"), size=(20, 20))


# Create and place the "History" button
history_button = ctk.CTkButton(app, text="History", command=show_history, fg_color="#FCFBFB",hover_color="darkblue", text_color="black", image=icon, compound="left" )
history_button.place(x=0, y=10)  # Adjust position as needed



#fg_color="blue",  # Button background color
#hover_color="darkblue",  # Color when hovered
#text_color="white"  # Text color
#image=icon,  # Attach the icon
#compound="left"  # Position the icon to the left of the text

# ---------------------------
# UI Elements
# ---------------------------
initial_currency_var = ctk.StringVar(value="USD")
target_currency_var = ctk.StringVar(value="EUR")


# Initial Currency ComboBox
initial_currency_menu = ttk.Combobox(app, textvariable=initial_currency_var, font=("Arial", 20), width=15, height=10)
initial_currency_menu["values"] = currency_list
initial_currency_menu.place(x=30, y=80)
initial_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, initial_currency_menu, initial_currency_var))

# Entry under Initial Currency
initial_amount_entry = ctk.CTkEntry(app, width=260,height=60, font=("Arial", 20))
initial_amount_entry.place(x=30, y=160)
initial_amount_entry.bind("<KeyRelease>", convert_amount)  # Convert on typing




# Target Currency ComboBox
target_currency_menu = ttk.Combobox(app, textvariable=target_currency_var, font=("Arial", 20), width=15, height=10)
target_currency_menu["values"] = currency_list
target_currency_menu.place(x=350, y=80)
target_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, target_currency_menu, target_currency_var))


# Entry under Target Currency
target_amount_entry = ctk.CTkEntry(app, width=260,height=60, font=("Times New Roman", 20))
target_amount_entry.place(x=350, y=160)
target_amount_entry.bind("<KeyRelease>", reverse_convert_amount)  # Prevent typing

#convert_button = ctk.CTkButton(app, text="Convert",command=convert)
#convert_button.place(x=180, y=100)

# Label to display the current data source
# data_source_label = ctk.CTkLabel(app, text="Current Data Source: Custom Data")
# data_source_label.place(x=180, y=100)

# Toggle button to switch between custom data and API data
# toggle_button = ctk.CTkButton(app, text="Switch to API Data", command=toggle_data_source)
# toggle_button.place(x=180, y=150)

# Apply styling
style_combobox(app)


app.mainloop()

















# import tkinter as tk
# from tkinter import ttk
# import customtkinter as ctk
# import requests
# import json
# import os
# from dotenv import load_dotenv
# from datetime import datetime
# from tkinter import PhotoImage
# from PIL import Image
# from tkinter import messagebox



# # ---------------------------
# # UI Components
# # ---------------------------
# app = ctk.CTk()
# app.title("Real-Time Currency Converter")
# app.geometry("650x400")
# app.resizable(True, True)
# app.config(bg="#FCFBFB")


# #ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"

# # App Icon
# #Load image with CTkImage #(supports PNG, JPG, etc.)
# icon = ctk.CTkImage(light_image=Image.open("images/currency_icon.png"), size= (20, 20))


# #<img src="https://flagsapi.com/{}/:style/:size.png">


# # ---------------------------
# # Load Custom Data from JSON file
# # ---------------------------
# with open('custom_rates.json', 'r') as f:  # Load the JSON data
#     custom_rates_data = json.load(f)

# # ------------------------------------
# # API Configuration (unchanged aside from removing refresh)
# # ------------------------------------
# load_dotenv()
# API_KEY = os.getenv("API_KEY1")
# BASE_URL = "https://api.currencyapi.com/v3/latest"
# flag_base_url ="https://flagsapi.com/:country_code/:style/:size.png"



# # Fetch available currencies dynamically
# def get_available_currencies():
#     try:
#         response = requests.get(f"{BASE_URL}?apikey={API_KEY}")
#         response.raise_for_status()
#         data = response.json()
#         return list(data["data"].keys())  # Extract currency codes
#     except requests.exceptions.RequestException as e:
#         messagebox.showerror("Network Error", f"Failed to fetch currency list.\nError: {e}")
#         return []

# def get_exchange_rates():
#     try:
#         response = requests.get(f"{BASE_URL}?apikey={API_KEY}")
#         response.raise_for_status()
#         data = response.json()
#         cached_rates = data["data"]
#         return cached_rates
#     except requests.exceptions.RequestException as e:
#         messagebox.showerror("Network Error", f"Failed to fetch exchange rates.\nError: {e}")
#         return None

# # ---------------------------
# # Global variable for Data Source
# # ---------------------------
# # If True, use the custom data; if False, use API data.
# use_custom_data = True


# # ---------------------------
# # Currency List
# # ---------------------------
# # Dynamically fetch the currency list
# currency_list = get_available_currencies()


# # List to store conversion history
# #conversion_history = []


# # JSON file to store conversion history
# history_file = "history.json"

# # Function to load history from JSON file
# def load_history():
#     if os.path.exists(history_file):
#         try:
#             with open(history_file, "r") as file:
#                 return json.load(file)
#         except json.JSONDecodeError:
#             return []  # Return empty list if JSON is corrupted
#     return []



# # Function to save history to JSON file
# def save_history():
#     with open(history_file, "w") as file:
#         json.dump(conversion_history, file, indent=4)

# # Load existing history
# conversion_history = load_history()


# # ---------------------------
# # Conversion Function
# # ---------------------------


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

#         # Get the conversion rates
#         initial_rate = rates[initial_currency]["value"]
#         target_rate = rates[target_currency]["value"]
#         # print(initial_rate, target_rate)

#         # Determine which widget triggered the event
#         widget = event.widget.master if event else None

#         # If the initial amount entry triggered the event, convert to the target amount
#         if widget == initial_amount_entry:
#             amount_str = initial_amount_entry.get().strip()
#             if not amount_str:
#                 target_amount_entry.delete(0, tk.END)
#                 return
#             amount = float(amount_str)
#             converted = amount * (target_rate / initial_rate)
#             target_amount_entry.delete(0, tk.END)
#             target_amount_entry.insert(0, f"{converted:.2f}")

#             # Optionally, store conversion history here

#         # If the target amount entry triggered the event, convert to the initial amount
#         elif widget == target_amount_entry:
#             amount_str = target_amount_entry.get().strip()
#             if not amount_str:
#                 initial_amount_entry.delete(0, tk.END)
#                 return
#             amount = float(amount_str)
#             converted = amount * (initial_rate / target_rate)
#             initial_amount_entry.delete(0, tk.END)
#             initial_amount_entry.insert(0, f"{converted:.2f}")

        
#         if store_history:
#             # Store conversion in history
#             amount = float(initial_amount_entry.get().strip() or 0)
#             converted = amount * (target_rate / initial_rate)
#             conversion_history.append({
#                 "amount": amount,
#                 "initial_currency": initial_currency,
#                 "target_currency": target_currency,
#                 "converted_amount": round(converted, 2),
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
                
#             })
#             save_history()

#     except ValueError:
#         messagebox.showerror("Input Error", "Please enter a valid numerical amount.")

# # ---------------------------
# # Toggle Data Source Functionality
# # ---------------------------
# def toggle_data_source():
#     global use_custom_data
#     use_custom_data = not use_custom_data
#     # if use_custom_data:
#     #     data_source_label.configure(text="Current Data Source: Custom Data")
#     #     toggle_button.configure(text="Switch to API Data")
#     # else:
#     #     data_source_label.configure(text="Current Data Source: API Data")
#     #     toggle_button.configure(text="Switch to Custom Data")





# # Function to filter and auto-expand the dropdown
# def update_dropdown(event, combobox, currency_var):
#     search_term = currency_var.get().upper()
#     filtered_currencies = [c for c in currency_list if c.startswith(search_term)]  # Filter list

#     if filtered_currencies:
#         combobox["values"] = filtered_currencies  # Update dropdown with filtered values
#         combobox.event_generate("<Down>")  # Force dropdown to expand
#     else:
#         combobox["values"] = currency_list  # Reset if no match

# # Styling function to match CustomTkinter look
# def style_combobox(combobox):
#     combobox.option_add("*TCombobox*Listbox.font", ("Arial", 16))
#     combobox.option_add("*TCombobox*Listbox.background", "#2C2F33")  # Dark background
#     combobox.option_add("*TCombobox*Listbox.foreground", "white")  # White text

# # Global variable to track history window
# history_window = None

# def show_history():
#     global history_window, history_text  # Make history_text accessible in other functions

#     if history_window and history_window.winfo_exists():
#         history_window.lift()
#         return

#     history_window = tk.Toplevel(app)
#     history_window.title("Conversion History")
#     history_window.geometry("550x450")  

#     history_label = tk.Label(history_window, text="Conversion History", font=("Arial", 14, "bold"))
#     history_label.pack(pady=10)

#     history_text = tk.Text(history_window, wrap="none", height=18, width=70, font=("Courier", 10))
#     history_text.pack(pady=5, padx=10)
    
#     # Scrollbar for large history
#     scrollbar = tk.Scrollbar(history_window, command=history_text.yview)
#     scrollbar.pack(side="right", fill="y")
#     history_text.config(yscrollcommand=scrollbar.set)

#     # Insert previous conversions
#     if not conversion_history:
#         history_text.insert("end", "No conversions have been made yet.\n")
#     else:
#         history_text.insert("end", f"{'Amount':<10} {'From':<6} {'To':<6} {'Converted':<12} {'Timestamp':<20}\n")
#         history_text.insert("end", "-" * 60 + "\n")  # Separator

#         for entry in conversion_history:
#             history_text.insert("end", 
#                 f"{str(entry['amount']):<10} {entry['initial_currency']:<6} {entry['target_currency']:<6} "
#                 f"{str(entry['converted_amount']):<12} {entry['timestamp']:<20}\n"
#             )

#     history_text.config(state="disabled")

#     def close_window():
#         global history_window
#         history_window.destroy()
#         history_window = None

#     close_button = tk.Button(history_window, text="Close", command=close_window, bg="blue")
#     close_button.pack(pady=10)

#     # Now this button calls the globally defined `clear_history()`
#     clear_button = tk.Button(history_window, text="Clear History", command=clear_history, bg="red")
#     clear_button.pack(pady=12)


# def clear_history():
#     global conversion_history, history_text  # Declare conversion_history as global

#     # Show confirmation dialog
#     confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to clear all history?")

#     if confirm:  # If the user clicks "Yes"
#         # Clear in-memory history
#         conversion_history.clear()

#         # Overwrite JSON file with an empty list
#         with open("history.json", "w") as file:
#             json.dump(conversion_history, file, indent=4)

#         # Clear the history text widget in UI
#         if history_window and history_window.winfo_exists():
#             history_text.config(state="normal")  # Allow editing
#             history_text.delete("1.0", tk.END)   # Remove all content
#             history_text.insert("end", "History cleared.\n")  # Confirmation message
#             history_text.config(state="disabled")  # Make read-only again

#         messagebox.showinfo("History Cleared", "Conversion history has been cleared.")
#     else:
#         # User clicked "No", so do nothing and show a message
#         messagebox.showinfo("Action Canceled", "Conversion history was not cleared.")
        
        
# # Load the icon image using CTkImage
# icon = ctk.CTkImage(light_image=Image.open("images/history_icon.png"), size=(20, 20))


# # Create and place the "History" button
# history_button = ctk.CTkButton(app, text="History", command=show_history, fg_color="#FCFBFB",hover_color="darkblue", text_color="black", image=icon, compound="left" )
# history_button.place(x=0, y=10)  # Adjust position as needed



# #fg_color="blue",  # Button background color
# #hover_color="darkblue",  # Color when hovered
# #text_color="white"  # Text color
# #image=icon,  # Attach the icon
# #compound="left"  # Position the icon to the left of the text

# # ---------------------------
# # UI Elements
# # ---------------------------
# initial_currency_var = ctk.StringVar(value="USD")
# target_currency_var = ctk.StringVar(value="EUR")


# # Initial Currency ComboBox
# initial_currency_menu = ttk.Combobox(app, textvariable=initial_currency_var, font=("Arial", 20), width=15)
# initial_currency_menu["values"] = currency_list
# initial_currency_menu.place(x=30, y=80)
# initial_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, initial_currency_menu, initial_currency_var))

# # Entry under Initial Currency
# initial_amount_entry = ctk.CTkEntry(app, width=260,height=60, font=("Arial", 20))
# initial_amount_entry.place(x=30, y=160)
# initial_amount_entry.bind("<KeyRelease>", convert)  # Convert on typing




# # Target Currency ComboBox
# target_currency_menu = ttk.Combobox(app, textvariable=target_currency_var, font=("Arial", 20), width=15)
# target_currency_menu["values"] = currency_list
# target_currency_menu.place(x=350, y=80)
# target_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, target_currency_menu, target_currency_var))


# # Entry under Target Currency
# target_amount_entry = ctk.CTkEntry(app, width=260,height=60, font=("Times New Roman", 20))
# target_amount_entry.place(x=350, y=160)
# target_amount_entry.bind("<KeyRelease>", convert)  # Prevent typing

# convert_button = ctk.CTkButton(app, text="Convert", command=lambda:convert(store_history=True))
# convert_button.place(x=190, y=250)

# # Label to display the current data source
# # data_source_label = ctk.CTkLabel(app, text="Current Data Source: Custom Data")
# # data_source_label.place(x=180, y=100)

# # Toggle button to switch between custom data and API data
# # toggle_button = ctk.CTkButton(app, text="Switch to API Data", command=toggle_data_source)
# # toggle_button.place(x=180, y=150)

# # Apply styling
# style_combobox(app)


# app.mainloop()





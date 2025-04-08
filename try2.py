import tkinter as tk
import customtkinter as ctk
import requests
import json
import os
from dotenv import load_dotenv
from tkinter import messagebox

# ---------------------------
# UI Components
# ---------------------------
app = ctk.CTk()
app.title("Real-Time Currency Converter")
app.geometry("600x400")
app.resizable(True, True)
app.config(bg="#FCFBFB")

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
currency_list = [
    "USD", "EUR", "GBP", "JPY", "CNY", "INR", "AUD", "CAD", "CHF", "NZD",
    "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "BGN", "RON", "HRK",
    "MXN", "BRL", "ARS", "CLP", "COP", "PEN", "UYU",
    "AED", "SAR", "EGP", "ZAR", "GHS", "NGN", "KES", "MAD", "TND", "IQD",
    "SGD", "HKD", "KRW", "TWD", "THB", "MYR", "IDR", "PHP", "VND", "BDT", "PKR",
    "RUB", "UAH", "KZT", "GEL", "BYN", "AMD", "AZN",
    "TRY", "ISK", "LKR", "QAR", "OMR", "BHD", "JOD", "DZD", "MUR"
]



# List to store conversion history
conversion_history = []


# ---------------------------
# Conversion Function
# ---------------------------
'''def convert(event=None):  
    try:
        # Determine which entry field triggered the event
        source_entry = event.widget if event else None

        if source_entry == initial_amount_entry or source_entry is None:
            # User is typing in the initial amount (or clicked the button)
            amount = float(initial_amount_entry.get()) if initial_amount_entry.get().strip() else 0
            reverse = False  # Normal conversion
        elif source_entry == target_amount_entry:
            # User is typing in the target amount (reverse conversion)
            amount = float(target_amount_entry.get()) if target_amount_entry.get().strip() else 0
            reverse = True  # Reverse conversion
        else:
            return  # If neither entry triggered, exit

    except ValueError:
        amount = 0  # Default to 0 if input is invalid
    
    if amount == 0:
        return

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
        
        if initial_currency not in rates or target_currency not in rates:
            messagebox.showerror("Data Error", "One of the selected currencies is not available in the current data.")
            return
        
        # Perform conversion based on input direction
        initial_rate = rates[initial_currency]["value"]
        target_rate = rates[target_currency]["value"]

        if reverse:
            converted_amount = amount * (initial_rate / target_rate)  # Reverse conversion
            initial_amount_entry.delete(0, tk.END)
            initial_amount_entry.insert(0, f"{converted_amount:.2f}")
        else:
            converted_amount = amount * (target_rate / initial_rate)  # Normal conversion
            target_amount_entry.delete(0, tk.END)
            target_amount_entry.insert(0, f"{converted_amount:.2f}")

        # Store conversion in history
        result_text = f"{amount} {initial_currency} = {converted_amount:.2f} {target_currency}"
        conversion_history.append(result_text)

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")'''


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
        conversion_history.append(result_text)

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
        return

# initial_amount_entry.bind("<KeyRelease>", convert_amount)
# target_amount_entry.bind("<KeyRelease>", reverse_convert_amount)


# ---------------------------
# Toggle Data Source Functionality
# ---------------------------
def toggle_data_source():
    global use_custom_data
    use_custom_data = not use_custom_data
    if use_custom_data:
        data_source_label.configure(text="Current Data Source: Custom Data")
        # toggle_button.configure(text="Switch to API Data")
    else:
        data_source_label.configure(text="Current Data Source: API Data")
        # toggle_button.configure(text="Switch to Custom Data")



# Function to filter and update dropdown

def update_dropdown(event, combobox, currency_var):
    search_term = currency_var.get().upper()
    filtered_currencies = [c for c in currency_list if search_term in c]
    
    if filtered_currencies:
        combobox.configure(values=filtered_currencies)
    else:
        combobox.configure(values=currency_list)  # Reset if no match


# Global variable to track history window
history_window = None

def show_history():
    global history_window

    # Check if history window is already open
    if history_window and history_window.winfo_exists():
        history_window.lift()  # Bring existing window to front
        return

    # Create a new window since it doesn't exist
    history_window = tk.Toplevel(app)
    history_window.title("Conversion History")
    history_window.geometry("300x400")

    # Display history
    history_label = tk.Label(history_window, text="Conversion History", font=("Arial", 14, "bold"))
    history_label.pack(pady=10)

    history_text = tk.Text(history_window, wrap="word", height=15, width=35)
    history_text.pack(pady=5)
    
    # Insert previous conversions
    if not conversion_history:
        history_text.insert("end", "No conversions have been made yet.\n")
    else:
        for entry in conversion_history:
            history_text.insert("end", entry + "\n")

    history_text.config(state="disabled")  # Make text read-only


     # Close button
    def close_window():
        global history_window
        history_window.destroy()
        history_window = None  # Reset the reference

    close_button = tk.Button(history_window, text="Close", command=close_window)
    close_button.pack(pady=10)


# Create and place the "History" button
history_button = ctk.CTkButton(app, text="History", command=show_history)
history_button.place(x=190, y=240)  # Adjust position as needed


# ---------------------------
# UI Elements
# ---------------------------
initial_currency_var = ctk.StringVar(value="USD")
target_currency_var = ctk.StringVar(value="EUR")


# Initial Currency ComboBox
initial_currency_menu = ctk.CTkComboBox(app, values=currency_list, variable=initial_currency_var, width=170)
initial_currency_menu.place(x=30, y=10)
initial_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, initial_currency_menu, initial_currency_var))


# Entry under Initial Currency
initial_amount_entry = ctk.CTkEntry(app, width=170)
initial_amount_entry.place(x=30, y=50)
initial_amount_entry.bind("<KeyRelease>", convert_amount)  # Convert on typing




# Target Currency ComboBox
target_currency_menu = ctk.CTkComboBox(
    app, values=currency_list, variable=target_currency_var, width=170)
target_currency_menu.place(x=300, y=10)
target_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, target_currency_menu, target_currency_var))


# Entry under Target Currency
target_amount_entry = ctk.CTkEntry(app, width=170)
target_amount_entry.place(x=300, y=50)
target_amount_entry.bind("<KeyRelease>", reverse_convert_amount)  # Prevent typing



# amount_entry = ctk.CTkEntry(app, width=140, placeholder_text="Enter amount")
# amount_entry.place(x=180, y=60)

convert_button = ctk.CTkButton(app, text="Convert",command=convert_amount)
convert_button.place(x=180, y=200)


# Label to display the current data source
data_source_label = ctk.CTkLabel(app, text="Current Data Source: Custom Data")
data_source_label.place(x=180, y=100)

# Toggle button to switch between custom data and API data
toggle_button = ctk.CTkButton(app, text="Switch to API Data", command=toggle_data_source)
toggle_button.place(x=180, y=150)

app.mainloop()





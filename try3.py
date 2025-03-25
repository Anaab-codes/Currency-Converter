import tkinter as tk
import customtkinter as ctk
import requests
import json
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
API_KEY = "cur_live_1mSuanw4qX2TYNrlnqNFPTOeGxlUF5ZdwqZnvF3z"
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
def convert_amount():
    try:
        amount = float(amount_entry.get())
        initial_currency = initial_currency_var.get()
        target_currency = target_currency_var.get()
        
        if not initial_currency or not target_currency:
            messagebox.showerror("Selection Error", "Please select both currencies.")
            return
        if initial_currency == target_currency:
            messagebox.showwarning("Invalid Selection", "Currencies cannot be the same!")
            return

        # Choose data source based on toggle
        if use_custom_data:
            rates = custom_rates_data["data"]
        else:
            rates = get_exchange_rates()
            if rates is None:
                return
        
        if initial_currency not in rates or target_currency not in rates:
            messagebox.showerror("Data Error", "One of the selected currencies is not available in the current data.")
            return
        
        # Conversion: (amount) * (target_rate / initial_rate)
        initial_rate = rates[initial_currency]["value"]
        target_rate = rates[target_currency]["value"]
        conversion_factor = target_rate / initial_rate
        converted_amount = amount * conversion_factor
        
        result_text = f"{amount} {initial_currency} = {converted_amount:.2f} {target_currency}"
        converted_amount_label.configure(text=result_text)
        # Store conversion in history
        conversion_history.append(result_text)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numerical amount.")

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
initial_currency_menu = ctk.CTkComboBox(
    app, values=currency_list, variable=initial_currency_var, width=170)
initial_currency_menu.place(x=30, y=10)
initial_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, initial_currency_menu, initial_currency_var))

# Target Currency ComboBox
target_currency_menu = ctk.CTkComboBox(
    app, values=currency_list, variable=target_currency_var, width=170)
target_currency_menu.place(x=300, y=10)
target_currency_menu.bind("<KeyRelease>", lambda event: update_dropdown(event, target_currency_menu, target_currency_var))


amount_entry = ctk.CTkEntry(app, width=140, placeholder_text="Enter amount")
amount_entry.place(x=180, y=60)

convert_button = ctk.CTkButton(app, text="Convert",command=convert_amount)
convert_button.place(x=180, y=100)

converted_amount_label = ctk.CTkLabel(app, text="Converted Amount", width=150)
converted_amount_label.place(x=180, y=140)

# Label to display the current data source
data_source_label = ctk.CTkLabel(app, text="Current Data Source: Custom Data")
data_source_label.place(x=180, y=180)

# Toggle button to switch between custom data and API data
# toggle_button = ctk.CTkButton(app, text="Switch to API Data", command=toggle_data_source)
# toggle_button.grid(row=5, column=1, padx=10, pady=10)

app.mainloop()




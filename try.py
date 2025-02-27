import tkinter as tk
import customtkinter as ctk
import requests
import json
from tkinter import messagebox

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
    """Fetch rates from the API with basic caching (30-minute duration)."""
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
        
        converted_amount_label.configure(
            text=f"Converted amount: {converted_amount:.2f} {target_currency}"
        )
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

# ---------------------------
# UI Components
# ---------------------------
app = ctk.CTk()
app.title("Real-Time Currency Converter")
app.geometry("600x400")
app.resizable(True, True)
app.config(bg="#FCFBFB")

initial_currency_var = ctk.StringVar(value="Initial Currency")
target_currency_var = ctk.StringVar(value="Target Currency")

initial_currency_menu = ctk.CTkComboBox(app, values=currency_list, variable=initial_currency_var)
initial_currency_menu.grid(row=0, column=0, padx=10, pady=10)

target_currency_menu = ctk.CTkComboBox(app, values=currency_list, variable=target_currency_var)
target_currency_menu.grid(row=0, column=2, padx=10, pady=10)

amount_entry = ctk.CTkEntry(app, width=200, placeholder_text="Enter amount")
amount_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

convert_button = ctk.CTkButton(app, text="Convert", command=convert_amount)
convert_button.grid(row=2, column=1, padx=10, pady=10)

converted_amount_label = ctk.CTkLabel(app, text="Converted Amount", width=200)
converted_amount_label.grid(row=3, column=1, padx=10, pady=10)

# Label to display the current data source
data_source_label = ctk.CTkLabel(app, text="Current Data Source: Custom Data")
data_source_label.grid(row=4, column=1, padx=10, pady=5)

# Toggle button to switch between custom data and API data
# toggle_button = ctk.CTkButton(app, text="Switch to API Data", command=toggle_data_source)
# toggle_button.grid(row=5, column=1, padx=10, pady=10)

app.mainloop()

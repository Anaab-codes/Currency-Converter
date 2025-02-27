import os
import json
import tkinter as tk
import customtkinter as ctk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import time

# -------------------------------
# Save/Load Custom Rates Data
# -------------------------------
CUSTOM_DATA_FILENAME = "custom_rates_data.json"

if not os.path.exists(CUSTOM_DATA_FILENAME):
    custom_rates_data = {
        "meta": {"last_updated_at": "2025-02-24T23:59:59Z"},
        "data": {
            "USD": {"code": "USD", "value": 0.0105595714},
            "EUR": {"code": "EUR", "value": 0.010093368},
            "GBP": {"code": "GBP", "value": 0.0083705737},
            "JPY": {"code": "JPY", "value": 1.5827180439},
            "CNY": {"code": "CNY", "value": 0.0765449714},
            "INR": {"code": "INR", "value": 0.915264539},
            "AUD": {"code": "AUD", "value": 0.016661},
            "CAD": {"code": "CAD", "value": 0.01507643},
            "CHF": {"code": "CHF", "value": 0.0094783784},
            "NZD": {"code": "NZD", "value": 0.0184434557},
            "SEK": {"code": "SEK", "value": 0.1126470972},
            "NOK": {"code": "NOK", "value": 0.1175255067},
            "DKK": {"code": "DKK", "value": 0.0753008443},
            "PLN": {"code": "PLN", "value": 0.041770503},
            "CZK": {"code": "CZK", "value": 0.2518574339},
            "HUF": {"code": "HUF", "value": 4.0467411266},
            "BGN": {"code": "BGN", "value": 0.0196985673},
            "RON": {"code": "RON", "value": 0.0502348464},
            "HRK": {"code": "HRK", "value": 0.0708610709},
            "MXN": {"code": "MXN", "value": 0.2162455805},
            "BRL": {"code": "BRL", "value": 0.061037291},
            "ARS": {"code": "ARS", "value": 11.1984988896},
            "CLP": {"code": "CLP", "value": 9.972878435},
            "COP": {"code": "COP", "value": 43.4814062967},
            "PEN": {"code": "PEN", "value": 0.0389781309},
            "UYU": {"code": "UYU", "value": 0.4529556261},
            "AED": {"code": "AED", "value": 0.0387910134},
            "SAR": {"code": "SAR", "value": 0.0395559485},
            "EGP": {"code": "EGP", "value": 0.5345294963},
            "ZAR": {"code": "ZAR", "value": 0.1939070217},
            "GHS": {"code": "GHS", "value": 0.1632388576},
            "NGN": {"code": "NGN", "value": 15.847603738},
            "KES": {"code": "KES", "value": 1.3673028624},
            "MAD": {"code": "MAD", "value": 0.1050726081},
            "TND": {"code": "TND", "value": 0.0333675118},
            "IQD": {"code": "IQD", "value": 13.8166504489},
            "SGD": {"code": "SGD", "value": 0.0141400072},
            "HKD": {"code": "HKD", "value": 0.0820738563},
            "KRW": {"code": "KRW", "value": 15.0753349444},
            "TWD": {"code": "TWD", "value": 0.3458632743},
            "THB": {"code": "THB", "value": 0.3539810679},
            "MYR": {"code": "MYR", "value": 0.0465747912},
            "IDR": {"code": "IDR", "value": 171.688177214},
            "PHP": {"code": "PHP", "value": 0.6113822569},
            "VND": {"code": "VND", "value": 268.9585156372},
            "BDT": {"code": "BDT", "value": 1.2852275355},
            "PKR": {"code": "PKR", "value": 2.9516932103},
            "RUB": {"code": "RUB", "value": 0.9309845681},
            "UAH": {"code": "UAH", "value": 0.440677696},
            "KZT": {"code": "KZT", "value": 5.2772417823},
            "GEL": {"code": "GEL", "value": 0.0297479},
            "BYN": {"code": "BYN", "value": 0.0345300293},
            "AMD": {"code": "AMD", "value": 4.1619369089},
            "AZN": {"code": "AZN", "value": 0.0179512713},
            "TRY": {"code": "TRY", "value": 0.384966425},
            "ISK": {"code": "ISK", "value": 1.4629434756},
            "LKR": {"code": "LKR", "value": 3.1255753845},
            "QAR": {"code": "QAR", "value": 0.0384444485},
            "OMR": {"code": "OMR", "value": 0.0040577272},
            "BHD": {"code": "BHD", "value": 0.0039703988},
            "JOD": {"code": "JOD", "value": 0.0074972957},
            "DZD": {"code": "DZD", "value": 1.4266568666},
            "MUR": {"code": "MUR", "value": 0.4863325255}
        }
    }
    with open(CUSTOM_DATA_FILENAME, "w") as outfile:
        json.dump(custom_rates_data, outfile, indent=4)
else:
    with open(CUSTOM_DATA_FILENAME, "r") as infile:
        custom_rates_data = json.load(infile)

# -------------------------------
# API Configuration (No Refresh)
# -------------------------------
API_KEY = "cur_live_1mSuanw4qX2TYNrlnqNFPTOeGxlUF5ZdwqZnvF3z"
BASE_URL = "https://api.currencyapi.com/v3/latest"
cached_rates = {}
cached_time = 0

def get_exchange_rates():
    global cached_rates, cached_time
    current_time = time.time()
    if current_time - cached_time < 1800 and cached_rates:
        return cached_rates
    try:
        response = requests.get(f"{BASE_URL}?apikey={API_KEY}")
        response.raise_for_status()
        data = response.json()
        cached_rates = data["data"]
        cached_time = current_time
        return cached_rates
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to fetch exchange rates.\nError: {e}")
        return None

# -------------------------------
# Currency List and Flag URL Mapping
# -------------------------------
currency_list = [
    "USD", "EUR", "GBP", "JPY", "CNY", "INR", "AUD", "CAD", "CHF", "NZD",
    "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "BGN", "RON", "HRK",
    "MXN", "BRL", "ARS", "CLP", "COP", "PEN", "UYU",
    "AED", "SAR", "EGP", "ZAR", "GHS", "NGN", "KES", "MAD", "TND", "IQD",
    "SGD", "HKD", "KRW", "TWD", "THB", "MYR", "IDR", "PHP", "VND", "BDT", "PKR",
    "RUB", "UAH", "KZT", "GEL", "BYN", "AMD", "AZN",
    "TRY", "ISK", "LKR", "QAR", "OMR", "BHD", "JOD", "DZD", "MUR"
]

# Mapping currency code to the ISO country code for flagcdn.com (all in lowercase)
currency_flag_url_mapping = {
    "USD": "https://flagcdn.com/w320/us.png",
    "EUR": "https://flagcdn.com/w320/eu.png",  # Using the EU flag for the Eurozone
    "GBP": "https://flagcdn.com/w320/gb.png",
    "JPY": "https://flagcdn.com/w320/jp.png",
    "CNY": "https://flagcdn.com/w320/cn.png",
    "INR": "https://flagcdn.com/w320/in.png",
    "AUD": "https://flagcdn.com/w320/au.png",
    "CAD": "https://flagcdn.com/w320/ca.png",
    "CHF": "https://flagcdn.com/w320/ch.png",
    "NZD": "https://flagcdn.com/w320/nz.png",
    "SEK": "https://flagcdn.com/w320/se.png",
    "NOK": "https://flagcdn.com/w320/no.png",
    "DKK": "https://flagcdn.com/w320/dk.png",
    "PLN": "https://flagcdn.com/w320/pl.png",
    "CZK": "https://flagcdn.com/w320/cz.png",
    "HUF": "https://flagcdn.com/w320/hu.png",
    "BGN": "https://flagcdn.com/w320/bg.png",
    "RON": "https://flagcdn.com/w320/ro.png",
    "HRK": "https://flagcdn.com/w320/hr.png",
    "MXN": "https://flagcdn.com/w320/mx.png",
    "BRL": "https://flagcdn.com/w320/br.png",
    "ARS": "https://flagcdn.com/w320/ar.png",
    "CLP": "https://flagcdn.com/w320/cl.png",
    "COP": "https://flagcdn.com/w320/co.png",
    "PEN": "https://flagcdn.com/w320/pe.png",
    "UYU": "https://flagcdn.com/w320/uy.png",
    "AED": "https://flagcdn.com/w320/ae.png",
    "SAR": "https://flagcdn.com/w320/sa.png",
    "EGP": "https://flagcdn.com/w320/eg.png",
    "ZAR": "https://flagcdn.com/w320/za.png",
    "GHS": "https://flagcdn.com/w320/gh.png",
    "NGN": "https://flagcdn.com/w320/ng.png",
    "KES": "https://flagcdn.com/w320/ke.png",
    "MAD": "https://flagcdn.com/w320/ma.png",
    "TND": "https://flagcdn.com/w320/tn.png",
    "IQD": "https://flagcdn.com/w320/iq.png",
    "SGD": "https://flagcdn.com/w320/sg.png",
    "HKD": "https://flagcdn.com/w320/hk.png",
    "KRW": "https://flagcdn.com/w320/kr.png",
    "TWD": "https://flagcdn.com/w320/tw.png",
    "THB": "https://flagcdn.com/w320/th.png",
    "MYR": "https://flagcdn.com/w320/my.png",
    "IDR": "https://flagcdn.com/w320/id.png",
    "PHP": "https://flagcdn.com/w320/ph.png",
    "VND": "https://flagcdn.com/w320/vn.png",
    "BDT": "https://flagcdn.com/w320/bd.png",
    "PKR": "https://flagcdn.com/w320/pk.png",
    "RUB": "https://flagcdn.com/w320/ru.png",
    "UAH": "https://flagcdn.com/w320/ua.png",
    "KZT": "https://flagcdn.com/w320/kz.png",
    "GEL": "https://flagcdn.com/w320/ge.png",
    "BYN": "https://flagcdn.com/w320/by.png",
    "AMD": "https://flagcdn.com/w320/am.png",
    "AZN": "https://flagcdn.com/w320/az.png",
    "TRY": "https://flagcdn.com/w320/tr.png",
    "ISK": "https://flagcdn.com/w320/is.png",
    "LKR": "https://flagcdn.com/w320/lk.png",
    "QAR": "https://flagcdn.com/w320/qa.png",
    "OMR": "https://flagcdn.com/w320/om.png",
    "BHD": "https://flagcdn.com/w320/bh.png",
    "JOD": "https://flagcdn.com/w320/jo.png",
    "DZD": "https://flagcdn.com/w320/dz.png",
    "MUR": "https://flagcdn.com/w320/mu.png",
}

# -------------------------------
# Image Caching for Flags
# -------------------------------
flag_images = {}

def get_flag_image_cached(currency_code, width=50):
    """Download and cache the flag image for the given currency code."""
    if currency_code in flag_images:
        return flag_images[currency_code]
    url = currency_flag_url_mapping.get(currency_code)
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = response.content
            pil_image = Image.open(BytesIO(image_data))
            aspect_ratio = pil_image.height / pil_image.width
            pil_image = pil_image.resize((width, int(width * aspect_ratio)), Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(pil_image)
            flag_images[currency_code] = tk_image
            return tk_image
        except Exception as e:
            print(f"Error loading flag for {currency_code}: {e}")
    return None

# -------------------------------
# Global Variable for Data Source
# -------------------------------
# If True, use custom data; if False, use API data.
use_custom_data = True

# -------------------------------
# Currency Conversion Function
# -------------------------------
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
        
        initial_rate = rates[initial_currency]["value"]
        target_rate = rates[target_currency]["value"]
        conversion_factor = target_rate / initial_rate
        converted_amount = amount * conversion_factor
        
        converted_amount_label.configure(
            text=f"Converted amount: {converted_amount:.2f} {target_currency}"
        )
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numerical amount.")

# -------------------------------
# Toggle Data Source Functionality
# -------------------------------
def toggle_data_source():
    global use_custom_data
    use_custom_data = not use_custom_data
    if use_custom_data:
        data_source_label.configure(text="Current Data Source: Custom Data")
        toggle_button.configure(text="Switch to API Data")
    else:
        data_source_label.configure(text="Current Data Source: API Data")
        toggle_button.configure(text="Switch to Custom Data")

# -------------------------------
# Flag Update Functions
# -------------------------------
def update_initial_flag(*args):
    code = initial_currency_var.get()
    img = get_flag_image_cached(code)
    if img:
        initial_flag_label.configure(image=img)
        initial_flag_label.image = img

def update_target_flag(*args):
    code = target_currency_var.get()
    img = get_flag_image_cached(code)
    if img:
        target_flag_label.configure(image=img)
        target_flag_label.image = img

# -------------------------------
# Tkinter UI Setup
# -------------------------------
app = ctk.CTk()
app.title("Currency Converter with Real Flags")
app.geometry("650x500")
app.config(bg="#FCFBFB")

# Currency Selection Variables
initial_currency_var = ctk.StringVar(value="USD")
target_currency_var = ctk.StringVar(value="EUR")

# Comboboxes for currencies
initial_currency_menu = ctk.CTkComboBox(app, values=currency_list, variable=initial_currency_var)
initial_currency_menu.grid(row=0, column=0, padx=10, pady=10)

target_currency_menu = ctk.CTkComboBox(app, values=currency_list, variable=target_currency_var)
target_currency_menu.grid(row=0, column=2, padx=10, pady=10)

# Bind selection events to update flags
initial_currency_menu.bind("<<ComboboxSelected>>", update_initial_flag)
target_currency_menu.bind("<<ComboboxSelected>>", update_target_flag)

# Flag Labels (initial and target)
initial_flag_label = ctk.CTkLabel(app, text="")
initial_flag_label.grid(row=1, column=0, padx=10, pady=5)

target_flag_label = ctk.CTkLabel(app, text="")
target_flag_label.grid(row=1, column=2, padx=10, pady=5)

# Entry for amount and conversion button
amount_entry = ctk.CTkEntry(app, width=200, placeholder_text="Enter amount")
amount_entry.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

convert_button = ctk.CTkButton(app, text="Convert", command=convert_amount)
convert_button.grid(row=3, column=1, padx=10, pady=10)

converted_amount_label = ctk.CTkLabel(app, text="Converted Amount", width=200)
converted_amount_label.grid(row=4, column=1, padx=10, pady=10)

# Data Source Toggle
data_source_label = ctk.CTkLabel(app, text="Current Data Source: Custom Data")
data_source_label.grid(row=5, column=1, padx=10, pady=5)

toggle_button = ctk.CTkButton(app, text="Switch to API Data", command=toggle_data_source)
toggle_button.grid(row=6, column=1, padx=10, pady=10)

# Initialize flag images for the default selections
update_initial_flag()
update_target_flag()

app.mainloop()

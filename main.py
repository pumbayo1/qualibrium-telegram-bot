import psutil
import pandas as pd
import requests
from telegram import Bot
import schedule
import time
import os
from dotenv import load_dotenv

# Wczytanie zmiennych z pliku config.env
load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Ustawienia bota Telegram
bot = Bot(token=bot_token)

# Funkcje monitorujące stan serwera
def is_server_running():
    return psutil.cpu_percent(interval=1)

def check_server():
    load = is_server_running()
    if load > 90:
        return False, load
    return True, load

# Odczytanie i sumowanie tokenów
def read_and_sum_tokens(file_path):
    try:
        df = pd.read_csv(file_path)
        total_tokens = df['tokens'].sum()
        return total_tokens
    except FileNotFoundError:
        return 0

def sum_tokens_across_servers(file_paths):
    total_tokens = 0
    for file_path in file_paths:
        total_tokens += read_and_sum_tokens(file_path)
    return total_tokens

# Pobieranie ceny tokena z CoinGecko
def get_token_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=wrapped-quil&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data['wrapped-quil']['usd']

# Wyliczenie wydobycia na godzinę
previous_balance = 0
def calculate_hourly_production(current_balance):
    global previous_balance
    production = current_balance - previous_balance
    previous_balance = current_balance
    return production

# Funkcja do wysyłania powiadomień
def send_telegram_message(message):
    bot.send_message(chat_id=chat_id, text=message)

# Główna logika monitorowania
def monitor_servers():
    servers = ['server1/balance_log.csv', 'server2/balance_log.csv']  # Lista ścieżek do plików CSV
    total_tokens = sum_tokens_across_servers(servers)
    token_price = get_token_price()
    hourly_production = calculate_hourly_production(total_tokens)

    server_running, cpu_load = check_server()
    if not server_running:
        send_telegram_message(f'Server down! CPU load: {cpu_load}%')

    total_value = total_tokens * token_price
    message = (f'Total tokens: {total_tokens}, Hourly production: {hourly_production}, '
               f'Token price: {token_price}$, Total value: {total_value}$')
    send_telegram_message(message)

# Harmonogram co godzinę
schedule.every(1).hours.do(monitor_servers)

while True:
    schedule.run_pending()
    time.sleep(1)

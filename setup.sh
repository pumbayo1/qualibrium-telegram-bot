#!/bin/bash

# Aktualizacja systemu i instalacja pip
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Tworzenie wirtualnego środowiska
python3 -m venv venv
source venv/bin/activate

# Klonowanie repozytorium
git clone https://github.com/pumbayo1/qualibrium-telegram-bot.git
cd qualibrium-telegram-bot

# Instalacja wymaganych bibliotek
pip install -r requirements.txt

# Pobranie tokenu bota i ID chatu od użytkownika
read -p "Podaj swój TELEGRAM_BOT_TOKEN: " bot_token
read -p "Podaj swój TELEGRAM_CHAT_ID: " chat_id

# Zapisanie danych do pliku konfiguracyjnego
echo "TELEGRAM_BOT_TOKEN=$bot_token" > config.env
echo "TELEGRAM_CHAT_ID=$chat_id" >> config.env

# Uruchomienie bota
python3 main.py

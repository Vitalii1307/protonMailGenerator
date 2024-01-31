# Michi4's ProtonMail Generator

import platform
import ctypes
import re
import random
import string
import time
import webbrowser
import pyautogui

CF_TEXT = 1

def is_windows():
    return platform.system() == 'Windows'

def get_clipboard_data():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            return ctypes.c_char_p(kernel32.GlobalLock(data)).value
    finally:
        user32.CloseClipboard()

def get_clip_6_digit():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            return re.search(r'(\d{6})', ctypes.c_char_p(kernel32.GlobalLock(data)).value).group(0)
    finally:
        user32.CloseClipboard()

def get_mail():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            value = ctypes.c_char_p(kernel32.GlobalLock(data)).value
            valid_domains = ["@dropmail.me", "@emltmp.com", "@spymail.one", "@10mail.org"]
            return next((re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', value).group(0) for domain in valid_domains if domain in value), False)
    finally:
        user32.CloseClipboard()

def open_protonmail_signup():
    webbrowser.open('https://account.proton.me/signup?plan=free')
    time.sleep(5)

def randomize(option, length):
    if length <= 0:
        return 'error'

    characters = {
        '-p': string.ascii_letters + string.digits + string.punctuation,
        '-s': string.ascii_letters + string.digits,
        '-l': string.ascii_letters,
        '-n': string.digits,
        '-m': 'JFMASOND',
    }

    if option in characters:
        if option == '-d':
            return str(random.randint(1, 28))
        elif option == '-y':
            return str(random.randint(1950, 2000))
        else:
            return ''.join(random.choice(characters[option]) for _ in range(length))

    return 'error'

def generate_protonmail_account():
    username = randomize('-s', 15)
    pyautogui.typewrite(username + '\t\t\t')
    print("Username:", username)

    password = randomize('-p', 16)
    pyautogui.typewrite(password + '\t' + password + '\t')
    print("Password:", password)

    pyautogui.typewrite('\n')
    time.sleep(5)
    pyautogui.typewrite('\t\t\t\n')

    pyautogui.hotkey('ctrlleft', 't')

    time.sleep(10)
    pyautogui.typewrite('https://dropmail.me/\n')

    pyautogui.hotkey('shift', 'down')
    time.sleep(10)

    new_mail = True
    while True:
        if not new_mail:
            pyautogui.hotkey('ctrlleft', 'r')
            time.sleep(5)
        pyautogui.typewrite('\t' * 50)
        pyautogui.hotkey('ctrlleft', 'shiftleft', 'shiftright', 'down')
        pyautogui.hotkey('ctrlleft', 'c')
        new_mail = get_mail()
        if new_mail:
            print("10 min mail:", new_mail)
            break

    pyautogui.hotkey('ctrlleft', 'v')
    pyautogui.press('backspace')
    pyautogui.typewrite('\n')

    time.sleep(10)

    pyautogui.hotkey('ctrlleft', 'a', 'c')
    time.sleep(5)
    pyautogui.typewrite(get_clip_6_digit() + '\n')

    time.sleep(5)
    pyautogui.typewrite('\n\t\t\t\t\n\t\n')

    print(username + "@proton.me:", password)

    with open("accLog.txt", "a") as logfile:
        logfile.write(username + "@proton.me:" + password + "\n")

if __name__ == "__main__":
    if is_windows():
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32

        open_protonmail_signup()
        generate_protonmail_account()
    else:
        print("This script is designed for Windows. Please run it on a Windows system.")
import time
try:
    from machine import Pin  # Works on Pico with CircuitPython
    microcontroller = True
except ImportError:
    microcontroller = False  # For testing on PC

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import usb_hid

# Initialize the USB keyboard
keyboard = Keyboard(usb_hid.devices)

# Recognized command keywords
COMMANDS = {"open", "search", "play"}

CHAR_MAP = {".": Keycode.PERIOD, ",": Keycode.COMMA}

def split_commands(command_list):
    """Splits the command list into structured tasks based on command keywords."""
    tasks = []
    current_task = []
    for word in command_list:
        if word in COMMANDS:
            if current_task:
                tasks.append(current_task)
            current_task = [word]
        else:
            current_task.append(word)
    if current_task:
        tasks.append(current_task)
    return tasks

def type_text(text):
    """Simulates typing text using USB HID keyboard."""
    for char in text:
        try:
            keycode = CHAR_MAP.get(char, getattr(Keycode, char.upper(), None))
            if keycode:
                keyboard.press(keycode)
                time.sleep(0.01)
                keyboard.release(keycode)
        except AttributeError:
            if char == " ":
                keyboard.press(Keycode.SPACE)
                keyboard.release(Keycode.SPACE)
        time.sleep(0.1)
    
    keyboard.press(Keycode.ENTER)
    keyboard.release(Keycode.ENTER)
    time.sleep(0.5)

def press(key):
    """Simulates pressing a key (or key combination) using USB HID keyboard."""
    key = key.lower()
    if key == "win":
        keyboard.press(Keycode.GUI)
        time.sleep(0.03)
        keyboard.release(Keycode.GUI)
    elif key == "enter":
        keyboard.press(Keycode.ENTER)
        time.sleep(0.02)
        keyboard.release(Keycode.ENTER)
    elif key == "ctrl+l":
        keyboard.press(Keycode.CONTROL, Keycode.L)
        time.sleep(0.02)
        keyboard.release_all()
    elif key == "alt+d":
        keyboard.press(Keycode.ALT, Keycode.D)
        time.sleep(0.02)
        keyboard.release_all()
    elif key == "ctrl+t":
        keyboard.press(Keycode.CONTROL, Keycode.T)
        time.sleep(0.02)
        keyboard.release_all()
    elif key == "tab":
        keyboard.press(Keycode.TAB)
        time.sleep(0.02)
        keyboard.release(Keycode.TAB)
    elif key == "/":  # Use the correct keycode for forward slash
        keyboard.press(Keycode.FORWARD_SLASH)
        time.sleep(0.02)
        keyboard.release(Keycode.FORWARD_SLASH)
    else:
        print(f"Unknown key command: {key}")
    time.sleep(0.03)

def execute_command(command_list):
    """Processes structured commands and executes keystrokes accordingly."""
    tasks = split_commands(command_list)
    for task in tasks:
        if not task:
            continue
        command = task[0]
        arguments = task[1:]

        if command == "open":
            keyboard.press(Keycode.GUI, Keycode.D)  # Minimize all windows
            time.sleep(0.05)
            keyboard.release_all()
            time.sleep(1)

            press("win")  # Open Start Menu
            time.sleep(1)

            if arguments:
                type_text(" ".join(arguments))
                time.sleep(0.05)
                press("enter")
                time.sleep(1)

        elif command == "search":
            try:
                press("ctrl+l")  # Focus address bar
            except:
                press("alt+d")  # Alternative for some browsers
            time.sleep(0.05)

            if arguments:
                type_text(" ".join(arguments))
                time.sleep(0.5)
                press("enter")
                time.sleep(2)

        elif command == "play":
            press("ctrl+t")  # Open a new tab
            time.sleep(0.05)

            type_text("youtube.com")  # Type full URL
            time.sleep(0.05)
            press("enter")
            time.sleep(1)

            press("/")  # Focus on YouTube search bar by typing '/'
            time.sleep(0.05)

            if arguments:
                type_text(" ".join(arguments))
                time.sleep(0.5)
                press("enter")
                time.sleep(1)

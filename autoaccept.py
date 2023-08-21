import os
import io
import pyautogui
import pystray
from PIL import Image
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import win32gui
import base64
import threading
from io import BytesIO
from PIL import Image
import keyboard  # Import the keyboard library
from constants import TRAY_ICON_BASE64, BUTTON_ACCEPT_BASE64

class TrayIconThread(threading.Thread):
    def __init__(self, image, menu):
        super().__init__()
        self.image = image
        self.menu = menu
        self.icon = None

    def run(self):
        self.icon = pystray.Icon("Auto Accept", self.image, "Auto Accept", self.menu)
        self.icon.run()

    def stop(self):
        if self.icon is not None:
            self.icon.stop()

class Dota2QueueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Accept")

        image = Image.open(io.BytesIO(base64.b64decode(TRAY_ICON_BASE64)))
        menu = (pystray.MenuItem('Exit', self.close_application),)

        self.tray_thread = TrayIconThread(image, menu)
        self.tray_thread.start()


        # Bind the Ctrl + X key combination to a function that will close the application
        keyboard.add_hotkey('ctrl+x', self.close_application)  # Use the keyboard library

        data_button_accept = base64.b64decode(BUTTON_ACCEPT_BASE64)
        self.accept_image = Image.open(BytesIO(data_button_accept))

        self.root.configure(bg="#171d25")  # Set the background color of the root window

        self.message_label = ttk.Label(self.root, text="", font=("Proxima Nova ExCn Rg", 16), anchor="center", background="#171d25", foreground="white")
        self.message_label.pack(fill="both", expand=True)  # Center both horizontally and vertically

        self.close_label_bg = tk.Label(self.root, background="#2b2b2b")
        self.close_label_bg.pack(fill="both", expand=True)

        self.close_label = ttk.Label(self.close_label_bg, text="Ctrl + X to close", font=("Trajan Pro Bold", 8), anchor="center", background="#0e1218", foreground="#818181")
        self.close_label.pack(fill="both", expand=True)



        self.queue_thread = Thread(target=self.look_for_match)
        self.queue_thread.start()

        self.root.withdraw()  # Hide the GUI initially

        # Start a thread to continuously check the Dota 2 window state and show/hide the GUI
        self.dota_window_thread = Thread(target=self.check_dota_window_state)
        self.dota_window_thread.start()
        
    def close_application(self, event=None):
        self.tray_thread.stop()  # Stop the tray icon
        os._exit(0)

    def update_message(self, message):
        self.message_label.config(text=message)

    def look_for_match(self):
        self.update_message("Ready to Accept Matches")
        while True:
            dota2_window = win32gui.FindWindow(None, "Dota 2")
            if dota2_window != 0 and win32gui.IsWindowVisible(dota2_window) and not win32gui.IsIconic(dota2_window):
                accept_coords = self.locate_accept_button()

                if accept_coords is not None:
                    pyautogui.click(accept_coords[0], accept_coords[1])
                    self.update_message("Match Accepted!")

                    time.sleep(3)  # Add a 3-second delay

                    self.update_message("Ready to Accept Matches")  # Reset status message

    def locate_accept_button(self):
        accept_location = pyautogui.locateCenterOnScreen(self.accept_image, grayscale=True, confidence=0.8)
        return accept_location
    
    def check_dota_window_state(self):
        while True:
            dota2_window = win32gui.FindWindow(None, "Dota 2")
            if dota2_window != 0 and win32gui.IsWindowVisible(dota2_window) and not win32gui.IsIconic(dota2_window):
                self.root.deiconify()  # Show the GUI
            else:
                self.root.withdraw()  # Hide the GUI
            time.sleep(1)  # Check every second

# Set working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

root = tk.Tk()
root.configure(bg="#171d25")
root.attributes('-alpha', 0.85)
app = Dota2QueueGUI(root)
# Calculate screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the desired position for top left corner
desired_x = 0  # Adjust this value as needed
desired_y = 0  # Adjust this value as needed

# Set the geometry and position of the window
root.geometry(f"300x100+{desired_x}+{desired_y}")
root.overrideredirect(True)  # Remove window decorations (title bar, borders, etc.)
root.wm_attributes("-topmost", True)  # Keep the window on top
root.wm_attributes("-disabled", True)  # Disable interactions

root.mainloop()

import os
import pyautogui
import pystray
import tkinter as tk
from tkinter import ttk
import threading
import time
import win32gui
import base64
from io import BytesIO
from PIL import Image
import keyboard
from constants import TRAY_ICON_BASE64, BUTTON_ACCEPT_BASE64

class TrayIconThread(threading.Thread):
    def __init__(self, image, menu):
        super().__init__()
        self.icon = pystray.Icon("Auto Accept", image, "Auto Accept", menu)

    def run(self):
        self.icon.run()

    def stop(self):
        self.icon.stop()

class Dota2QueueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Accept")

        image = Image.open(BytesIO(base64.b64decode(TRAY_ICON_BASE64)))
        menu = (pystray.MenuItem('Exit', self.close_application),)
        self.tray_thread = TrayIconThread(image, menu)
        self.tray_thread.start()

        keyboard.add_hotkey('ctrl+x', self.close_application)
        self.accept_image = Image.open(BytesIO(base64.b64decode(BUTTON_ACCEPT_BASE64)))

        self.root.configure(bg="#171d25")
        self.message_label = ttk.Label(self.root, text="", font=("Proxima Nova ExCn Rg", 16), anchor="center", background="#171d25", foreground="white")
        self.message_label.pack(fill="both", expand=True)
        self.close_label_bg = tk.Label(self.root, background="#2b2b2b")
        self.close_label_bg.pack(fill="both", expand=True)
        self.close_label = ttk.Label(self.close_label_bg, text="Ctrl + X to close", font=("Trajan Pro Bold", 8), anchor="center", background="#0e1218", foreground="#818181")
        self.close_label.pack(fill="both", expand=True)

        # Update the message label here with the initial message
        self.update_message("Ready to Accept Matches")

        self.queue_thread = threading.Thread(target=self.look_for_match)
        self.queue_thread.start()
        self.root.withdraw()

        self.dota_window_thread = threading.Thread(target=self.check_dota_window_state)
        self.dota_window_thread.start()


    def close_application(self, event=None):
        self.tray_thread.stop()
        os._exit(0)

    def update_message(self, message):
        self.message_label.config(text=message)

    def look_for_match(self):
        while True:
            dota2_window = win32gui.FindWindow(None, "Dota 2")
            if dota2_window and win32gui.IsWindowVisible(dota2_window) and not win32gui.IsIconic(dota2_window):
                accept_coords = pyautogui.locateCenterOnScreen(self.accept_image, grayscale=True, confidence=0.8)
                if accept_coords:
                    pyautogui.click(*accept_coords)
                    self.update_message("Match Accepted!")
                    time.sleep(3)
                    self.update_message("Ready to Accept Matches")

    def check_dota_window_state(self):
        while True:
            dota2_window = win32gui.FindWindow(None, "Dota 2")
            self.root.deiconify() if dota2_window and win32gui.IsWindowVisible(dota2_window) and not win32gui.IsIconic(dota2_window) else self.root.withdraw()
            time.sleep(1)

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

root = tk.Tk()
root.configure(bg="#171d25")
root.attributes('-alpha', 0.85)
app = Dota2QueueGUI(root)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
desired_x, desired_y = 0, 0
root.geometry(f"300x100+{desired_x}+{desired_y}")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.mainloop()

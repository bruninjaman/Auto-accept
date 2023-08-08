import os
import pyautogui
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import win32gui

class Dota2QueueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Accept")

        self.root.configure(bg="#171d25")  # Set the background color of the root window

        self.message_label = ttk.Label(self.root, text="", font=("Proxima Nova ExCn Rg", 16), anchor="center", background="#171d25", foreground="white")
        self.message_label.pack(fill="both", expand=True)  # Center both horizontally and vertically

        self.queue_thread = Thread(target=self.look_for_match)
        self.queue_thread.start()

        self.root.withdraw()  # Hide the GUI initially

        # Start a thread to continuously check the Dota 2 window state and show/hide the GUI
        self.dota_window_thread = Thread(target=self.check_dota_window_state)
        self.dota_window_thread.start()

    def update_message(self, message):
        self.message_label.config(text=message)

    def look_for_match(self):
        self.update_message("Waiting for Dota 2 queue to find a match")
        while True:
            dota2_window = win32gui.FindWindow(None, "Dota 2")
            if dota2_window != 0 and win32gui.IsWindowVisible(dota2_window) and not win32gui.IsIconic(dota2_window):
                accept = pyautogui.locateCenterOnScreen('./img/accept.png')

                if accept is not None:
                    pyautogui.click(accept[0], accept[1])
                    self.update_message("Match Accepted!")

                    time.sleep(3)  # Add a 3-second delay

                    self.update_message("Waiting for Dota 2 queue to find a match")  # Reset status message

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
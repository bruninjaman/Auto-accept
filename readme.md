[![Forks][forks-shield]][https://github.com/superoo7/dota2-auto-accept]>

<!-- ABOUT THE PROJECT -->
## About The Project

This is a dota 2 python script to auto-accept matches. So you can leave your computer for a second and go drink some water.

### Built With

This is script is built with python with many libraries like
pyautogui, tkinter, threading, time, win32gui..

<!-- GETTING STARTED -->
## Getting Started

1. Install Python: If you don't have Python installed, download and install Python from the official website (https://www.python.org/downloads/). Choose the appropriate version for your operating system.

2. Install Required Libraries: Open a terminal/command prompt and use the following commands to install the required libraries:

```
pip install pyautogui
pip install pywin32

```

3. Run the Script: Open a terminal/command prompt, navigate to the directory where you saved the Python file, and run the script using the following command:
```
python main.py
```

4. Dota 2 and Script Interaction: The script will monitor the Dota 2 window state and automatically accept a match when it finds the "Accept" button. The GUI window created by the script will also be displayed when Dota 2 is active.

### Aditional solution

If your script can't find the image due to your language or screen resolution, you will need to change the image "./img/accept.png". Take a screenshot of your accept button and cut it and replace the image with same name.

### Prerequisites

Python, libraries(imports) also you will need Accept.png that matches your resolution.
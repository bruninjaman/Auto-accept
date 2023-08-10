[![Forks][forks-shield]][https://github.com/superoo7/dota2-auto-accept]>

<!-- ABOUT THE PROJECT -->
## About The Project

This is a dota 2 python script to auto-accept matches. So you can leave your computer for a second and go drink some water.

<!-- GETTING STARTED -->
## Getting Started

1. Install Python: If you don't have Python installed, download and install Python from the official website (https://www.python.org/downloads/). Choose the appropriate version for your operating system.

2. Install Required Libraries: Open a terminal/command prompt and use the following commands to install the required libraries:

```
pip install pyautogui
pip install pywin32
pip install opencv-python
```

3. Run the Script: Open a terminal/command prompt, navigate to the directory where you saved the Python file, and run the script using the following command:
```
python main.py
```

4. Dota 2 and Script Interaction: The script will monitor the Dota 2 window state and automatically accept a match when it finds the "Accept" button. The GUI window created by the script will also be displayed when Dota 2 is active.

### Aditional solution

If your script can't find the image due to your language or screen resolution, you will need to change the base64 encoded image.

### Prerequisites

Python, libraries(imports)...


### How to build it

1. navigate to script directory on command prompt

2. Use the code:
```pyinstaller --onefile --noconsole main.py```


(it gives errors due to dll imports at the moment)
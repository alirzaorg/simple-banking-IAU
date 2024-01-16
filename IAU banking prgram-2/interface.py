import os
import time


def clean_terminal_screen():
    """
   دستور:.
   cls
   برای پاک کردن ترمینال در ویندوز
    """

    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(0.2)

def display_horizontal_line():

    print("───────────────────────────────────────────────────────────────")

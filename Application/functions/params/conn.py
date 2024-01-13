import os
import sys
import subprocess

import tkinter as tk

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(parent_dir)

from config.Variables.variables import *

class BashLikeCanvas(tk.Canvas):
    def __init__(self, parent, width: int = 1140, height: int = 300):
        super().__init__(parent, width=width, height=height, bg="black", highlightthickness=2, highlightbackground="gray")
        self.config(bg='black')  # Set background to black
        self.mysql_status()

    def mysql_status(self) -> str:
        """Renvoie l'état de la connexion MySQL"""
        try:
            result = subprocess.run(["systemctl", "status", "mysql"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
        except Exception as e:
            output = f"Erreur : {e}"

        x, y = 10, 10  # Starting position
        print(output)
        for line in output.split("\n"):
            self.create_text(x, y, anchor='nw', text=line, fill="white", font=('Courier', 12))
            y += 20  # Move to the next line
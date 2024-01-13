import os
import sys

import tkinter as tk

from tkinter import font
from tkinter import PhotoImage
from functions.menu import MenuPrincipal
from functions.params.conn import BashLikeCanvas

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config.Variables.variables import *


# Fenêtre principale
root = tk.Tk()
root.title("Babel Onche")
icon = PhotoImage(file=f"{GLOBAL_PATH}Application/utils/icons/App.png")
root.iconphoto(True, icon)
root.geometry("1280x800")

# ------

root.config(menu=MenuPrincipal(root))
canvas = BashLikeCanvas(root)
canvas.pack(expand=True)
canvas.place(x=60, y=60)

# ------

root.mainloop()
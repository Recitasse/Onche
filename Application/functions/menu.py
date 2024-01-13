import os
import sys

import tkinter as tk

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

from config.Variables.variables import *

import tkinter as tk
from tkinter import messagebox, font

class MenuPrincipal(tk.Menu):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self._text_color = "#232323"
        self._bg_in_color = "#f5f6ff"
        self._bg_hover_color = "#ebebeb"
        self._font = font.Font(family="Arial", size=14, weight="bold")

        self.config(bg=self._bg_in_color, fg=self._text_color, font=self._font)
        self.create_file_menu()
        self.create_commu_menu()
        self.outils_menu()

    def menu_label(self, label: str, width: int = 25):
        return f" {label}".ljust(width)

    def create_file_menu(self):
        file_menu = tk.Menu(self, tearoff=0, bg=self._bg_in_color, fg=self._text_color, font=self._font, activebackground=self._bg_hover_color)
        file_menu.add_command(label="Visiter")
        file_menu.add_command(label="Query predéfinies")
        file_menu.add_separator()
        file_menu.add_command(label="Entrée manuelle", command=self.master.quit)
        self.add_cascade(label=self.menu_label("Queries"), menu=file_menu)

    def create_commu_menu(self):
        commu_menu = tk.Menu(self, tearoff=0, bg=self._bg_in_color, fg=self._text_color, font=self._font, activebackground=self._bg_hover_color)
        commu_menu.add_command(label="Communautés")

        # topic
        topic_menu = tk.Menu(self, tearoff=0, bg=self._bg_in_color, fg=self._text_color, font=self._font, activebackground=self._bg_hover_color)
        topic_menu.add_command(label="Boucle")
        topic_menu.add_command(label="Intéressant (beta)")

        # onchois
        onchois_menu = tk.Menu(self, tearoff=0, bg=self._bg_in_color, fg=self._text_color, font=self._font, activebackground=self._bg_hover_color)
        onchois_menu.add_command(label="Recherche")
        onchois_menu.add_command(label="Par sujet (beta)")
        onchois_menu.add_command(label="Constellation")

        # communautés
        com_menu = tk.Menu(self, tearoff=0, bg=self._bg_in_color, fg=self._text_color, font=self._font, activebackground=self._bg_hover_color)
        com_menu.add_command(label="Découvrir")
        com_menu.add_command(label="Depuis REGEXP")
        com_menu.add_command(label="Expension (beta)")

        # menu
        commu_menu.add_command(label="Badges")
        commu_menu.add_cascade(label="Topics", menu=topic_menu)
        commu_menu.add_cascade(label="Onchois", menu=onchois_menu)

        self.add_cascade(label=self.menu_label("Éléments"), menu=commu_menu)

    def outils_menu(self):
        options_menu = tk.Menu(self, tearoff=0, bg=self._bg_in_color, fg=self._text_color, font=self._font, activebackground=self._bg_hover_color)
        options_menu.add_command(label=self.menu_label("Interface"))
        options_menu.add_command(label=self.menu_label("Connexion"))
        options_menu.add_separator()
        options_menu.add_command(label=self.menu_label("Informations"))

        self.add_cascade(label=self.menu_label("Paramètres"), menu=options_menu)


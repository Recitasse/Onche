import datetime
import threading
import os
import sys


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from webscrapper.onche_scrapper import ScrapperOnche
from config.Variables.variables import *

# ----------------------------------------------

if __name__ == "__main__":

    Inst_gen = ScrapperOnche(1)

    it = 1
    while True:
        try:
            Inst_gen.add_to_bdd_page(it)
        except Exception as e:
            print(e)
        print(it)
        it += 1
        
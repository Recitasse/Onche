import threading
import os
import sys


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from webscrapper.onche_scrapper import ScrapperOnche
from config.Variables.variables import *

# ----------------------------------------------

def add_to_bdd_thread(instance, page_number):
    try:
        instance.add_to_bdd_page(page_number)
    except Exception as e:
        print(f"Error on instance {instance}: {e}")

if __name__ == "__main__":

    """Inst_blabla = ScrapperOnche(1, BOT_agent=MYSQL_BOT_BLABLA)
    Inst_sugg = ScrapperOnche(2, BOT_agent=MYSQL_BOT_SUGG)
    Inst_pron = ScrapperOnche(3, BOT_agent=MYSQL_BOT_PRON)
    Inst_goulag = ScrapperOnche(4, BOT_agent=MYSQL_BOT_GOULAG)
    #Inst_anciens = ScrapperOnche(5, BOT_agent=MYSQL_BOT_ANCIENS)
    #Inst_mode = ScrapperOnche(6, BOT_agent=MYSQL_BOT_MODE)
    Inst_crypto = ScrapperOnche(7, BOT_agent=MYSQL_BOT_CRYPTO)
    Inst_jv = ScrapperOnche(8, BOT_agent=MYSQL_BOT_JV)
    Inst_auto = ScrapperOnche(9, BOT_agent=MYSQL_BOT_AUTO)"""

    Inst_blabla = ScrapperOnche(1, BOT_agent=MYSQL_USER)
    Inst_sugg = ScrapperOnche(2, BOT_agent=MYSQL_USER)
    Inst_pron = ScrapperOnche(3, BOT_agent=MYSQL_USER)
    Inst_goulag = ScrapperOnche(4, BOT_agent=MYSQL_USER)
    #Inst_anciens = ScrapperOnche(5, BOT_agent=MYSQL_BOT_ANCIENS)
    #Inst_mode = ScrapperOnche(6, BOT_agent=MYSQL_BOT_MODE)
    Inst_crypto = ScrapperOnche(7, BOT_agent=MYSQL_USER)
    Inst_jv = ScrapperOnche(8, BOT_agent=MYSQL_USER)
    Inst_auto = ScrapperOnche(9, BOT_agent=MYSQL_USER)

    ALL = {Inst_blabla, Inst_sugg, Inst_pron, Inst_goulag, Inst_crypto, Inst_jv, Inst_auto}
    ALL  = {Inst_blabla}

    it = 1
    while True:
        threads = []
        for instance in ALL:
            thread = threading.Thread(target=add_to_bdd_thread, args=(instance, it))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        it += 1
        
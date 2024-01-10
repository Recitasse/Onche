import os
import sys

from preparation_FONC import congruence_topic

parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(parent)

from config.Variables.variables import *

liste_mot = [" Retou ", " retou ", " RETOU "]
nb_jour = 365
mes_seuil = 2
nom="Retou"
title=f"Relation {nom}"
k=5
alp_p=[1.5, 1]
size_font=[5, 35, 5]
coef = [2, 6, 0.17]

if not os.path.exists(f"{GLOBAL_PATH}/OncheSTUD/communautes/Sujet/{nom}"):
    os.mkdir(f"{GLOBAL_PATH}/OncheSTUD/communautes/Sujet/{nom}")

congruence_topic(nb_jour,mes_seuil, liste_mot, nom, title, k, alp_p, size_font, coef, 130, 3)

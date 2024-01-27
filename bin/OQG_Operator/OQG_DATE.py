import datetime

from config.Variables.variables import *
from BDD.bdd import BDD

def ADD_TIME_TO_DATE(date: datetime, interval: int, unit: str = 'DAY') -> datetime:
    """"Ajoute une valeur de temps (interval) à une date"""
    try:
        bdd_tmp = BDD()
        query='SELECT ADDDATE(%s, INTERVAL %s '+unit+');'
        return bdd_tmp.get_results(query, params=(date, interval,))
    except Exception as e:
        print(e)
    return None

print(f"Ajout de 5 jours : {ADD_TIME_TO_DATE(datetime.datetime(2024, 1, 1), 5)}")
print(f"Ajout de 5 mois : {ADD_TIME_TO_DATE(datetime.datetime(2024, 1, 1), 5, 'MONTH')}")
print(f"Erreur : {ADD_TIME_TO_DATE(datetime.datetime(2024, 1, 1), 5, 'NIMP')}")

def ADD_TIME(date1: datetime, date2: datetime) -> datetime:
    """"Aoute une date à une date"""
    try:
        bdd_tmp = BDD()
        query='SELECT ADDTIME(%s, %s);'
        return bdd_tmp.get_results(query, params=(date1, date2,))
    except Exception as e:
        print(e)
    return None

def CONVERT_TIME_ZONE(date: datetime, original_timezone: str, final_timezone: str) -> datetime:
    """"Convertir une date dans zone temporelle à une autre"""
    try:
        bdd_tmp = BDD()
        query='SELECT CONVERT_TZ(%s, %s, %s);'
        return bdd_tmp.get_results(query, params=(date, original_timezone, final_timezone,))
    except Exception as e:
        print(e)
    return None

def CURRENT_DATE() -> datetime:
    """"Retourne la date actuelle (la date, pas l'horraire !)"""
    try:
        bdd_tmp = BDD()
        query='SELECT CURDATE();'
        return bdd_tmp.get_results(query)
    except Exception as e:
        print(e)
    return None

def CURRENT_TIME() -> datetime:
    """"Retourne l'horraire actuelle (l'horraire, pas la date !)"""
    try:
        bdd_tmp = BDD()
        query='SELECT CURTIME();'
        return bdd_tmp.get_results(query)
    except Exception as e:
        print(e)
    return None


import datetime

from config.variables import *
from BDD.bdd import BDD

def ADD_TIME_TO_DATE(date: datetime, interval: int, unit: str = 'DAY') -> datetime:
	"""Ajoute une valeur de temps (interval) à une date"""
	if unit not in ('MICROSECOND', 'SECOND', 'MINUTE', 'HOUR', 'DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'):
		print("Erreur, unit doit être l'une de ces valeurs : ('MICROSECOND', 'SECOND', 'MINUTE', 'HOUR', 'DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR').")
	try:
		bdd_tmp = BDD()
		query='SELECT ADDDATE(%s, INTERVAL %s '+unit+');'
		return bdd_tmp.get_results(query, params=(date, interval,))
	except Exception as e:
		print(e)
	return None

def ADD_TIME(date1: datetime, date2: datetime) -> datetime:
	"""Aoute une date à une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT ADDTIME(%s, %s);'
		return bdd_tmp.get_results(query, params=(date1, date2,))
	except Exception as e:
		print(e)
	return None

def CONVERT_TIME_ZONE(date: datetime, original_timezone: str, final_timezone: str) -> datetime:
	"""Convertir une date dans zone temporelle à une autre"""
	try:
		bdd_tmp = BDD()
		query='SELECT CONVERT_TZ(%s, %s, %s);'
		return bdd_tmp.get_results(query, params=(date, original_timezone, final_timezone,))
	except Exception as e:
		print(e)
	return None

def CURRENT_DATE() -> datetime:
	"""Retourne la date actuelle (la date, pas l'horraire !)"""
	try:
		bdd_tmp = BDD()
		query='SELECT CURDATE();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def CURRENT_TIME() -> datetime:
	"""Retourne l'horraire actuelle (l'horraire, pas la date !)"""
	try:
		bdd_tmp = BDD()
		query='SELECT CURTIME();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def CURRENT_TIMESTAMP() -> datetime:
	"""Retourne l'heure actuelle"""
	try:
		bdd_tmp = BDD()
		query='SELECT CURRENT_TIMESTAMP();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def SUBSTRACT_TIME(temps1: datetime, temps2: datetime) -> datetime:
	"""Soustrait un temps"""
	try:
		bdd_tmp = BDD()
		query='SELECT SUBTIME(%s, %s);'
		return bdd_tmp.get_results(query, params=(temps1, temps2,))
	except Exception as e:
		print(e)
	return None

def SUBSTRACT_TIME(date1: datetime, date2: datetime) -> datetime:
	"""Soustrait une date à une autre"""
	try:
		bdd_tmp = BDD()
		query='SELECT DATEDIFF(%s, %s);'
		return bdd_tmp.get_results(query, params=(date1, date2,))
	except Exception as e:
		print(e)
	return None

def SEC_TO_TIME() -> datetime:
	"""convertit les seconds en temps"""
	try:
		bdd_tmp = BDD()
		query='SELECT SEC_TO_TIME();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def SEC_TO_DATE() -> datetime:
	"""convertit un string en date"""
	try:
		bdd_tmp = BDD()
		query='SELECT SEC_TO_DATE();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def TO_DAYS() -> int:
	"""retourne le nombre de jour d'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT TO_DAYS();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def TO_SECONDS() -> int:
	"""retourne le nombre de secondes d'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT TO_SECONDS();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def GET_MINUTE() -> int:
	"""retourne la minute 'd'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT MINUTE();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def GET_HOUR() -> int:
	"""retourne l'heure 'd'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT HOUR();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def GET_DAY() -> int:
	"""retourne le jour d'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT DAY();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def GET_WEEK() -> int:
	"""retourne la semaine d'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT WEEK();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def GET_MONTH() -> int:
	"""retourne le mois d'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT MONTH();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def GET_QUARTER() -> int:
	"""retourne le semestre d'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT QUARTER();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None

def GET_YEAR() -> int:
	"""retourne l'année' d'une date"""
	try:
		bdd_tmp = BDD()
		query='SELECT YEAR();'
		return bdd_tmp.get_results(query)
	except Exception as e:
		print(e)
	return None


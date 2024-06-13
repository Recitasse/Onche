from BDD.bdd import BDD

def LIKE(text: str, paterne: str, escape: str = '') -> bool:
	"""Indique si un string contient un patterne"""
	try:
		bdd_tmp = BDD()
		query='SELECT %s LIKE "'+paterne+'" ESCAPE "'+escape+'";'
		return bdd_tmp.get_results(query, params=(text,))
	except Exception as e:
		print(e)
	return None

def NOT_LIKE(text: str, paterne: str, escape: str = '') -> bool:
	"""Indique si un string ne contient pas un patterne"""
	try:
		bdd_tmp = BDD()
		query='SELECT %s LIKE "'+paterne+'" ESCAPE "'+escape+'";'
		return bdd_tmp.get_results(query, params=(text,))
	except Exception as e:
		print(e)
	return None

def STRING_COMPARE(text1: str, text2: str) -> bool:
	"""Compare 2 string et renvoie vrai si les 2 strings sont identiques"""
	try:
		bdd_tmp = BDD()
		query='SELECT STRCMP(%s, %s);'
		return bdd_tmp.get_results(query, params=(text1, text2,))
	except Exception as e:
		print(e)
	return None

def IN_REGEXP(text1: str, paterne: str) -> bool:
	"""Renvoie vraie si contient le paterne dans le regexp"""
	try:
		bdd_tmp = BDD()
		query='SELECT %s REGEXP '+paterne+';'
		return bdd_tmp.get_results(query, params=(text1,))
	except Exception as e:
		print(e)
	return None

def NOT_IN_REGEXP(text1: str, paterne: str) -> bool:
	"""Renvoie vraie si ne contient pas le paterne dans le regexp"""
	try:
		bdd_tmp = BDD()
		query='SELECT %s NOT REGEXP '+paterne+';'
		return bdd_tmp.get_results(query, params=(text1,))
	except Exception as e:
		print(e)
	return None

def IN_REGEXP_INSTR(text1: str, paterne: str, occurence: int = 1) -> bool:
	"""Renvoie vraie si ne contient pas le paterne dans le regexp_instr"""
	try:
		bdd_tmp = BDD()
		query='SELECT REGEXP_INSTR(%s, %s, %s);'
		return bdd_tmp.get_results(query, params=(text1, paterne, occurence,))
	except Exception as e:
		print(e)
	return None

def IN_REGEXP_LIKE(text1: str, paterne: str, match_type: str = 'c') -> bool:
	"""Renvoie vraie si contient le paterne dans le regexp_like"""
	if match_type not in ('c', 'i', 'm', 'n', 'u'):
		print("Erreur, match_type doit être l'une de ces valeurs : ('c', 'i', 'm', 'n', 'u').")
	try:
		bdd_tmp = BDD()
		query='SELECT REGEXP_LIKE(%s, %s, %s);'
		return bdd_tmp.get_results(query, params=(text1, paterne, match_type,))
	except Exception as e:
		print(e)
	return None


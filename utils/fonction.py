import datetime

import xml.etree.ElementTree as ET

from config.Variables.variables import *

def conversion(el:str) -> int:
    """
    Conversion d'un string en un temps

    Args: 
        el (string):
    
    Exemple:
        '14j', '25s', '78h', '45j'
    """
    if 'h' in el:
        hours, rest = el.split('h')
        seconds = int(hours) * 60 * 60
    elif 'j' in el:
        days, rest = el.split('j')
        seconds = int(days) * 24 * 60 * 60
    elif 'mois' in el:
        months, rest = el.split(' mois')
        seconds = int(months) * 30 * 24 * 60 * 60
    elif 'm' in el:
        minutes, rest = el.split('m')
        seconds = int(minutes) * 60
    elif 's' in el:
        seconds, rest = el.split('s')
    else:
        seconds = 0     # Erreur
    return int(seconds)


def timedelta(delais:str="365j") -> datetime:
    """
    Obtention du délais via un string.

    Args:
        delais (string): nombre+unité
    
    Exemple:
        14m -> pour 14 minutes,
        25h -> pour 25h,
        20  -> pour 20s,
    
    Unité:
        '' : second,
        'm': minute,
        'h': heure,
        'j': jour,

    Returns:
        delais (datetime), délais.
    """
    #Transformation en liste de l'entrée
    delais = conversion(delais)
    target_date = datetime.datetime.now() - datetime.timedelta(seconds=delais)

    return target_date

def forum_xml(inf: str | int) -> dict:
    """Renvoie les éléments du forums dans le XML"""
    tree = ET.parse(FORUM_XML)
    root = tree.getroot()
    if isinstance(inf, int):
        type_ = "id"
    if isinstance(inf, str):
        type_ = "name"

    for forum in root.findall('forum'):
        if str(inf) and forum.get(type_) == str(inf):
            forum_details = {attr: forum.get(attr) for attr in forum.keys()}
            topics = [topic.text for topic in forum.find('topics').findall('topic')]
            forum_details['topics'] = topics
            forum_details['profile'] = {"need": eval(forum.find("profile").text), "profile": forum.get("json_link")}
            forum_details['name'] = '-'.join(forum_details['name'].split())
            return forum_details

def create_url(forum: dict, page: int) -> str:
    """Renvoie l'url du forum ciblé (depuis la fonction forum_xml)"""
    if page <= 0:
        raise ValueError("La page ne peut pas être inférieur ou égale à 0.")
    return f"https://onche.org/forum/{forum['id']}/{forum['name']}/{page}"

def change_value_variables(variable: str, value: str) -> False:
    """Change la valeur d'une variable globale"""
    with open(f"{GLOBAL_PATH}config/Variables/variables.py", "r", encoding="utf-8") as verif:
        text = verif.read().split("\n")
    _ret = ""
    for line in text:
        if line.find(variable) > -1:
            _ret = line
            break
    if _ret == "":
        return False
    
    with open(f"{GLOBAL_PATH}config/Variables/variables.py", 'w') as file:
        file.writelines('\n'.join(text).replace(line, f'MYSQL_DATABASE = "{value}"'))
    return True

import os
import sys
import subprocess

from flask import Flask, jsonify, Blueprint
from random import randint

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

from config.Variables.variables import *
from BDD.bdd import BDD

def get_mysql_base():
    """Renvoie l'état de la connexion mysql"""
    try:
        result = subprocess.run(["systemctl", "status", "mysql"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
    except Exception as e:
        output = f"Erreur : {e}"
    return output.split("\n")

def get_mysql_parameter():
    """Renvoie les paramètres de la base de donnée actuellement"""
    date = DDB.split("_")[-1].split(".")[0][:8]
    str_date = date[5:7]+"/"+date[4:6]+"/"+date[:4]
    return {"user": f"User : {MYSQL_USER}", "host": f"Host : {MYSQL_HOST}" if len(MYSQL_HOST)>0 else "Host : 127.0.0.1", "database": f"Database : {MYSQL_DATABASE}", "size": f"Size : {BDD(database=MYSQL_DATABASE).size()} Mo", "date": f"Date : {str_date}"}

def get_version_variables():
    """Renvoie les variables d'état du sytème"""
    date = DDB.split("_")[-1].split(".")[0][:8]
    str_date = date[5:7]+"/"+date[4:6]+"/"+date[:4]
    bdd = DDB.split("_")[1]
    return {"version": VERSION, "Créateur": CREATEUR, "BDD": bdd,"DATE": str_date}

import os
import subprocess
import inspect

from mysql.connector import connect as connect_server
from datetime import datetime

from config.Variables.variables import *
from utils.logger import logger


class Link:
    def __init__(self, user: str = MYSQL_USER, host: str = MYSQL_HOST,
                 mdp: str = MYSQL_PASSWORD, database: str = MYSQL_DATABASE, verbose: bool = False) -> None:

        # public
        self.user = user
        self.host = host
        self.database = database
        self.badgeList = []

        # private
        self._verbose = verbose
        self._mdp = mdp
        self._logger = logger(PATH_BDD_LOG, "BDD", self._verbose)

        # connexion
        try:
            self.connexion = connect_server(user=self.user, host=self.host,
                                            password=self._mdp, database=self.database,
                                            auth_plugin="mysql_native_password")
            self._logger.info("Connexion à la base de donnée réussie.")
        except Exception as e:
            self._logger.error(f"Echec de la connexion à la base de donnée : {e}")
            raise Exception(f"Echec de la connexion à la base de donnée : {e}")

    @property
    def size(self):
        """Renvoie la taille de la base de donnée """
        query = "SELECT SUM(data_length + index_length) / 1024 / 1024 'Database Size in MB' FROM information_schema.tables WHERE table_schema = %s;"
        try:
            return self.get_results(query, params=(MYSQL_DATABASE,))
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}.")
        return 0

    @property
    def bdd(self) -> dict:
        return {'user': self.user, 'mdp': self._mdp, 'bdd': self.database, 'host': self.host}

    @bdd.setter
    def bdd(self, database: str, user: str = MYSQL_USER, host: str = MYSQL_HOST, pass_: str = MYSQL_PASSWORD):
        """Change de base de donnée

        Args:
            database (str): Nouveau nom de la base de donnée
        """
        self.user = user
        self.host = host
        self._mdp = pass_
        try:
            self.connexion = connect_server(user=self.user, host=self.host,
                                            password=self._mdp, database=database,
                                            auth_plugin="mysql_native_password")
            self._logger.info(f"Connexion à la base de donnée {database} réussie.")
            self.database = database
        except Exception as e:
            self._logger.error(f"Echec de la connexion à la base de donnée {database} : {e}")
            raise Exception(f"Echec de la connexion à la base de donnée {database} : {e}")

    def exporter_bdd(self) -> None:
        """Exporte les éléments de la table SQL choisie au format sql"""
        date = datetime.now().strftime("%d_%m_%Y")
        backup_path = GLOBAL_PATH+"BDD/export/bdd_"
        if "bdd_" in os.listdir(GLOBAL_PATH+"BDD/export/"):
            os.remove(os.path.join(backup_path, f"bdd_{date}.sql"))
        try:
            subprocess.run(f"mysqldump -u{MYSQL_USER} -p{MYSQL_PASSWORD} {self.database} > '{backup_path}{self.database}.sql'", shell=True, check=True)
            self._logger.info(f"Base de donnée {self.database} exportée : {backup_path}{self.database}.sql")
        except subprocess.CalledProcessError as e:
            self._logger.error(f"Impossible d'exporter la base de donnée {self.database} : {e}")
            raise subprocess.CalledProcessError(f"Impossible d'exporter la base de donnée {self.database} : {e}")

    def QUERY(self, query: str, values: tuple = None):
        """
        Permet d'éxécuter n'importe quelle query

        Args:
            query (string) : La commande sql
            values (a,b,c,) : Les values de la commande (mysql format)
        """
        cond = True
        cursor = self.connexion.cursor()
        res = None
        if len(values) == 0:
            cond = False
        try:
            if cond:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query, params=values)
                res = cursor.fetchall()
            if res and res[0]:
                return [item.decode('utf-8') if isinstance(item, (bytearray, bytes)) else item for item in res[0]]
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}.")
        return []

    def get_results(self, query: str, params: tuple = None, ind_=0):
        """Renvoie les résultats d'une query

        Args:
            query (str): la query sql
            ind_ (int, optional): l'indice à récupérer. Defaults to 0.

        Raises:
            ValueError: l'indice donné est invalide
            ValueError: la base de donnée n'a pas donnée de réponse

        Returns:
            (Any): retourne le résultat d'une query
        """

        cursor = self.connexion.cursor()
        try:
            if params:
                cursor.execute(query, params=params)
            else:
                cursor.execute(query)
            resultats = cursor.fetchall()
        except Exception as e:
            self._logger.error(e)
            raise ValueError(e)
        finally:
            cursor.close()

        if isinstance(ind_, str):
            vals = []
            if ind_ == "all":
                for value in resultats:
                    if len(value) > 1:
                        if inspect.currentframe().f_back.f_code.co_name == "get_table_info":
                            vals.append(list(value))
                        else:
                            tmp_ = [val for val in value]
                            vals.append(tmp_)
                    else:
                        vals = [value[0] for value in resultats]
                return tuple(vals)
            else:
                self._logger.warning("La l'indice demandé est erroné, indice 0 par défaut.")
                ind_ = 0
        elif isinstance(ind_, int):
            if ind_ == 0:
                if resultats:
                    return resultats[0][0]
                return []
            elif ind_ > 0:
                vals = [value[0] for value in resultats]
                return vals[0][ind_]
        else:
            self._logger.error("Impossible de demander un indice autre qu'un entier ou exceptionnellement 'all'.")
            raise ValueError(f"Impossible de récupérer l'indice {ind_} du résultat de la requête select.")

import os
import sys
import subprocess

from datetime import datetime
from pathlib import Path

from mysql.connector import connect

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config.Variables.variables import *
from utils.logger import logger

class BDD:
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
            self.connexion = connect(user=self.user, host=self.host,
                                            password=self._mdp, database=self.database,
                                            auth_plugin="mysql_native_password")
            self._logger.info("Connexion à la base de donnée réussie.")
        except Exception as e:
            self._logger.error(f"Echec de la connexion à la base de donnée : {e}")
            raise Exception(f"Echec de la connexion à la base de donnée : {e}")

    # Utils methods
        
    def size(self):
        """Renvoie la taille de la base de donnée """
        query = f"SELECT table_schema 'Database Name', SUM(data_length + index_length) / 1024 / 1024 'Database Size in MB' FROM information_schema.tables WHERE table_schema = '{MYSQL_DATABASE}';"
        try:
            return self.get_results(query)
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}.")

    def change_bdd(self, database: str):
        """Change de base de donnée

        Args:
            database (str): Nouveau nom de la base de donnée
        """
        try:
            self.connexion = connect(user=self.user, host=self.host,
                                            password=self._mdp, database=database,
                                            auth_plugin="mysql_native_password")
            self._logger.info(f"Connexion à la base de donnée {database} réussie.")
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
        
    def import_table(self, path: str) -> None:
        """Importe les tables sélectionnées

        Args:
            path (str): path du fichier (au format sql)

        Raises:
            FileNotFoundError: Le fichier n'existe pas ou son path est invalide
            Exception: L'import côté sql a échoué
        """

        if not (path.endswith(".sql")) and not os.path.exists(path):
            self._logger.error(f"Le fichier {path} n'est pas valide ou n'existe pas.")
            raise FileNotFoundError(f"Le fichier {path} n'est pas valide ou n'existe pas.")

        try:
            subprocess.run(f"mysql -u{MYSQL_USER} -p{MYSQL_PASSWORD} {self.database} < {path}.sql", shell=True)
            self._logger.info(f"Table importée : {path}")
        except subprocess.CalledProcessError as e:
            self._logger.info(f"mysql -u{MYSQL_USER} -p{MYSQL_PASSWORD} {self.database} < {path}.sql")
            self._logger.error(f"Impossible d'importer la base de donnée {path.split('/')[-1]} : {e}")
            raise Exception(f"Impossible d'importer la base de donnée {path.split('/')[-1]} : {e}")

    def QUERY(self, query: str, values: tuple = None):
        """
        Permet d'éxécuter n'importe quelle query

        Args:
            query (string) : La commande sql
            values (a,b,c,) : Les values de la commande (mysql format)
        """
        cond = True
        cursor = self.connexion.cursor()
        if len(values) == 0:
            cond = False
        try:
            if cond:
                if values:
                    cursor.execute(query,values)
                else:
                    cursor.execute(query, params=values)
                res = cursor.fetchall()
            if res and res[0]:
                return [item.decode('utf-8') if isinstance(item, (bytearray, bytes)) else item for item in res[0]]
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}.")
        return []

    @property
    def outils(self):
        return self.connexion

    # Convert methods

    def user_id2name(self, id_:int) -> str:
        """Convertit l'id en pseudonyme (pour la bdd)"""
        query = "SELECT onchois_nom FROM onchois WHERE onchois_id = %s;"
        params = (id_,)
        return self.get_results(query, params=params)
        
    def user_name2id(self, nom:str) -> int:
        """Convertit le pseudonyme en id (pour la bdd)"""
        query = "SELECT onchois_id FROM onchois WHERE onchois_nom = %s;"
        params = (nom,)
        return self.get_results(query, params=params)
        
    def badge_name2id(self, nom:str):
        """Convertit le nom en id pour le badge (pour la bdd)"""
        query = "SELECT badges_id FROM badges WHERE badges_nom = %s;"
        params = (nom,)
        return self.get_results(query, params=params)

    def badge_id2name(self, nom:str):
        """Convertit l'id en nom pour le badge (pour la bdd)"""
        query = "SELECT badges_nom FROM badges WHERE badges_id = %s;"
        params = (nom,)
        return self.get_results(query, params=params)
    
    def topic_name2id(self, nom:str) -> int:
        """Convertit le topic en nom (pour la bdd)"""
        query = "SELECT id_topic FROM topic WHERE topic_nom = %s;"
        params = (nom,)
        return self.get_results(query, params=params)

    def topic_id2name(self, id_:int) -> str:
        """Convertit l'id du topic en nom"""
        query = "SELECT topic_nom FROM topic WHERE id_topic = %s;"
        params = (id_,)
        return self.get_results(query, params=params)

    def topic_url2name(self, link: str) -> str:
        """Renvoie le nom du topic via son url"""
        query = "SELECT topic_nom FROM topic WHERE topic_lien = %s;"
        params = (link,)
        return self.get_results(query, params=params)
    
    def topic_name2url(self, name: str) -> str:
        """Renvoie le nom du topic via son url"""
        query = "SELECT topic_lien FROM topic WHERE topic_nom = %s;"
        params = (name,)
        return self.get_results(query, params=params)

    # Add methods
        
    def add_user(self, nom:str) -> None:
        """
        Ajoute un Onchois à la base de donnée

        Args:
            nom (string) : Son nom
            qual (float) : sa qualité (5/10 de base)
        """
        # ON vérifie si l'on a pas un id au lieu d'un nom

        # Vérifie si l'utilisateur n'est pas dans la bdd
        if not self.is_user_in_bdd(nom):
            cursor = self.connexion.cursor()
            query = "INSERT INTO onchois (onchois_nom) VALUES (%s);"
            try:
                cursor.execute(query, (nom,))
                self.connexion.commit()
                self._logger.info(f"Ajout de l'onchois : '{nom}'")
            except Exception as e:
                self._logger.error(f"Une erreur est survenue : {e}.")
            finally:
                cursor.close()

    def add_topic(self, nom:str, user:str, nb:int, lien:str, forum: int) -> None:
        """
        Ajoute un utilisateur dans la base de donnée

        Args:
            nom (string) : titre du topic
            user (string) : nom du créateur
            nb (int) : nombre de message du topic
            lien (string) : lien du topic

        NB: Si l'utilisateur n'a jamais été vu auparavant, son ajout est automatique.

        NB2: Si le topic existe déjà il ne sera pas ajouté
        """
        # Si l'utilisateur n'existe pas il est impossible d'ajouter le topic
        if self.user_name2id(user) == []:
            self._logger.info(f"Ajout de l'utilisateur '{user}' pour insérer le topic : '{nom}'.")
            self.add_user(user)

        if not self.is_topic_in_bdd(lien):
            cursor = self.connexion.cursor()
            query = "INSERT INTO topic (topic_user, topic_nom, topic_message, topic_lien, topic_forum) VALUES (%s, %s, %s, %s, %s);"
            params = (self.user_name2id(user), nom, nb, lien, forum,)
            try:
                cursor.execute(query, params=params)
                self.connexion.commit()
                self._logger(f"Ajout du topic : '{nom}' de '{user}'.")
            except Exception as e:
                self._logger.error(f"Une erreur mysql est survenue : {e}.")
            finally:
                cursor.close()
        else:
            cursor = self.connexion.cursor()
            query = "SELECT topic_message FROM topic WHERE topic_nom = %s;"
            params = (nom,)
            try:
                
                cursor.execute(query, params=params)
                old_mess = self.get_results(query, params=params)
                if old_mess != None:
                    old_mess = old_mess[0]
                else:
                    old_mess = 0
                self._logger.info(f"MAJ du topic : '{nom}'")
            except Exception as e:
                self._logger.error(f"Une erreur mysql est survenue : {e}.")
            finally:
                cursor.close()

            if old_mess!=nb:
                # Si le nombre de message est différent Update
                cursor = self.connexion.cursor()
                query = "UPDATE topic SET topic_message = %s WHERE topic_lien = %s;"
                try:
                    cursor.execute(query, (nb, lien))
                    self.connexion.commit()
                except Exception as e:
                    self._logger.error(f"Une erreur mysql est survenue : {e}.")
                finally:
                    cursor.close()

    def add_badges(self, badge:str) -> None:
        """Ajoute les badges à la BDD

        Args:
            badge (str): nom du badge
        """
        if badge not in self.badgeList:
            query = "INSERT INTO badges (badges_nom) VALUES (%s);"
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, (badge,))
                self.connexion.commit()
                self.badgeList.append(badge)
                self._logger.info(f"Ajout du badge '{badge}'")
            except Exception as e:
                if e.errno == 1062:
                    self._logger.warning(e)
                else:
                    self._logger.error(f"Une erreur est survenue : {e}.")

    def add_badges_users(self, badge:str, nom:str) -> None:
        """
        On ajoute le badge voulu à l'utilisateur

        Args:
            badge (string) : nom du badge
            nom (string) : nom de l'utilisateur

        NB: Si le badge n'existe pas, on l'ajoute à la base de donnée badge
        """
        # On ajoute le badge à la base de donnée si non ajouté
        self.add_badges(badge)
        query = "SELECT ob_badgeid FROM onchois_badges WHERE ob_userid = %s;"
        params = (self.user_name2id(nom),)
        r = []
        try:
            r = self.get_results(query, ind_="all", params=params)
        except Exception as e:
            self._logger.error(f"Une erreur mysql est survenue : {e}.")

        if self.badge_name2id(badge) not in r:
            query = "INSERT INTO onchois_badges (ob_userid, ob_badgeid) VALUES (%s, %s);"
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, (self.user_name2id(nom), self.badge_name2id(badge), ))
                self.connexion.commit()
                self._logger.info(f"\t Ajout du badge '{badge}' à '{nom}'")
            except Exception as e:
                self._logger.error(f"Une erreur est survenue : {e}.")
        else:
            self._logger.info(f"\t '{nom}' possède déjà le badge '{badge}'")

    def add_message(self, user:str, topic:str, msg:str, toUser:str, date:datetime, citation: int) -> None:
        """
        Ajoute un message à la base de donnée

        Args:
            user (string) : Nom de l'utilisateur qui post -> id
            topic (string) : nom du topic sur lequel le message est posté -> id
            msg (string) : le message posté
            toUser (string) : le nom de l'utilisateur auquel le user répond -> id
            date (datetime) : la date de publication du message
            state (int) : 1 si le message est une citation 0 sinon

        On vérifie d'abord si le message est déjà dans la bdd
        """
        # Vérifier si le topic est bien ajouté
        if not self.is_topic_in_bdd(self.topic_name2url(topic)):
            raise ValueError(f"Le topic {topic} n'existe pas.")

        # ajouter un message
        if not self.is_msg_in_bdd(date, user, topic):
            try:
                cursor = self.connexion.cursor()
                if toUser != '':
                    query = "INSERT INTO messages (message_user, message_topic, message_toUser, message_message, message_date, message_citation) VALUES (%s, %s, %s, %s, %s, %s);"
                    cursor.execute(query, (self.user_name2id(user), self.topic_name2id(topic), self.user_name2id(toUser), msg, date, citation,))
                else:
                    query = "INSERT INTO messages (message_user, message_topic, message_message, message_date, message_citation) VALUES (%s, %s, %s, %s, %s);"
                    cursor.execute(query, (self.user_name2id(user), self.topic_name2id(topic), msg, date, citation,))
            except Exception as e:
                self._logger.error(f"Impossible de poursuivre au risque de ne pas respecter les intégrités référentielles de la base de donnée. {e}")
                raise ValueError("error")

    # GET methods

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
            if ind_ == "all":
                vals = [value[0] for value in resultats]
                return vals
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
 
    def get_data(self, date:str="365j") -> dict:
        """
        Permet d'obtenir tout les titres dans la base de donnée

        Args:
            date (string) : nombre+type

        Exemple:
            '14j', '28m'
        """
        data = {'nom': [], 'user' : [], 'msg': []}
        query = "SELECT topic_nom, topic_user, topic_message FROM topic WHERE topic_date > %s;"
        params = (date,)
        try:
            r = self.get_results(query, params=params, ind_="all")
            for i in range(len(r)):
                data['nom'].append(r[i][0])
                data['user'].append(self.convertId(r[i][1]))
                data['msg'].append(r[i][2])
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e};")
        return data

    # WEB methods

    def nb_mess_start_stop(self, nom:str) -> [int, int]:
        """
        Permet d'obtenir la page de départ à obtenir dans un topic et sa page de fin

        Args: 
            nom (string) : nom du topic

        return:
            [start, stop]
        """

        # Nombre de messages dans message
        query = "SELECT COUNT(id_message) FROM messages WHERE message_topic = %s;"
        params = (self.topic_name2id(nom),)
        try:
            mm = self.get_results(query, params=params)
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}.")
            mm = -1

        query = "SELECT topic_message FROM topic WHERE topic_nom = %s;"
        params = (nom,)
        try:
            mt = self.get_results(query, params=params)
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}")
            mt = -1

        if mm < mt:
            return [mm//20, mt//20+1]
        return [-1, -1]

    # IS methods

    def is_msg_in_bdd(self, date:datetime, user: str, topic: str) -> bool:
        """
        Renvoie un booléen si oui ou non le msg est déjà dans la base de donnée
        Args:
            date (datetime): timestamp du message

        Raises:
            retrieve: [description]
            UnboundLocalError: [description]

        Returns:
            bool: [description]
        """

        _IS_IN = False
        query = "SELECT * FROM messages WHERE message_date = %s AND message_user = %s AND message_topic = %s;"
        params = (date, self.user_name2id(user), self.topic_name2id(topic),)
        try:
            if self.get_results(query, params=params):
                _IS_IN = True
        except Exception as e:
            self._logger.error(f"Une erreur mysql s'est produite : {e}.")
        finally:
            return _IS_IN

    def is_user_in_bdd(self, user: str) -> bool:
        """Indique si un utilisateur est dans la bdd

        Args:
            user (str): [description]

        Returns:
            bool: [description]
        """
        query = "SELECT onchois_id FROM onchois WHERE onchois_nom = %s;"
        params = (user,)
        try:
            if self.get_results(query, params=params):
                self._logger.info(f"L'utilisateur '{user}' existe déjà.")
                return True
        except Exception as e:
            self._logger.error(f"Une erreur mysql est survenue : {e}.")
        self._logger.info(f"L'utilisateur '{user}' n'est pas dans la BDD.")
        return False
    
    def is_topic_in_bdd(self, lien: str) -> bool:
        """Vérifie si un topic est déjà dans la bdd
        Args:
            topic (str): [description]

        Returns:
            bool: [description]
        """
        _ADD = False
        query = "SELECT id_topic FROM topic WHERE topic_lien = %s;"
        params = (lien,)
        try:
            if self.get_results(query, params=params) != []:
                self._logger.info(f"Le topic '{self.topic_url2name(lien)}' est déjà dans la base de donnée.")
                _ADD = True
            self._logger.info(f"Le topic : '{lien}' n'est pas présent dans la base de donnée. Ajout de celui-ci.")
        except Exception as e:
            self._logger.error(f"Une erreur mysql est survenue : {e}.")
        return _ADD
    
    def is_badge_in_bdd(self, badge: str) -> bool:
        """Vérifie si un badge est déjà dans la bdd
        Args:
            badge (str): [description]

        Returns:
            bool: [description]
        """
        _ADD = False
        query = "SELECT badges_id FROM topic WHERE badges_nom = %s;"
        params = (badge,)
        try:
            if self.get_results(query, params=params) != []:
                self._logger.info(f"Le badge '{self.topic_url2name(badge)}' est déjà dans la base de donnée.")
                _ADD = True
            self._logger.info(f"Le badge : '{badge}' n'est pas présent dans la base de donnée. Ajout de celui-ci.")
        except Exception as e:
            self._logger.error(f"Une erreur mysql est survenue : {e}.")
        return _ADD
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from config.Variables.variables import *
from requests import Response, request
from requests.auth import HTTPBasicAuth
from utils.cryptage.encryption import Encrypteur
from utils.logger import logger

class BrowserRequests:
    def __init__(self, user: str, password: str, salt: str = None, profile: str = None, verbose: bool = False):
        # public
        self.data = Encrypteur().decrypte_file(profile, salt, password)
        self.token = self.data[1]
        self.auth = HTTPBasicAuth(user, password)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.token}'}
        self.profile = self.data[0]

        # private
        self._verbose = verbose
        self._logger = logger(PATH_WEB_BROWSER, "WEB", self._verbose)

    def req_html(self, url: str) -> Response:
        """Renvoie la réponse d'une requête"""
        # verification du profile
        try:
            reponse = request("GET", url, auth=self.auth, headers=self.headers)
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}.")
        
        if reponse.status_code // 400 > 0 and reponse.status_code < 500:
            if reponse.status_code == 404:
                self._logger.warning(f"La page a été suprimée.")
            elif reponse.status_code == 403:
                self._logger.warning(f"Vous n'avez pas le bon profile pour accéder à la page.")
            else:
                self._logger.warning(f"Impossible de se connecter, le mot de passe, pseudonyme, le salt ou le profile est/sont mauvais. Err : {reponse.status_code}.")
            exit(1)
        if reponse.status_code // 500 > 0:
            self._logger.warning(f"Impossible de vous connecter à la page (client).")

        if reponse.status_code // 200 > 0 and reponse.status_code < 300:
            return reponse.text
        return ""

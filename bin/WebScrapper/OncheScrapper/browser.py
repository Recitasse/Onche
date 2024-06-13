import os
from typing import Dict

from requests import Response, request
from requests.auth import HTTPBasicAuth

from config.variables import *
from utils.cryptage.encryption import Encrypteur
from utils.logger import logger

from dataclasses import dataclass, field, InitVar


@dataclass
class BrowserRequests:

    user: InitVar[str] = field(default=str)
    password: InitVar[str] = field(default=str)
    salt: InitVar[str] = field(default=None)
    profile: InitVar[str] = field(default=None)
    verbose: bool = field(default=False, init=True)

    headers: dict = field(default_factory=Dict, init=False)
    auth: HTTPBasicAuth = field(default=HTTPBasicAuth, init=False)
    token: str = field(default=str, init=False)

    def __post_init__(self, user: str, password: str, salt: str, profile: str):
        data = Encrypteur().decrypte_file(profile, salt, password)
        self.token = data[1]
        self.auth = HTTPBasicAuth(user, password)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.token}'}
        self.profile = data[0]

        # private
        self._logger = logger(PATH_WEB_BROWSER, "WEB", self.verbose)

    def req_html(self, url: str) -> Response:
        """Renvoie la réponse d'une requête"""
        # verification du profile
        reponse = None
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
                self._logger.warning(
                    f"Impossible de se connecter, le mot de passe, pseudonyme, le salt ou le profile est/sont mauvais. Err : {reponse.status_code}.")
            exit(1)
        if reponse.status_code // 500 > 0:
            self._logger.warning(f"Impossible de vous connecter à la page (client).")

        if reponse.status_code // 200 > 0 and reponse.status_code < 300:
            return reponse.text
        return reponse

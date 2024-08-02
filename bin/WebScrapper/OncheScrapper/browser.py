import os
from typing import Dict

from requests import Response, request
from requests.auth import HTTPBasicAuth

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
        response = None
        try:
            response = request("GET", url, auth=self.auth, headers=self.headers)
        except Exception as e:
            self._logger.error(f"Une erreur est survenue : {e}.")

        if response.status_code // 400 > 0 and response.status_code < 500:
            if response.status_code == 404:
                self._logger.warning(f"La page a été suprimée.")
            elif response.status_code == 403:
                self._logger.warning(f"Vous n'avez pas le bon profile pour accéder à la page.")
            else:
                self._logger.warning(
                    f"Impossible de se connecter, le mot de passe, pseudonyme, le salt ou le profile est/sont mauvais. Err : {reponse.status_code}.")
            exit(1)
        if response.status_code // 500 > 0:
            self._logger.warning(f"Impossible de vous connecter à la page (client).")

        if response.status_code // 200 > 0 and response.status_code < 300:
            return response.text
        return response

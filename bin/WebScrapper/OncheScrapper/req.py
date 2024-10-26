import json

import requests
from requests import get, Session
from dataclasses import dataclass, field
from typing import Dict, Tuple, final, Optional, ClassVar, Union
from datetime import datetime
from config.variables import GLOBAL_PATH
from xml.etree import ElementTree as ET
from os import path
from utils.logger import logger
from bs4 import BeautifulSoup


@dataclass(init=True)
class Requests:
    _session: Session = field(init=False)

    # logger
    _logger: ClassVar = logger("Requests")

    def __post_init__(self) -> None:
        auth, sess = self.__get_cookies()
        self._session = Session()
        self._session.cookies.update({
            "auth": auth,
            "sess": sess
        })

    @staticmethod
    def __get_cookies() -> Tuple[str, str]:
        """
        Renvoie la valeur de la session dans la config
        """
        config_file = path.join(GLOBAL_PATH, "config/OncheIdentificator.xml")
        tree = ET.parse(config_file)
        root = tree.getroot()

        return root.find('auth').text, root.find('sess').text

    @final
    def __bool__(self) -> bool:
        """
        Retourne l'état de la connexion
        """
        if self._session.get("https://onche.org/forum/3/plus-de-18-ans").status_code == 200:
            return True
        return False

    def logged(self) -> Optional[Tuple[datetime, Dict[str, int]]]:
        """
        Retourne les dates de connexions des utilisateurs
        :return: tuple
        """
        url = 'https://onche.org/user/logged'
        response = self._session.get(url)
        if response.status_code == 200:
            return datetime.now(), response.json()
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            print("Response text:", response.text)
        return None

    def req_html(self, url: str = "", bs4_mode: bool = True, json_mode: bool = False) -> Union[str, BeautifulSoup]:
        """
        Renvoie le document HTML de la requête
        """
        response = self._session.get(url)
        if response.status_code // 400 > 0 and response.status_code < 500:
            if response.status_code == 404:
                self._logger.warning(f"La page a été suprimée.")
            elif response.status_code == 403:
                self._logger.warning(f"Vous n'avez pas le bon profile pour accéder à la page.")
            else:
                self._logger.warning(
                    f"Impossible de se connecter, le mot de passe, pseudonyme, le salt ou le profile est/sont mauvais. Err : {response.status_code}.")
        if response.status_code // 500 > 0:
            self._logger.warning(f"Impossible de vous connecter à la page (client).")
        if not bs4_mode and not json_mode:
            return response.text
        elif json_mode:
            return response.json()
        return BeautifulSoup(response.text, 'html.parser')

import os
import re
import xml.etree.ElementTree as ET
import requests
from lxml import html, etree
from bs4 import BeautifulSoup
from utils.logger import logger
from webscrapper.OncheParser.elements.Payload import Payload
from datetime import datetime

from config.Variables.variables import *


class profilPayload(Payload):
    def __init__(self) -> None:
        super().__init__()

    def get_payload(self, name: str):
        """Obtient le payload d'un profil via son pseudo"""
        name = name.lower()
        profil_elements = self._root_profiles.find(f'.//profil')
        DATA = {}
        for child in profil_elements:
            XPATH = child.find('xpath').text
            text = self.__load_profil(name).xpath(XPATH)
            fnd_elem = child.find("clean")
            if fnd_elem.text:
                text = [el.replace(fnd_elem.text, "") for el in text]
            if fnd_elem.get("re"):
                text = [re.search(fnd_elem.get("re"), el) for el in text]
            if len(text) == 1:
                if child.get("type") == "date":
                    DATA.update({child.tag: datetime.strptime(text[0], "%d/%m/%Y")})
                if child.get("type") == "int":
                    DATA.update({child.tag: int(text[0])})
            elif len(text) > 1:
                DATA.update({child.tag: tuple(text)})
            else:
                self.logger.error(f"Impossible d'obtenir une liste vide")
        self.payload = DATA

    def __load_profil(self, name: str):
        """Renvoie le text html etree d'un profile"""
        return etree.HTML(str(BeautifulSoup(requests.get(f"https://onche.org/profil/{name}").content, "html.parser")))

if __name__ == "__main__":
    p = profilPayload()
    p.get_payload("recitasse")

    print(p.get_element("niveau", 2))
    
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

class boardPayload(Payload):
    def __init__(self, id_: int, nom: str) -> None:
        super().__init__()
        self.board = (id_, nom)

    def get_payload(self, page: int):
        """Obtient le payload d'un board via son pseudo"""
        board_elements = self._root_board.find(f'.//board')
        DATA = {}
        for child in board_elements:
            XPATH = child.find('xpath').text
            text = self.__load_board(page).xpath(XPATH)
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
        return {i: {child.tag: DATA[f"""{child.tag}"""][i] for child in board_elements} for i in range(len(DATA[child.tag]))}

    def __load_board(self, num: int):
        """Renvoie le text html etree d'un boarde"""
        return etree.HTML(str(BeautifulSoup(requests.get(f"https://onche.org/forum/{self.board[0]}/{self.board[1]}/{num}").content, "html.parser")))

if __name__ == "__main__":
    p = boardPayload(1, "blabla-general").get_payload(1)
    print(p)
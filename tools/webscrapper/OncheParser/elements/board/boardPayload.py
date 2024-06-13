import xml.etree.ElementTree as ET
import requests
from lxml import etree
from bs4 import BeautifulSoup
from logging import Logger
from utils.logger import logger
from tools.webscrapper.OncheParser.functions import non_message_cleaner
from config.variables import *

from dataclasses import dataclass, field, InitVar
from typing import ClassVar

@dataclass
class boardPayload:
    id_: InitVar[int] = field(default=int, init=True)
    nom: InitVar[str] = field(default=str, init=True)

    balises_board: ClassVar[str] = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/board/board_balises.xml"
    board_elements: ClassVar[ET.Element] = None

    DATA: dict = field(default=None, init=False)
    board: tuple = field(default=None, init=False)
    board_logger: Logger = field(default=None, init=False
                                 )
    def __post_init__(self, id_: int, nom: str):
        """Obtient le payload d'un board via son pseudo"""
        self.board = (id_, nom)
        boardPayload.board_elements = ET.parse(boardPayload.balises_board).getroot()
        self.board_logger = logger(f"{PATH_LOG}/board_scrapper.log", "BOARD SCRAPPER", False)
        self.DATA = {}

    def get_board_info(self, page: int = 1):
        board_elements = boardPayload.board_elements.find(f'.//board')
        board = self.__load_board(page)
        self.DATA = non_message_cleaner(board_elements, board, self.board_logger)
        return self.DATA

    def __load_board(self, num: int):
        """Renvoie le text html etree d'un boarde"""
        return etree.HTML(str(BeautifulSoup(requests.get(f"https://onche.org/forum/{self.board[0]}/{self.board[1]}/{num}").content, "html.parser")))

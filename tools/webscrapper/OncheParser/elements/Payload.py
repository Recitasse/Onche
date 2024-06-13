import re
import xml.etree.ElementTree as ET
from utils.logger import logger

from config.variables import *

class Payload:
    def __init__(self) -> None:
        self.payload = None
        self.logger = logger(PATH_SCRAPPER_LOG, "SCRAPPER")

        self._balises_profiles = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/profil/profil_balises.xml"
        self._balises_board = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/board/board_balises.xml"
        self._balises_topics = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/topic/topic_balises.xml"

        self._root_profiles = self.__load_xml_profil()
        self._root_board = self.__load_xml_board()
        self._root_topics = self.__load_xml_topics()

    def get_element(self, key: str, num: int = None):
        if not num:
            return self.payload[key]
        else:
            try:
                return self.payload[key][0]
            except TypeError:
                self.logger.warning(f"L'index {num} de {key} n'existe pas")
                return self.payload[key]

    def __load_xml_profil(self) -> ET.Element:
        with open(self._balises_profiles, 'r', encoding='utf-8') as xml_balises:
            xml_content = xml_balises.read()
        return ET.fromstring(xml_content)
    
    def __load_xml_board(self) -> ET.Element:
        with open(self._balises_board, 'r', encoding='utf-8') as xml_balises:
            xml_content = xml_balises.read()
        return ET.fromstring(xml_content)
    
    def __load_xml_topics(self) -> ET.Element:
        with open(self._balises_topics, 'r', encoding='utf-8') as xml_balises:
            xml_content = xml_balises.read()
        return ET.fromstring(xml_content)

    @property
    def get_version(self):
        return self._root_profiles.attrib.get('onche-version')

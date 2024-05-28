import xml.etree.ElementTree as ET
import requests
from lxml import etree
from bs4 import BeautifulSoup
from logging import Logger
from utils.logger import logger
from webscrapper.OncheParser.functions import non_message_cleaner

from config.Variables.variables import *

from dataclasses import dataclass, InitVar, field
from typing import ClassVar

@dataclass
class profilPayload:
    name: InitVar[str] = field(init=True, default=str)

    balises_profiles: ClassVar[str] = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/profil/profil_balises.xml"
    profil_elements: ClassVar[ET.Element] = None

    DATA: dict = field(init=False, default=None)
    pseudo: str = field(default=str, init=False)
    profil_logger: Logger = field(default=Logger, init=False)
    
    def __post_init__(self, name: str):
        profilPayload.profil_elements = ET.parse(profilPayload.balises_profiles).getroot()
        self.pseudo = name.lower()
        self.profil_logger = logger(f"{PATH_LOG}/profil_scrapper.log", "PROFIL SCRAPPER", False)
        self.DATA = {}

    def get_profil_info(self):
        profil_elements = profilPayload.profil_elements.find(f'.//profil')
        profil = self.__load_profile()
        self.DATA = non_message_cleaner(profil_elements, profil, self.profil_logger)

    def __load_profile(self) -> ET.Element:
        return etree.HTML(str(BeautifulSoup(requests.get(f"https://onche.org/profil/{self.pseudo.lower()}").content, "html.parser")))
    
    
    @property
    def current_profil(self) -> dict:
        self.get_profil_info()
        return self.DATA

    @property
    def current_badges(self) -> tuple:
        self.get_profil_info()
        return self.DATA['badges']
    
    @property
    def current_level(self) -> int:
        self.get_profil_info()
        return self.DATA['niveau']
    
    @property
    def current_messages(self) -> int:
        self.get_profil_info()
        return self.DATA['messages']
    
p = profilPayload("Recitasse")
print(p.current_profil)
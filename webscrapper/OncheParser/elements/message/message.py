import os
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from lxml import html
from webscrapper.OncheParser.elements.Payload import Payload

from config.Variables.variables import *


class Message:
    def __init__(self, etree_element) -> None:
        self.hard_cleaner = [{'hard': "/>", 'to_set': '>'}, 
                             {'hard': "\n ", 'to_set': '\n'},
                             {'hard': " \n", 'to_set': '\n'},
                             {'hard': "\n<", 'to_set': '<'}, 
                             {'hard': ">\n", 'to_set': '>'}]

        self.message_global = ""
        self.__define_global_message(etree_element)

    def __hard_cleaner(self, text: str) -> str:
        for hard_cleaner in self.hard_cleaner:
            text = text.replace(hard_cleaner['hard'], hard_cleaner['to_set'])
        return text

    def __define_global_message(self, etree_element) -> str:
        if etree_element is not None:
            self.message_load = [el for el in etree_element]
        for el in etree_element:
            self.message_global += html.tostring(el, encoding='unicode')

    def __get_balises(self):
        balise_file = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/message/message_clean.xml"
        with open(balise_file, 'r', encoding='utf-8') as xml_balises:
            xml_content = xml_balises.read()
        self.balises = ET.fromstring(xml_content)

    def clean_balises_html(self) -> str:
        self.__get_balises()
        if self.message_global is None:
            return "" 
        _message = self.__hard_cleaner(self.message_global)
        html_soup = BeautifulSoup(_message, 'html.parser')
        
        for balise in self.balises.findall('.//soup/*'):
            el = balise.get("element")
            class_ = balise.get("class")
            value = balise.get("value")
            decorator_left = balise.get("decorator_left")
            decorator_right = balise.get("decorator_right")

            _soup_find_elements = html_soup.find_all(el, class_=class_)
            for message in _soup_find_elements:
                text_to_replace = self.__hard_cleaner(message.prettify().strip())
                if message and value in message.attrs and message.prettify().strip().find(text_to_replace):
                    if decorator_left and decorator_right:
                        _message = _message.replace(text_to_replace, f"{decorator_left}{message[value]}{decorator_right}")
                    else:
                        _message = _message.replace(text_to_replace, message[value])
                elif value == "text":
                    _message = _message.replace(text_to_replace, message.prettify())
            print(_message)
            
        return ""
            
    def sgt_to_text(self, text: str) -> str:
        self.__get_balises()
        divs = self.balises.find(".//division[@name='signature']")

        element = divs.attrib.get('element')
        class_value = divs.attrib.get('class')
        text = text.replace(f"""<{element} class="{class_value}">""", "")
        text = text.replace(f"</{element}>", "")

        return text

    def msg_to_text(self, text: str) -> str:
        self.__get_balises()
        divs = self.balises.find(".//division[@name='content']")

        element = divs.attrib.get('element')
        class_value = divs.attrib.get('class')
        text = text.replace(f"""<{element} class="{class_value}">""", "")
        text = text.replace(f"</{element}>", "")

        #TODO vérifier pourquoi le parser récupère la signature sans de div à la fin
        text = text.split("<div")[0]
        text = text.replace("<br>", "\n")

        return text



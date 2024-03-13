import os
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from lxml import html
from webscrapper.OncheParser.elements.Payload import Payload

from config.Variables.variables import *


class Message:
    def __init__(self, etree_element) -> None:
        self.message_global = ""
        self.__define_global_message(etree_element)

    def __define_global_message(self, etree_element) -> str:
        if etree_element is not None:
            self.message_load = [el for el in etree_element]
        for el in etree_element:
            self.message_global += html.tostring(el, encoding='unicode')
        self.message_global = self.__clean_html_to_text(self.message_global)

    def __get_balises(self):
        balise_file = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/message/message_clean.xml"
        with open(balise_file, 'r', encoding='utf-8') as xml_balises:
            xml_content = xml_balises.read()
        self.balises = ET.fromstring(xml_content)



    def clean_balises_html(self, name:str) -> str:
        self.__get_balises()
        _message = self.message_global
        if name not in ["message", "signature"]:
            raise ValueError(f'Le type doit soit être "message" soit "signature"')
        for elements in self.balises.findall(f'.//soup[@name="{name}"]'):
            for divisions in elements:
                div_ = divisions.get("element")
                class_ = divisions.get("class")
                text_to_delete = BeautifulSoup(_message, "html.parser").find(div_, class_=class_)

                if divisions.tag == "exclude":
                    if text_to_delete:
                        text_to_delete = self.__clean_html_to_text(text_to_delete.prettify())
                        _message = _message.replace(text_to_delete, "")

                elif divisions.tag == "division":
                    decorator_left = divisions.get("decorator_left")
                    decorator_right = divisions.get("decorator_right")
                    value = divisions.get("value")

                    text_to_replace = BeautifulSoup(_message, "html.parser").find_all(div_, class_=class_)
                    print(text_to_replace)
                    if text_to_replace != []:
                        for element_to_replace in text_to_replace:
                            text_to_replace_final = self.__clean_html_to_text(element_to_replace.prettify())
                            if value in element_to_replace.attrs:
                                _message = _message.replace(text_to_replace_final, f'{decorator_left}{element_to_replace[value]}{decorator_right}')
                            if value == "raw":
                                _message = _message.replace(text_to_replace_final, f'{decorator_left}{self.__clean_html_to_text(element_to_replace.prettify())}{decorator_right}')

        #print("message : ", _message)
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

    @staticmethod
    def __clean_html_to_text(text: str) -> str:
        text = re.sub(r'>\s+<', '><', text)
        text = re.sub(r'>\s+', '>', text)
        text = re.sub(r'\s+<', '<', text)
        text = re.sub(r'<img\s.*?/>', lambda m: m.group(0)[:-2] + '>', text)
        return ''.join([element for element in list(text) if element != '\n'])

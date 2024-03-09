import os
import re
import xml.etree.ElementTree as ET
import requests

from lxml import html, etree
from bs4 import BeautifulSoup
from datetime import datetime
from utils.logger import logger
from webscrapper.OncheParser.elements.Payload import Payload
from webscrapper.OncheParser.elements.message.message import Message

from config.Variables.variables import *

class topicPayload(Payload):
    def __init__(self) -> None:
        super().__init__()

    def get_payload(self, link: str, page: int):
        """Obtient le payload d'un board via son pseudo"""
        DATA = {}
        topic_elements = self._root_topics.find('.//topic')
        msg_root = self._root_topics.find('topic').get("root")
        messages = self.__load_topic(link, page).xpath(msg_root)

        for i, message in enumerate(messages):
            message_element = etree.ElementTree(message)
            tmp_ = {}
            print(f"message n°{i}")

            for child in topic_elements:
                XPATH = child.find('xpath').text
                fnd_elem = child.find("clean")
                is_message = child.get("is_message")

                text = message_element.xpath(XPATH)[-1] if len(message_element.xpath(XPATH)) != 0 else ""
                if fnd_elem.text:
                    text = [el.replace(fnd_elem.text, "") for el in text]

                if fnd_elem.get("re"):
                    if fnd_elem.get("time"):
                        _occ_date = re.findall(fnd_elem.get("re"), text)
                        text = _occ_date[0] if len(_occ_date) != 0 else ""
                    else:
                        text = [re.search(fnd_elem.get("re"), el) for el in text]

                if is_message == "1":
                    _tmp_message = Message(text)
                    _tmp_message.clean_balises_html(child.tag)
                    """if child.tag == "signature":
                        tmp_.update({"signature": _tmp_message.sgt_to_text(text)})
                        print(tmp_['signature'])
                    if child.tag == "message":
                        tmp_.update({"message": _tmp_message.msg_to_text(text)})
                        print(tmp_['message'])"""
    
                if len(text) == 1:
                    if child.get("type") == "date":
                        tmp_.update({child.tag: datetime.strptime(text[0], "%d/%m/%Y %H:%M:%S")})
                    elif child.get("type") == "int":
                        tmp_.update({child.tag: int(text[0])})
                    else:
                        tmp_.update({child.tag: text[0]})
                if len(text) > 1:
                    tmp_.update({child.tag: tuple(text)})
                else:
                    self.logger.error(f"Impossible d'obtenir une liste vide")
            DATA.update({i: tmp_})
            print("\n\n")
        self.payload = DATA
        

    def __load_topic(self, link: str, page: int):
        """Renvoie le text html etree d'un topic"""
        return etree.HTML(str(BeautifulSoup(requests.get(f"{link}/{page}").content, "html.parser")))

if __name__ == "__main__":
    p = topicPayload()
    p.get_payload("https://onche.org/topic/467663/dragon-ball-quand-meme", 1)
    #print(p.payload)

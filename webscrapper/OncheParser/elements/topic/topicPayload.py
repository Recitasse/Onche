import requests
from html import unescape
import re

from config.Variables.variables import *

from logging import Logger
from utils.logger import logger
from webscrapper.OncheParser.functions import *

from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class topicPayload:
    link: str = field(init=True, default=str)

    balises_topics: ClassVar[str] = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/topic/topic_balises.xml"
    balises_messages: ClassVar[str] = f"{GLOBAL_PATH}webscrapper/OncheParser/elements/topic/message_balises.xml"
    topics_elements: ClassVar[ET.Element] = None
    messages_elements: ClassVar[ET.Element] = None

    DATA: dict = field(init=False, default=None)
    messages: list = field(init=False, default=None)
    topic_logger: Logger = field(default=Logger, init=False)
    
    def __post_init__(self):
        topicPayload.topics_elements = ET.parse(topicPayload.balises_topics).getroot()
        topicPayload.messages_elements = ET.parse(topicPayload.balises_messages).getroot()
        self.topic_logger = logger(f"{PATH_LOG}/topic_scrapper.log", "TOPIC SCRAPPER", False)
        self.DATA = {}


    def get_message(self, message, page: int = 1):
        message_elements = topicPayload.messages_elements.find(f".//message")
        global_message = etree.tostring(message, pretty_print=True).decode("utf-8")
        global_message = clean_signature(global_message)
        global_message = sticker_message(message_elements, message, self.topic_logger, global_message)['message']
        global_message = smiley_svg_message(message_elements, message, self.topic_logger, global_message)
        global_message = gif_message(message_elements, message, self.topic_logger, global_message)
        global_message = smiley_message(message_elements, message, self.topic_logger, global_message)
        global_message = image_message(message_elements, message, self.topic_logger, global_message)
        global_message = link_message(message_elements, message, self.topic_logger, global_message)
        global_message = normal_message(global_message)
        global_message = message_to_onche(message_elements, self.topic_logger, global_message)
        return unescape(global_message)

    def get_topic_payload(self, page: int = 1) -> dict:
        GLOBAL = {}
        topic_elements = topicPayload.topics_elements.find(f".//topic")
        topic = self.__load_topic(page)
        messages = list(non_message_cleaner(topic_elements, topic, self.topic_logger)['message'])
        for i, message in enumerate(messages):
            global_message = self.get_message(message, page)
            DATA = non_message_cleaner(topic_elements, message, self.topic_logger)
            print(f"message {i}")
            print(global_message)
            print(DATA['pseudo'][i])
            print("\n============================\n")


    def __load_topic(self, page: int):
        """Renvoie le text html etree d'un topic"""
        return etree.HTML(str(BeautifulSoup(requests.get(f"{self.link}/{page}").content, "html.parser")))

if __name__ == "__main__":
    p = topicPayload("https://onche.org/topic/267079/rando-la-breche-de-roland")
    p.get_topic_payload(1)

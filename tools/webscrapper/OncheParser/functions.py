from abc import ABC
from lxml import html, etree
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from logging import Logger

import re
from datetime import datetime


def non_message_cleaner(xml_elements: ET.Element, loader, logger: Logger) -> dict:
    tmp_data = {}
    for child in xml_elements:
        XPATH = child.find('xpath').text
        text = loader.xpath(XPATH)
        fnd_elems = child.findall("clean")
        if len(fnd_elems) > 1:
            i = 0
            while i < len(fnd_elems) or len(''.join(text).split()) != 1:
                if fnd_elems[i].text:
                    text = [el.replace(fnd_elems[i].text, "") for el in text]
                if fnd_elems[i].get("re"):
                    complete_text = ''.join(text)
                    match = re.search(fnd_elems[i].get("re"), complete_text)
                    if match:
                        text = [el.replace(f" {match.group(0)}", "") for el in text]
                i += 1
        else:
            if fnd_elems[0].text is not None:
                text = [el.replace(fnd_elems[0].text, "") for el in text]
            elif not fnd_elems:
                logger.warning(f"Impossible de nettoyer le texte correctement pour : {child.tag}")

        if len(text) == 1:
            if child.get("type") == "date":
                tmp_data.update({child.tag: datetime.strptime(text[0], "%d/%m/%Y")})
            if child.get("type") == "int":
                tmp_data.update({child.tag: int(text[0])})
    
        elif len(text) > 1:
            tmp_data.update({child.tag: tuple(text)})

        else:
            logger.error(f"Impossible d'obtenir une liste vide")
    return tmp_data


def clean_signature(global_text: str) -> str:
    global_text = global_text.replace('<div class="_format _center">', "")
    global_text = global_text.replace("<br/>", "\n")
    global_text = global_text.replace('<div class="_format _spoiler"><div>', "")
    return global_text.split('<div class="signature">')[0]+"</div>"


def smiley_message(xml_elements: ET.Element, loader, logger: Logger, global_text: str) -> str:
    root_ = xml_elements.find(".//smiley/xpath")
    for i, el in enumerate(loader.xpath(root_.text)):
        text = etree.tostring(el, pretty_print=True).decode("utf-8")
        match = re.search(f"{xml_elements.find('.//smiley/clean').get('re')}", text)

        match_text = re.search(f'{xml_elements.find(".//smiley/total").get("re")}', text, re.DOTALL)

        if match and match_text:
            data_name = match.group(1)
            text = match_text.group(0)

            global_text = global_text.replace(text, data_name)
    return global_text

def smiley_svg_message(xml_elements: ET.Element, loader, logger: Logger, global_text: str) -> str:
    root_ = xml_elements.find(".//smiley-svg/xpath")
    for i, el in enumerate(loader.xpath(root_.text)):
        text = etree.tostring(el, pretty_print=True).decode("utf-8")

        match = re.search(f"{xml_elements.find('.//smiley-svg/clean').get('re')}", text, re.DOTALL)
        match_text = re.search(f'{xml_elements.find(".//smiley-svg/replace").get("re")}', text, re.DOTALL)

        if match and match_text:
            data_name = match.group(1)
            text = match_text.group(0)
            global_text = global_text.replace(text, data_name)

    return global_text

def message_to_onche(xml_elements: ET.Element, logger: Logger, global_text: str):
    root_ = xml_elements.find(".//html")
    for child in root_:
        global_text = global_text.replace(child.text, child.get('replace'))
    return global_text

def normal_message(global_text: str) -> str:
    global_text = global_text.replace('<div class="message-content">', "")
    global_text = ''.join(global_text.split("</div>")[:-1])
    return global_text

def gif_message(xml_elements: ET.Element, loader, logger: Logger, global_text: str) -> str:
    root_ = xml_elements.find(".//gif/xpath")
    for i, el in enumerate(loader.xpath(root_.text)):
        text = etree.tostring(el, pretty_print=True).decode("utf-8")
        match = re.search(f"{xml_elements.find('.//gif/clean').get('re')}", text)

        if match:
            gif_text = match.group(0).split("/")[-2]
            data_name = xml_elements.find('.//gif/clean').get('left') + gif_text + xml_elements.find('.//gif/clean').get('right')

            text_rep = text.split("\n")
            for i, _ in enumerate(text_rep):
                text_rep[i] = "  "+text_rep[i]
            text_rep = '\n'.join(text_rep[:-1])
            global_text = global_text.replace(text_rep, data_name)

            pattern = r'\n(\[gif:.*?\])\n'
            matches = re.findall(pattern, global_text)

            for match in matches:
                global_text = global_text.replace(f"\n{match}\n", match)

    return global_text


def image_message(xml_elements: ET.Element, loader, logger: Logger, global_text: str) -> str:
    root_ = xml_elements.find(".//image/xpath")
    for i, el in enumerate(loader.xpath(root_.text)):
        text = etree.tostring(el, pretty_print=True).decode("utf-8")
        match = re.search(f"{xml_elements.find('.//image/clean').get('re')}", text)


        if match:
            gif_text = match.group(0).split("/")[-1]
            data_name = xml_elements.find('.//image/clean').get('left') + gif_text[:-1] + xml_elements.find('.//image/clean').get('right')

            text_rep = text.split("\n")
            for i, _ in enumerate(text_rep):
                text_rep[i] = text_rep[i].strip()
            text_rep = ''.join(text_rep[:-1])
            global_text = global_text.replace(text_rep, data_name)

            pattern = r'\n(\[img:.*?\])\n'
            matches = re.findall(pattern, global_text)

            for match in matches:
                global_text = global_text.replace(f"\n{match}\n", match)

    return global_text


def link_message(xml_elements: ET.Element, loader, logger: Logger, global_text: str):
    root_ = xml_elements.find(".//link/xpath")
    for i, el in enumerate(loader.xpath(root_.text)):
        text = etree.tostring(el, pretty_print=True).decode("utf-8")

        match = re.search(f"{xml_elements.find('.//link/clean').get('re')}", text)
        match_text = re.search(f'{xml_elements.find(".//link/replace").get("re")}', text, re.DOTALL)

        if match and match_text:
            link_text = match.group(1)
            replace_text = match_text.group(0)

            tmp_ = ""
            for i, tt in enumerate(replace_text.split("\n")):
                tmp_ += tt.strip()
            replace_text = tmp_

            if 'class="youtube"' in replace_text:
                replace_text = replace_text.replace(">", ">\n")
                replace_text = ''.join(list(replace_text)[:-1])
                replace_text = replace_text.replace("</div>\n</a>", "</div></a></div>")

                link_text = re.search(xml_elements.find(".//link/youtube").get("re"), text).group(1)
                link_text = link_text.replace("www.youtube.com/embed", "youtu.be")

            global_text = global_text.replace(replace_text, link_text)

    return global_text

def sticker_message(xml_elements: ET.Element, loader, logger: Logger, global_text: str) -> dict:
    tmp_ = {'sticker': {}, 'message': ''}
    root_ = xml_elements.find('.//sticker/xpath')
    for i, el in enumerate(loader.xpath(root_.text)):
        div_content = ""
        data_name = ""

        text = etree.tostring(el, pretty_print=True).decode("utf-8")
        match = re.search(f"{xml_elements.find('.//sticker/infos').get('re')}", text)

        match_text = re.search(f'{xml_elements.find(".//sticker/clean").get("re")}', text, re.DOTALL)
        if match_text:
            div_content = match_text.group(0)
        else:
            logger.warning(f"Impossible de récupérer le texte : {text}")

        if match:
            data_collection = match.group(1)
            data_name = match.group(2)
            tmp_['sticker'].update({'collection': data_collection, 'name': data_name})
        else:
            logger.warning(f"Impossible de récupérer le texte : {text}")

        if match_text and match:
            global_text = global_text.replace(div_content, f':{data_name}:')
            tmp_['message'] = global_text
    return tmp_


from dataclasses import dataclass
import re


@dataclass(init=False)
class MessageCleaner:
    @staticmethod
    def clean_message(text: str) -> str:
        text = str(text)
        text = MessageCleaner.__clean_signature(text)
        text = MessageCleaner.__clean_basic_balise(text)
        text = MessageCleaner.__convert_sticker(text)
        text = MessageCleaner.__clean_html(text)
        text = MessageCleaner.__clean_center(text)
        text = MessageCleaner.__clean_spoiler(text)
        text = MessageCleaner.__clean_smileys(text)
        text = MessageCleaner.__clean_tweet(text)
        text = MessageCleaner.__clean_onche_image(text)
        text = MessageCleaner.__last_clean(text)

        return text

    @staticmethod
    def __convert_sticker(text: str) -> str:
        pattern = r'<div class="sticker"[^>]*data-name="([^"]+)"[^>]*>.*?</div>'
        replacement = lambda m: f":{m.group(1)}:"
        return re.sub(pattern, replacement, text, flags=re.DOTALL)

    @staticmethod
    def __clean_html(text: str) -> str:
        text = text.replace("<br/>", '\n')
        return text

    @staticmethod
    def __clean_signature(text: str) -> str:
        if '<div class="signature">' in text:
            text = text.split('<div class="signature">')[0]
        return text

    @staticmethod
    def __clean_center(text: str) -> str:
        pattern = r'<div class="_format _center">(.*?)</div>'
        replacement = r'[center]\1[/center]'
        return re.sub(pattern, replacement, text, flags=re.DOTALL)

    @staticmethod
    def __clean_spoiler(text: str) -> str:
        text = text.replace('<div class="_format _spoiler">', '')
        return text

    @staticmethod
    def __clean_basic_balise(text: str) -> str:
        basic = ['b', 'i', 'u', 's']
        for el in basic:
            pattern = f'<{el}>(.*?)</{el}>'
            replacement = f'[{el}]\\1[/{el}]'
            text = re.sub(pattern, replacement, text)
        return text

    @staticmethod
    def __clean_smileys(text: str) -> str:
        pattern = r'<div class="smiley svg">.*?<img[^>]+title="([^"]+)".*?</div>'
        replacement = lambda m: f"{m.group(1)}"
        return re.sub(pattern, replacement, text, flags=re.DOTALL)

    @staticmethod
    def __clean_onche_image(text: str) -> str:
        pattern = r'<a[^>]+href="([^"]+)"[^>]*>.*?<img.*?</a>'
        replacement = lambda m: f"[img:{m.group(1).split('/')[-2]}]" if "imgur.com" not in m.group(1) else m.group(1)
        return re.sub(pattern, replacement, text, flags=re.DOTALL)

    @staticmethod
    def __clean_tweet(text: str) -> str:
        pattern = r'<a class="link"[^>]*>\s*<div class="_format _tweet"[^>]*>(.*?)</div>\s*</a>'
        replacement = lambda m: f"{m.group(1)}"
        return re.sub(pattern, replacement, text, flags=re.DOTALL)

    @staticmethod
    def __last_clean(text: str) -> str:
        text = text.replace("</div>", '')
        text = text.replace('<div class="message-content">', '')
        return text

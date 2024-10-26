from datetime import datetime
import re
from dataclasses import dataclass
from bs4 import BeautifulSoup
from bin.WebScrapper.OncheScrapper.req import Requests


@dataclass(init=False)
class Messages:
    @staticmethod
    def _messages_collector(id: int, titre: str, page: int) -> BeautifulSoup:
        link = f'https://onche.org/topic/{id}/{titre}/{page}'
        return Requests().req_html(link, bs4_mode=True)

    @staticmethod
    def collector(id: int, titre: str, page: int) -> dict:
        soup = Messages._messages_collector(id, titre, page)
        info = {}
        if soup.select('.messages > div.message:nth-of-type(2n)').__len__() > 1:
            tmp_ = []
            for el in soup.select('.messages > div.message:nth-of-type(2n)'):
                tmp_.append(el.get('data-id') if True else el)
            info.update({'oid': tmp_})
        else:
            info.update({'oid': soup.select('.messages > div.message:nth-of-type(2n)')[0].get('data-id')})
        if not isinstance(info['oid'], list):
            info['oid'] = int(info['oid'])
        else:
            info['oid'] = [int(el_) if isinstance(el_, str) else int(el_) for el_ in info['oid']]
        if soup.select('.messages > div:nth-child(2n) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)').__len__() > 1:
            tmp_ = []
            for el in soup.select('.messages > div:nth-child(2n) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)'):
                tmp_.append(el.get('alt') if True else el)
            info.update({'user': tmp_})
        else:
            info.update({'user': soup.select('.messages > div:nth-child(2n) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)')[0].get('alt')})
        if soup.select('.messages > div > div:nth-last-child(2)').__len__() > 1:
            tmp_ = []
            for el in soup.select('.messages > div > div:nth-last-child(2)'):
                tmp_.append(el.text if False else el)
            info.update({'message': tmp_})
        else:
            info.update({'message': soup.select('.messages > div > div:nth-last-child(2)')[0].text})
        if soup.select('div.answer').__len__() > 1:
            tmp_ = []
            for el in soup.select('div.answer'):
                tmp_.append(el.get('data-username') if True else el)
            info.update({'touser': tmp_})
        else:
            info.update({'touser': soup.select('div.answer')[0].get('data-username')})
        if soup.select('div.answer').__len__() > 1:
            tmp_ = []
            for el in soup.select('div.answer'):
                tmp_.append(el.get('data-id') if True else el)
            info.update({'answeroid': tmp_})
        else:
            info.update({'answeroid': soup.select('div.answer')[0].get('data-id')})
        cleans = []
        for clean in cleans:
            if info['answeroid'].__len__() > 1 and not isinstance(info['answeroid'], str):
                for i in range(info['answeroid'].__len__()):
                    info['answeroid'][i] = info['answeroid'][i].replace(clean[0], '')
                    if clean[1] != '':
                        match = re.search(clean[1], info['answeroid'][i])
                        if match:
                            rep = ' ' + match[0]
                            info['answeroid'][i] = info['answeroid'][i].replace(rep, '') if clean[2] == 'False' else rep
                    if clean[3] != '':
                        info['answeroid'][i] = info['answeroid'][i].split(clean[3])[0]
            else:
                info['answeroid'] = info['answeroid'].replace(clean[0], '')
                if clean[1] != '':
                    match = re.search(clean[1], info['answeroid'])
                    if match:
                        rep = ' ' + match[0]
                        info['answeroid'] = info['answeroid'].replace(rep, '') if clean[2] == 'False' else rep
                if clean[3] != '':
                    info['answeroid'] = info['answeroid'].split(clean[3])[0]
        if not isinstance(info['answeroid'], list):
            info['answeroid'] = int(info['answeroid'])
        else:
            info['answeroid'] = [int(el_) if isinstance(el_, str) else int(el_) for el_ in info['answeroid']]
        if soup.select('div.message-date').__len__() > 1:
            tmp_ = []
            for el in soup.select('div.message-date'):
                tmp_.append(el.get('title') if True else el)
            info.update({'date': tmp_})
        else:
            info.update({'date': soup.select('div.message-date')[0].get('title')})
        cleans = [('Publié le ', '', 'False', ''), ('à ', '', 'False', ''), ('', '', '', 'et ')]
        for clean in cleans:
            if info['date'].__len__() > 1 and not isinstance(info['date'], str):
                for i in range(info['date'].__len__()):
                    info['date'][i] = info['date'][i].replace(clean[0], '')
                    if clean[1] != '':
                        match = re.search(clean[1], info['date'][i])
                        if match:
                            rep = ' ' + match[0]
                            info['date'][i] = info['date'][i].replace(rep, '') if clean[2] == 'False' else rep
                    if clean[3] != '':
                        info['date'][i] = info['date'][i].split(clean[3])[0]
            else:
                info['date'] = info['date'].replace(clean[0], '')
                if clean[1] != '':
                    match = re.search(clean[1], info['date'])
                    if match:
                        rep = ' ' + match[0]
                        info['date'] = info['date'].replace(rep, '') if clean[2] == 'False' else rep
                if clean[3] != '':
                    info['date'] = info['date'].split(clean[3])[0]
        if not isinstance(info['date'], list):
            info['date'] = info['date'][:-1] if info['date'][-1] == ' ' else info['date']
            info['date'] = datetime.strptime(info['date'], '%d/%m/%Y %H:%M:%S')
        else:
            for i in range(info['date'].__len__()):
                info['date'][i] = info['date'][i][:-1] if info['date'][i][-1] == ' ' else info['date'][i]
            info['date'] = [datetime.strptime(el_, '%d/%m/%Y %H:%M:%S') for el_ in info['date']]

        info['id'] = id
        info['titre'] = titre
        info['page'] = page

        return info

import sys
import os
import datetime
import time

from bs4 import BeautifulSoup
from prettytable import PrettyTable
from browser import BrowserRequests

from utils.logger import logger
from utils.fonction import forum_xml, timedelta
from utils.graphics import bar_etape

from config.Variables.variables import *
from BDD.bdd import BDD

class ScrapperOnche:
    def __init__(self, nom: str | int, BOT_agent: str = MYSQL_USER, pseudo: str = "Agent-PCO-001", pwd: str = "DwpNU4cs5Uaugwj", salt: str = "1kd0S", profil: str = DEFAULT_PROFILE, verbose: bool = False) -> None:
        
        # public
        self.forum = forum_xml(nom)
        self.url = f"https://onche.org/forum/{self.forum['id']}/{self.forum['name']}"
        self.excluded = self.forum['topics']
        self.profile = self.forum['profile']['profile']

        # private
        self._verbose = verbose
        self._logger = logger(PATH_SCRAPPER_LOG, "SCRAPPER", self._verbose)
        self._browser = BrowserRequests(pseudo, pwd, salt, profil)
        self._local_BDD = BDD(database=MYSQL_DATABASE, user=BOT_agent)
        

    def get_front_page_info(self, page_it:int=1) -> dict:
        """
        Renvoie le dict {'nom' : [], 'sujet' : [], 'nb' : [], 'lien' : []}
        """
        go_to = f"{self.url}/{page_it}"
        self.DATA = {'nom' : [], 'sujet' : [], 'nb' : [], 'lien' : []}
        html_text = self._browser.req_html(go_to)
        self.html_parser = BeautifulSoup(html_text, "html.parser")

        # Code à modifier suivant le forum
        # ===============================================================================
        topicNames = self.html_parser.find_all("div", class_="topic-username")
        nbMessageTopic = self.html_parser.find_all("span", class_="topic-nb")
        titreTopic = self.html_parser.find_all("a", class_="topic-subject link")
        lienTopic = self.html_parser.find_all("a", class_="topic-subject link")
        # ===============================================================================

        # Récupération des noms
        for nomUser in topicNames:
            self.DATA['nom'].append(nomUser.get_text(strip=True))
        for nbm in nbMessageTopic:
            self.DATA['nb'].append(nbm.get_text(strip=True))

        for lien in lienTopic:
            self.DATA['lien'].append(lien.get('href'))

        # Cas particulier pour le titre <a> -> <span>
        for i, spanElement in enumerate(titreTopic):
            spanText = list(spanElement.get_text(strip=True))
            
            # Suppression du chiffre et pseudo (via len)
            taille = len(list(self.DATA['nom'][i]))+len(list(self.DATA['nb'][i]))
            spanText = ''.join(spanText[:-taille]).replace("\'","'")
            # Correction sur les caractères spéciaux
            self.DATA['sujet'].append(spanText)
            del taille
        return self.DATA

    def add_to_bdd_page(self, page: int) -> dict:
        """
        On veut obtenir les messages, mais pas que :
        Le nom de l'user, s'il répond à qqn, son message et sa date de publication.

        Pour cela on a besoin du lien, du nombre de message et la date de publipostage des anciens.

        Args:
            lien (string) : mettre le lien du topic
        Return:
            list -> DATA_MESS = [[{'user' :  [], 'msg' :  [],'touser' : [], 'date' : [], 'page': 1}],[],[],...,[{... 'page':n}]]

        Note, on peut vérifier la page, où : DATA_MESS[0] = DATA_MESS[0]['page'] 
        """
        # Récupération des infos de la page
        topics = self.get_front_page_info(page)
        print(f"\n========================== PAGE {page} ==========================")
        # Si le topic n'existe pas
        for el in range(len(topics['lien'])):
            if topics["lien"][el] in self.excluded:
                self._logger.info(f"Le topic {topics['sujet'][el]} fait partie de la liste noire.")
                continue
            else:
                # attribution des valeurs Renvoie le dict {'nom' : [], 'sujet' : [], 'nb' : [], 'lien' : []}
                lien = topics['lien'][el]
                sujet = topics['sujet'][el]
                nom_user = topics['nom'][el]
                nb = int(topics['nb'][el])

                # TODO Trouvé pourquoi l'on récupère l'id et non pas le nom
                if isinstance(nom_user, int):
                    nom_user = self._local_BDD.user_id2name(nom_user)
                self._local_BDD.add_user(nom_user)
                timedelta("365j")

                # le topic n'est pas dans la base de donnée
                START = 0
                STOP = 0
                if not self._local_BDD.is_topic_in_bdd(lien):
                    START = 0
                    STOP = 1
                    self._local_BDD.add_topic(sujet, nom_user, nb, lien, self.forum['id'])
                else:
                    START, STOP = self._local_BDD.nb_mess_start_stop(sujet)
                    self._logger.info(f"Scrappe de {sujet} de {START} à {STOP}.")
                it = 0             

                # Regarde sur toutes les pages non visitées
                for i in range(START+1, STOP+1):
                    # Requête curl
                    go_to = f"{lien}/{i}"
                    Index = []
                    data = self._browser.req_html(go_to)
                    self.html_parser = BeautifulSoup(data, "html.parser")

                    liste_message = {'user' :  [], 'msg' :  [],'touser' : [], 'date' : [], 'badguser' : [], 'cite_state':[], 'page': i-1}
                    liste_cit = {'user' :  [], 'msg' :  [],'cite' : [], 'date' : [], 'page': i-1}
                
                    # Obtention de la liste des messages
                    old_username = ""
                    MESS = self.html_parser.find_all("div", class_="message")
                    for mes in MESS:
                        # Obtention des (réponses s'il y en a)
                        rep = mes.find("div", class_="message answer")
                        if rep:
                            user = mes.find('a', class_="message-username")
                            user = user.get_text(strip=True)
                            username = rep.get('data-username')
                            msg = ""

                        else:
                            username = ""
                            user = mes.find('a', class_="message-username")
                            user = user.get_text(strip=True)

                            # Obtention des informations si on a pas de réponse
                            msg = mes.find("div", class_="message-content")
                            sign = mes.find("div", class_="signature")
                            msg = msg.get_text(strip=True)
                            if sign:
                                msg = msg.replace(sign.get_text(),"")

                        # On récupère les user et les touser
                        if user == old_username:
                            pass
                        else:
                            liste_message["user"].append(user)
                            liste_message["touser"].append(username)
                        old_username = username
                            
                    for answer_div in self.html_parser.find_all("div", class_="message answer"):
                        answer_div.extract()

                    mess_user = self.html_parser.find_all("div", class_="message")
                    k = 0
                    
                    for mes in mess_user:
                        # On récupère le message
                        msg = mes.find("div", class_="message-content")

                        # remplacer les images par leur titre :
                        for img_tag in msg.find_all('img'):
                            img_title = img_tag.get('title')
                            img_tag.replace_with(f'({img_title})')
                        sign = mes.find("div", class_="signature")
                        msg = msg.get_text(strip=True).replace("(:",' :').replace(':)',": ")

                        if sign != None:
                            sign = sign.get_text(strip=True)
                        else:
                            sign = ""
                        msg = msg.replace(sign,"")

                        # On récupère la date 
                        try:
                            datemsg = mes.find("div", class_="message-date")
                            datemsg = datemsg.get('title').replace("Publié le ","").replace(" et modifié le ",",").replace(" à ", " ").split(",")
                            date_t = datemsg[0]

                            date_format = "%d/%m/%Y %H:%M:%S"
                            new_date_format = "%Y-%m-%d %H:%M:%S"

                            date_object = datetime.datetime.strptime(date_t, date_format)
                            date_t = date_object.strftime(new_date_format)
                            liste_message["date"].append(date_t) 
                        except AttributeError as e:
                            self._logger.error(f"x Erreur : {e}. La date est indisponible.")
                            return

                        liste_message["msg"].append(msg)
                        
                        # On récupère les badges des onchois
                        badges_loc = mes.find("div", class_="message-badges")
                        badges = badges_loc.find_all("img", class_="icon")
                        liste_message['badguser'].append([badge.get('alt') for badge in badges])

                        # On récupère les liste_cits manuelles
                        # ================= DEPRECIE ===========================
                        for liste_cits in mes.find_all("div", class_="signature"):
                            liste_cits.extract()

                        cits = mes.find_all("a", class_="_format _mention")
                        # Indexation : 
                        Index.append(len(cits))
                        for cit in cits:
                            userCite = cit.get_text(strip=True).replace('@','')
                            # On ajoute l'user au cas où il ne serait pas référencé
                            liste_cit['user'].append(liste_message["user"][k])
                            liste_cit['cite'].append(userCite)
                            liste_cit['msg'].append(liste_message["msg"][k])
                            liste_cit['date'].append(liste_message["date"][k])
                        # =======================================================
                        k+=1

                    for tsr in range(len(liste_message['touser'])):
                        if liste_message['touser'][tsr]:
                            liste_message['cite_state'].append(1)
                        else:
                            liste_message['cite_state'].append(0)
                    bar_etape(STOP-START, it, f"Topic {sujet} sur le forum {self.forum['name']}")
                    self.add_data_to_bdd(sujet, liste_message, liste_cit)
                    it+=1
                    time.sleep(1)
                time.sleep(1)
                self._logger.info("Ajout des messages effectué.")

    def afficher(self):
        """
        Affiche le tableau des informations récupérées dans le logger
        """
        self._logger.info(f"Actualisation du {datetime.datetime.now()}")
        table = PrettyTable()
        table.field_names = ["Nom", "Titre du topic", "Nb msg"]

        for i in range(len(self.DATA['nom'])):
            table.add_row([self.DATA['nom'][i], self.DATA['sujet'][i], self.DATA['nb'][i]])
        self._logger.info(table)
        self._logger.info("\n")

    def get_badges(self, nom:str) -> list:
        """
        Obtention des badges de l'utilisateurs

        Args:
            nom (string) : nom de l'utilisateur
        """
        # Via l'accession au topic
        url_badge = f"https://onche.org/profil/{nom}"
        data = self._browser.req_html(url_badge)
        self.html_parser = BeautifulSoup(data, "html.parser")

        # Class intéressantes 
        badges = self.html_parser.find_all("img", class_="icon")

        # Récupération des noms
        badgeListUser = []
        for badge in badges:
            badgeListUser.append(badge.get('alt'))
        return badgeListUser
    
    def add_data_to_bdd(self, topic: str, liste_message: dict, liste_cit: dict) -> None:
        """
        Ajoute à la base de donnée, les citations et les messages
        """
        
        for k in range(len(liste_message['user'])):
            # Ajout de l'user (nécessaire à l'intégrité de la bdd)
            self._local_BDD.add_user(liste_message['user'][k])

            # Pour tout les badges dans badguser
            try:
                for badge in liste_message['badguser'][k]:
                    self._local_BDD.add_badges_users(badge, liste_message['user'][k])
            except IndexError as e:
                self._logger.warning(f"ATTENTION : {e}")
            
            # Ajout des messages
            self._local_BDD.add_message(user=liste_message['user'][k], topic=topic, msg=liste_message['msg'][k], toUser=liste_message['touser'][k], date=liste_message['date'][k], citation=liste_message['cite_state'][k])

        for k in range(len(liste_cit['user'])):
            # Ajout de l'user (nécessaire à l'intégrité de la bdd)
            self._local_BDD.add_user(liste_cit['user'][k])

            #self._local_BDD.add_message(user=liste_cit['user'][k], topic=topic, msg=liste_cit['msg'][k], toUser=liste_cit['touser'][k], date=liste_cit['date'][k], citation=0)

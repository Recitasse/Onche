import requests
import datetime
import sys
import time

import numpy as np

from bs4 import BeautifulSoup
from prettytable import PrettyTable

from utils.graphics import bar_etape
from utils.fonction import conversion

class Onche:
    def __init__(self):
        # public
        self.essais_max = 100
        self.delais = 1
        self.url = "https://onche.org/forum/1/blabla-general"

        # private
        self.DATA = {'nom' : [], 'sujet' : [], 'nb' : [], 'lien' : []}
        self.DATA_MESS = []
        self.ListCite = []
        self.html_parser = ""

    def get_data(self, page_it:int=1) -> None:
        """
        Obtention des données \n 
        Renvoie le dict {'nom' : [], 'sujet' : [], 'nb' : [], 'lien' : []}
        """
        self.url = f"https://onche.org/forum/1/blabla-general/{page_it}"
        self.DATA = {'nom' : [], 'sujet' : [], 'nb' : [], 'lien' : []}
        self.DATA_MESS = []
        self.ListCite = []
        self.html_parser = ""
        self.essais_max = 100
        self.delais = 1
        
        reponse = requests.get(self.url)
        for essai in range(self.essais_max):
            if reponse.status_code == 200:       # Valide
                data = reponse.text
                self.html_parser = BeautifulSoup(data, "html.parser")

                # Class intéressantes 
                # Code à modifier suivant le forum
                # ===============================================================================
                topicNames = self.html_parser.find_all("div", class_="topic-username")
                nbMessageTopic = self.html_parser.find_all("span", class_="topic-nb")
                titreTopic = self.html_parser.find_all("a", class_="topic-subject link")
                lienTopic = self.html_parser.find_all("a", class_="topic-subject link")
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
                # ================================================================================
            # Trop de demande
            elif reponse.status_code == 503:  
                print(f"Trop de demande ! (essais {essai+1}/{self.essais_max})")
                time.sleep(self.delais)
            elif reponse.status_code == 404:
                print(f"Topic supprimé !")
                return
            # Si erreur de connexion

    def get_messages(self, lien:str, nbpstart:int, nbpstop:int) -> dict:
        """
        On veut obtenir les messages, mais pas que :
        Le nom de l'user, s'il répond à qqn, son message et sa date de publication.

        Pour cela on a besoin du lien, du nombre de message et la date de publipostage des anciens.

        Args:
            lien (string) : mettre le lien du topic
            nbpstart (int) : la page de départ (là où commence le scrap)
            nbpstop (int) : page de stop (dernière page recensée)

        Return:
            list -> DATA_MESS = [[{'user' :  [], 'msg' :  [],'touser' : [], 'date' : [], 'page': 1}],[],[],...,[{... 'page':n}]]

        Note, on peut vérifier la page, où : DATA_MESS[0] = DATA_MESS[0]['page'] 
        """
        self.DATA_MESS = []
        self.ListCite = []
        self.ListBadges = []
        it = 0
        for i in range(nbpstart+1, nbpstop+1):
            # Liste complète des data
            bar_etape(nbpstop-nbpstart, it)
            # On se connecte à la page
            self.url = str(lien)+"/"+str(i)
            reponse = requests.get(self.url)
            time.sleep(1) # arrêt de 0.5s pour éviter de surcharger le serveur
            Index = []
            
            for essai in range(self.essais_max):
                if reponse.status_code == 200:       # Valide
                    data = reponse.text
                    self.html_parser = BeautifulSoup(data, "html.parser")

                    # Class intéressantes 
                    # Code à modifier suivant le forum
                    liste_message = {'user' :  [], 'msg' :  [],'touser' : [], 'date' : [], 'badguser' : [], 'cite_state':[], 'page': i-1}
                    liste_cit = {'user' :  [], 'msg' :  [],'cite' : [], 'date' : [], 'page': i-1}
                
                    # Obtention de la liste des messages
                    old_username = ""
                    MESS = self.html_parser.find_all("div", class_="message")
                    for mes in MESS:
                        # Obtention des (réponses s'il y en a)
                        rep = mes.find("div", class_="message answer")  # Find only the first occurrence
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
                        cond = True
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
                            print(f"x Erreur : {e}. La date est indisponible.")
                            return 

                        liste_message["msg"].append(msg)
                        
                           

                        # On récupère les badges des onchois
                        badges_loc = mes.find("div", class_="message-badges")
                        badges = badges_loc.find_all("img", class_="icon")
                        #print(f"{liste_message['user'][k]} a {len(badges)}, {[badge.get('alt') for badge in badges]}")
                        liste_message['badguser'].append([badge.get('alt') for badge in badges])

                        # On récupère les citations manuelles
                        for citations in mes.find_all("div", class_="signature"):
                            citations.extract()


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

                        k+=1

                    it+=1
                    self.DATA_MESS.append(liste_message)
                    break
                        
                    # ================================================================================
                # Trop de demande
                elif reponse.status_code == 503:  
                    print(f"Trop de demande ! (essais {essai+1}/{self.essais_max})")
                    time.sleep(self.delais)
                elif reponse.status_code == 404:
                    print(f"Topic supprimé !")
                    return
                # Si erreur de connexion

        return self.DATA_MESS, self.ListCite

    def afficher(self):
        """
        Affiche le tableau des informations récupérées
        """
        print(f"Actualisation du \033[1m{datetime.datetime.now()}\033[0m")
        table = PrettyTable()
        table.field_names = ["Nom", "Titre du topic", "Nb msg"]

        for i in range(len(self.DATA['nom'])):
            table.add_row([self.DATA['nom'][i], self.DATA['sujet'][i], self.DATA['nb'][i]])
        print(table)
        print("\n")

    def get_badges(self, nom:str) -> None:
        """
        Obtention des badges de l'utilisateurs

        Args:
            nom (string) : nom de l'utilisateur
            main (bool) : si True (on récupère via le topic)
            parser (string) : text du parser (via message)
        """
        # Via l'accession au topic
        url_badge = f"https://onche.org/profil/{nom}"
        reponse = requests.get(url_badge)
        time.sleep(0.3)
        for essai in range(self.essais_max):
            if reponse.status_code == 200:       # Valide
                data = reponse.text
                self.html_parser = BeautifulSoup(data, "html.parser")

                # Class intéressantes 
                # Code à modifier suivant le forum
                # ===============================================================================
                badges = self.html_parser.find_all("img", class_="icon")

                # Récupération des noms
                badgeListUser = []
                for badge in badges:
                    badgeListUser.append(badge.get('alt'))
                return badgeListUser
                # ================================================================================
            elif reponse.status_code == 503:        # Si trop de demande
                print(f"Trop de demande ! (essais {essai+1}/{self.essais_max})")
                time.sleep(self.delais)
            elif reponse.status_code == 404:
                print(f"Topic supprimé !")
                return

    def reset(self):
        """
        Reset la class
        """
        self.DATA = {'nom' : [], 'sujet' : [], 'nb' : [], 'lien' : []}
        self.ListCite = []
        self.html_parser = ""

    def reset_time(self):
        """Obtention du temsp de rafraichissement de la première page"""
        lastTopic = self.html_parser.find_all("a", class_="right")
        Temps = []
        for spanElement in lastTopic:
            spanText = spanElement.get_text(strip=True)
            Temps.append(conversion(spanText))
        return Temps[-1]//2

    @staticmethod
    # Nettoie l'array des réponses
    def nettoie(rep:list)->list:
        new_list = []
        for i in range(len(rep) - 1):
            if rep[i] == 0 and rep[i + 1] == 1:
                continue
            new_list.append(rep[i])
        new_list.append(rep[-1])
        return new_list

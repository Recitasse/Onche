import numpy as np
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import json

parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(parent)

from BDD.bdd import BDD
from config.Variables.variables import *


class ONCHISATEUR:
    def __init__(self, user: int | str, database: str = MYSQL_DATABASE, verbose: bool = False) -> None:
        # futur
        self._database = database
        self._verbose = verbose
        self._local_BDD = BDD(user=MYSQL_USER, database=self._database, verbose=self._verbose)

        # public
        if isinstance(user, str):
            user = self._local_BDD.user_name2id(user)
        self.queries = ONCHISATEUR_QUERIES

        # private
        self._queries = self._get_queries()

        # Initialisation via la base de donnée (données élémentaires)
        DATA = self._local_BDD.QUERY(self._queries['info']['all'], (user,))
        self.id = DATA[0]
        self.nom = DATA[1]
        self.sexe = DATA[2]
        self.age = DATA[3]
        self.QI = DATA[4]
        self.qualite = DATA[5]
        del DATA

        # Onchois liens
        self.Lien_int = {}
        self.Lien_ext_f = {}

        # Les topics
        self.topicListe = self._local_BDD.QUERY(self._queries['info']['topics'], (user,))

        # Les messages
        self.topicListe = self._local_BDD.QUERY(self._queries['info']['messages'], (user,))

        # Les badges
        self.badgesListe = self._local_BDD.QUERY(self._queries['info']['badges'], (user,))

    def _get_queries(self):
        """obtiens les queries stocker via leurs clés"""
        with open(self.queries, 'r', encoding="utf-8") as QU:
            return json.load(QU)
        
    def get_Onchois(self, jour:int=7, limit:int=10):
        """
        Donne le nombre d'onchois sur le fofo
    
        Args:
            jour (int) : qui à poster sur un intervalle de J jours
            limit (int) : limit messages
        
        Soit selectionner un onchois qui a poste au moins limit messages sur J jours
        """
        return self._local_BDD.get_results(self._queries['ActiveUserDate'], params=(jour,limit,), ind_="all")

    def relation_sociale_onchienne(self, seuil_rep:int=2, seuil_topic:int=5, nb_jour:int=365):
        """
        Permet d'obtenir le lien qui uni un onchiens et le reste de la communauté

        Args:
            seuil_rep (int) : le nombre de message seuil (pour être considéré comme ayant un lien)
            seuil_topic (int) : le nombre de topic visité par l'utilisateur (et ayant au moins posté seuil_rep messages)
            nb_jour (int) : l'interval de jour
        """
        # Constellation interne
        print("Constellation interne:")
        self.Lien_int = {'onchois': [], 'nbmsg': []}
        N = len(self.get_Onchois(jour=365, limit=5))
        for k in range(N):
            if k-1!= self.id:
                DATA = self._local_BDD.QUERY(self._queries['ToUser'], (self.id,self.id,self.id,k-1,k-1,self.id,nb_jour,seuil_rep,))
                if DATA != []:
                    print(f"\t{DATA}")
                    self.Lien_int['onchois'].append(DATA[0])
                    self.Lien_int['nbmsg'].append(DATA[1])

        # Constellation externe
        print("\nConstellation interne:")
        Lien_ext = {'onchois' : [], 'RapNbMsg': [], 'titre' : []}
        for k in range(1,N):
            if k-1 != self.id:
                DATA = self._local_BDD.QUERY(self._queries['ConstInt'], (self.id,k-1,nb_jour,seuil_topic,))
                if DATA != []:
                    print(f"\t{DATA}")
                    DATA[0] = self._local_BDD.user_id2name(DATA[0])
                    Lien_ext['onchois'].append(DATA[0])
                    Lien_ext['RapNbMsg'].append(DATA[3])
                    Lien_ext['titre'].append(DATA[1])
                    
        # Supression des liens
        Ind = []
        self.Lien_ext_f = {'onchois' : [], 'RapNbMsg': [], 'titre' : []}
        for i in range(len(Lien_ext['onchois'])):
            if Lien_ext['onchois'][i] not in self.Lien_int['onchois']:
                Ind.append(i)
        for i in Ind:
            self.Lien_ext_f['onchois'].append(Lien_ext['onchois'][i])
            self.Lien_ext_f['RapNbMsg'].append(Lien_ext['RapNbMsg'][i])
            self.Lien_ext_f['titre'].append(Lien_ext['titre'][i])
    
    def relation(self):

        list1 = [(id_, nb_msg) for id_, nb_msg in zip(self.Lien_int['onchois'], self.Lien_int['nbmsg'])]
        list2 = [(id_, nb_msg) for id_, nb_msg in zip(self.Lien_ext_f['onchois'], self.Lien_ext_f['RapNbMsg'])]
        list3_center = (self.nom, self._local_BDD.get_results(self._queries['user']['message_user'], params=(self.id,)))

        # Normalisation des poids
        m_w = np.max(self.Lien_int['nbmsg'] + self.Lien_ext_f['RapNbMsg'] + [list3_center[1]])
        print(list1)

        G = nx.Graph()

        for user, weight in list1:
            G.add_node(user, color='blue', weight=int(1000*weight/m_w))

        for user, weight in list2:
            G.add_node(user, color='yellow', weight=int(1000*weight/m_w))

        # noeud central
        user_center, weight_center = list3_center
        G.add_node(user_center, color='red', weight=int(1000*weight_center/m_w))

        fig = plt.figure(figsize=(15, 15), dpi=300, facecolor='black')

        # Ajout des liens
        for user, _ in list1 + list2:
            edge_weight = G.nodes[user]['weight']
            G.add_edge(user_center, user, weight=int(edge_weight/100))

        # Couleur, taille
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        node_sizes = [G.nodes[node]['weight']*5 for node in G.nodes()]
        alpha_values = [al/5000 for al in node_sizes]
        edge_weights = [G[u][v]['weight']*2 for u, v in G.edges()]
        edge_colors = [G.nodes[node]['color'] for node in G.nodes()]
        font_sizes = [G.nodes[node]['weight'] for node in G.nodes()]

        # Réajustement des labels
        font_sizes_label = []
        al = 0.8
        for i in range(len(font_sizes)):
            font_sizes_label.append(15*(np.log(al*font_sizes[i]) - np.log(1)) / (np.log(al*np.max(font_sizes))) - np.log(1))

            num_list1 = len(list1)
            num_list2 = len(list2)
            radius_list1 = 2.2
            radius_list2 = 3.0
            angle_list1 = np.linspace(0, 2*np.pi, num_list1, endpoint=False)
            angle_list2 = np.linspace(0, 2*np.pi, num_list2, endpoint=False)

            pos_list1 = {user: (radius_list1 * np.cos(angle), -radius_list1 * np.sin(angle)) for user, angle in zip([user for user, _ in list1], angle_list1)}
            pos_list2 = {user: (radius_list2 * np.cos(angle), radius_list2 * np.sin(angle)) for user, angle in zip([user for user, _ in list2], angle_list2)}

            # Merge
            pos = {**pos_list1, **pos_list2}
            # Positions centrale du noeud principal
            pos[user_center] = (0, 0)

        print(node_sizes, node_colors)
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)

        # Mettre le bon alpha

        node_labels = {node: node for node in G.nodes()}
        it_size = 0
        for key, value in node_labels.items():
            if font_sizes_label[it_size] < 3:
                font_sizes_label[it_size] = 3
            nx.draw_networkx_labels(
                G, 
                pos, 
                labels={key : value}, 
                font_size=font_sizes_label[it_size], 
                font_color='white', 
                font_weight="bold", 
                verticalalignment='bottom')
            it_size+=1

        plt.axis('off')
        plt.savefig("test.png",format="png")

Emiliano = ONCHISATEUR('Recitasse')
Emiliano.relation_sociale_onchienne(seuil_rep=2, seuil_topic=2)
Emiliano.relation()
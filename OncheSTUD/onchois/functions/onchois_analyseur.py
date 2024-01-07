import numpy as np
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import json

parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(parent)
print(parent)

from BDD.bdd import BDD

class ONCHISATEUR:
    def __init__(self, id:int=None, nom:str="") -> None:
        self.nom = nom
        self.id = id

        # Initialisation via la base de donnée
        query = "SELECT * FROM onchois WHERE onchois_id = %s OR onchois_nom = %s;"
        DATA = bdd.QUERY(query, (self.id, self.nom,))

        self.id = DATA[0]
        self.nom = DATA[1]
        self.sexe = DATA[2]
        self.age = DATA[3]
        self.QI = DATA[4]
        self.qualite = DATA[5]
        self.Lien_int = {}
        self.Lien_ext_f = {}

        # Les topics
        query = "SELECT * FROM topic WHERE topic_user = %s;"
        DATA = bdd.QUERY(query, (self.id,))
        self.topicListe = DATA

        # Les messages
        query = "SELECT message_message FROM messages WHERE message_user = %s;"
        DATA = bdd.QUERY(query, (self.id,))
        self.topicListe = DATA

        # Les badges
        query = "SELECT b.badges_nom FROM badges b JOIN onchois_badges ob ON b.badges_id = ob.ob_badgeid WHERE ob.ob_userid = %s;"
        DATA = bdd.QUERY(query, (self.id,))
        self.badgesListe = DATA

    def relation_sociale_onchienne(self, seuil_rep:int=2, seuil_topic:int=5, nb_jour:int=365):
        """
        Permet d'obtenir le lien qui uni un onchiens et le reste de la communauté

        Args:
            seuil_rep (int) : le nombre de message seuil (pour être considéré comme ayant un lien)
            seuil_topic (int) : le nombre de topic visité par l'utilisateur (et ayant au moins posté seuil_rep messages)
            nb_jour (int) : l'interval de jour
        """

        # QUery sélectionnant le toUser si dans un interval de J jour et si X réponses ont été faite
        query = """
                    SELECT
                        o.onchois_nom,
                        COUNT(*) AS message_count
                    FROM
                        messages m
                    JOIN
                        onchois o ON (m.message_user = o.onchois_id AND o.onchois_id != %s) OR
                                    (m.message_toUser = o.onchois_id AND o.onchois_id != %s)
                    WHERE
                        (m.message_user = %s AND m.message_toUser = %s) OR
                        (m.message_user = %s AND m.message_toUser = %s)
                        AND m.message_date >= DATE_SUB(NOW(), INTERVAL %s DAY) AND m.message_date <= NOW()
                    GROUP BY
                        o.onchois_nom, m.message_user, m.message_toUser
                    HAVING
                        COUNT(*) >= %s;
                """

        # Constellation interne
        self.Lien_int = {'onchois': [], 'nbmsg': []}
        N = len(bdd.get_Onchois(jour=365, limit=5))
        for k in range(N):
            if k-1!= self.id:
                DATA = bdd.QUERY(query, (self.id,self.id,self.id,k-1,k-1,self.id,nb_jour,seuil_rep,))
                if DATA:
                    self.Lien_int['onchois'].append(DATA[0])
                    self.Lien_int['nbmsg'].append(DATA[1])

        query = """
                    SELECT
                        t.topic_user,
                        t.topic_nom,
                        t.topic_message,
                        COUNT(*) AS message_count
                    FROM
                        messages m
                    JOIN
                        onchois o ON (m.message_user = o.onchois_id)
                    JOIN
                        topic t ON m.message_topic = t.id_topic
                    WHERE
                        m.message_user = %s AND t.topic_user = %s AND
                        m.message_date >= DATE_SUB(NOW(), INTERVAL %s DAY) AND m.message_date <= NOW()
                    GROUP BY
                        t.topic_user, t.topic_nom, t.topic_message, o.onchois_nom
                    HAVING
                        COUNT(*) >= %s;
                """
        # Constellation externe
        Lien_ext = {'onchois' : [], 'RapNbMsg': [], 'titre' : []}
        for k in range(1,N):
            if k-1 != self.id:
                DATA = bdd.QUERY(query, (self.id,k-1,nb_jour,seuil_topic,))
                if DATA:
                    DATA[0] = bdd.convertId(DATA[0]).decode('utf-8')
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
    
    def relation(self, color:str="blue", color2:str="yellow"):

        list1 = [(x, y) for x, y in zip(self.Lien_int['onchois'], self.Lien_int['nbmsg'])]
        list2 = [(x, y) for x, y in zip(self.Lien_ext_f['onchois'], self.Lien_ext_f['RapNbMsg'])]
        list3_center = (self.nom, bdd.get_NbMsgOnchois(self.nom))

        G = nx.Graph()

        for user, weight in list1:
            G.add_node(user, color='blue', weight=weight)

        for user, weight in list2:
            G.add_node(user, color='yellow', weight=weight)

        user_center, weight_center = list3_center
        G.add_node(user_center, color='red', weight=weight_center)  # Central node

        fig = plt.figure(figsize=(15, 15), dpi=300, facecolor='black')

        # Add edges from the central node to other nodes
        for user, _ in list1 + list2:
            edge_weight = G.nodes[user]['weight'] / weight_center  # Calculate edge weight
            G.add_edge(user_center, user, weight=edge_weight)      # Add edge with calculated weight

        # Prepare node colors, sizes, and edge attributes for visualization
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        node_sizes = [G.nodes[node]['weight']*5 for node in G.nodes()]
        edge_weights = [G[u][v]['weight']*20 for u, v in G.edges()]
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

            # Merge positions
            pos = {**pos_list1, **pos_list2}
            pos[user_center] = (0, 0)  # Set the position for the central node

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color=edge_colors, alpha=0.5, arrows=True,connectionstyle="arc3,rad=0.3")

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

        plt.axis('off')  # Turn off axis
        plt.savefig("test.png",format="png")
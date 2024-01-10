import numpy as np
import os
import sys
from prettytable import PrettyTable
from __FONC__ import graphique

parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(parent)

from BDD.bdd import BDD
from config.Variables.variables import *

bs = "\033[1m"; bf = "\033[0m"

def congruence_topic(nb_jour,mess_s, liste_mot, nom, title, k, alp_p, size_font, coef, size, min_dist):

    print("Connexion à la base de donnée: ")
    bdd = BDD()
    print(f"-> {bs}'Done'{bf}")
    mots = '|'.join(liste_mot)

    print("Récupération des topics : ")
    query = "SELECT topic_nom FROM topic WHERE topic_nom REGEXP %s AND topic_date >= DATE_SUB(CURRENT_DATE(), INTERVAL %s DAY);"
    params = (mots, nb_jour,)
    TOPIC = bdd.QUERY(query, values=params)

    TOPIC = [bdd.topic_name2id(el) for el in TOPIC]
    print(f"{bs}'Done'{bf}")
    # Pour les réponses dans les topics
    print(f"Récupération des messages entre utilisateur (sur {nb_jour}) : ")
    query = """
                SELECT
                    m.message_user,
                    m.message_toUser,
                    COUNT(m.id_message) AS count_message_message
                FROM
                    `Onche`.`messages` m
                    JOIN `Onche`.`topic` t ON m.message_topic = t.id_topic
                WHERE
                    t.id_topic = %s
                    AND m.message_toUser IS NOT NULL
                GROUP BY
                    m.message_user, m.message_toUser;
            """
    INT = []
    for val in TOPIC:
        data = bdd.QUERY(query, values=(val,), type_="all")
        INT.append(data)
    print(f"Relation interne : {bs}'Done'{bf}")

    # Pour les messages dans le topic
    query = """
                SELECT
                    m.message_user,
                    COUNT(m.id_message) AS count_message_message
                FROM
                    `Onche`.`messages` m
                    JOIN `Onche`.`topic` t ON m.message_topic = t.id_topic
                WHERE
                    t.id_topic = %s
                    AND m.message_toUser IS NULL
                GROUP BY
                    m.message_user;
            """
    REP = []
    for val in TOPIC:
        data = bdd.QUERY(query, values=(val,), type_="all")
        print(data)
        REP.append(data)
    print(f"Relation externe : {bs}'Done'{bf}")

    dict_ext = {'user': [], 'mess':[]}
    dict_int = {'user': [], 'touser':[], 'mess':[]}

    print("Préparation des données...")
    for topic_mess in REP:
        if topic_mess:
            print(topic_mess)
            for i in range(len(topic_mess)):
                print(topic_mess)
                dict_ext['user'].append(bdd.user_id2name(topic_mess[i][0]))
                dict_ext['mess'].append(topic_mess[i][1])


    for topic_mess in INT:
        if topic_mess:
            for i in range(len(topic_mess)):
                dict_int['user'].append(bdd.user_id2name(topic_mess[i][0]))
                dict_int['touser'].append(bdd.user_id2name(topic_mess[i][1]))
                dict_int['mess'].append(topic_mess[i][2])

    # Pour avoir la matrice des liens ------------------------------------------------
    combined_users = dict_int['user'] + dict_ext['user']
    combined_messages = dict_int['mess'] + dict_ext['mess']

    user_message_counts = {}
    for user, mess in zip(combined_users, combined_messages):
        if user in user_message_counts:
            user_message_counts[user] += mess
        else:
            user_message_counts[user] = mess
    
    print(f"{bs}'Done'{bf}")
    print(f"Filtrage des utilisateurs, seuil de {mess_s} messages : ")
    # Filtrage des utilisateurs (retir les occasionnels)
    removed_keys = []
    filtered_data = {}
    for key, value in user_message_counts.items():
        if value >= mess_s:
            filtered_data[key] = value
        else:
            removed_keys.append(key)
    user_message_counts = filtered_data
    
    print("Supression des utilisateurs suivant : ")
    for el in removed_keys:
        print(f"\t {el}")

    print("Préparation du grahique : ")
    # Create a dictionary to map users to matrix indices
    user_index_mapping = {user: index for index, user in enumerate(user_message_counts)}
    print("-> Mapping user")

    # Create an empty weighted adjacency matrix
    num_users = len(user_message_counts)
    adjacency_matrix = np.zeros((num_users, num_users), dtype=int)

    # Populate the adjacency matrix with message counts
    for user, touser, mess in zip(dict_int['user'], dict_int['touser'], dict_int['mess']):
        if user in user_index_mapping and touser in user_index_mapping:
            user_index = user_index_mapping[user]
            touser_index = user_index_mapping[touser]
            adjacency_matrix[user_index][touser_index] += mess

    LINK = np.array(adjacency_matrix)
    print("-> Matrice des liens")
    labels = []
    weight_nodes = []
    for user, count in user_message_counts.items():
        labels.append(user)
        weight_nodes.append(count)
    print("-> Importance des utilisateurs")

    # Mise à l'échelle
    for i in range(len(labels)):
        data = 0
        query = """
                SELECT COUNT(*) AS topic_count
                FROM topic
                WHERE topic_user = %s
                AND id_topic IN ({})
                """.format(', '.join(['%s'] * len(TOPIC)))

        rep = bdd.QUERY(query, values=(bdd.user_name2id(labels[i]),) + tuple(TOPIC))
        if rep:
            data = rep[0]

        def msg_in_topic(id_user, TOPIC):
            query = """
                    SELECT COUNT(*) AS message_count
                    FROM messages
                    WHERE message_user = %s
                    AND message_topic IN ({})
                    """.format(', '.join(['%s'] * len(TOPIC)))
            rep = bdd.get_results(query, params=((id_user,)) + tuple(TOPIC))
            return rep

        weight_nodes[i] = (msg_in_topic(bdd.user_name2id(labels[i]), TOPIC)*5 + data*10)*5

        label_weight_pairs = list(zip(labels, weight_nodes))
        label_weight_pairs.sort(key=lambda pair: pair[1], reverse=False)

    print("Table des poids : ")
    table = PrettyTable()
    table.field_names = [f"{bs}Onchois{bf}", f"{bs}Importance{bf}"]

    for label, weight in label_weight_pairs:
        table.add_row([label, weight])
    print(table)

    N = len(labels)
    print("Création du dossier : ")
    if not os.path.exists(f"{GLOBAL_PATH}/OncheSTUD/communautes/Sujet/{nom}"):
        os.mkdir(f"{GLOBAL_PATH}/OncheSTUD/communautes/Sujet/{nom}")
    print(f"{bs}'Done'{bf}")

    print("Sauvegarde des prompts : ")
    with open(f"{GLOBAL_PATH}/OncheSTUD/communautes/Sujet/{nom}/prompt_{nom}.txt","w") as f:
        for el in liste_mot:
            f.write(el)
            f.write(', ')
        f.close()
    print(f"{bs}'Done'{bf}")

    graphique(labels, weight_nodes, LINK, N, nom=nom, title=title, k=k, alp_p=alp_p, size_font=size_font, dec=1, coef=coef, size=size, min_dist=min_dist)
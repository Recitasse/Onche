from dataclasses import dataclass, field, InitVar
from datetime import datetime
from typing import Tuple, List
from bin.WebScrapper.OncheScrapper.req import Requests
import os
from config.variables import DOCS_PATH
import json


@dataclass(init=False)
class Connexion:
    @staticmethod
    def get_connexion() -> Tuple[str, List[str]]:
        json = Requests().req_html("https://onche.org/user/logged", json_mode=True)
        date = datetime.now().strftime("%H:%M:%S")
        return date, [el['username'] for el in json]

    @staticmethod
    def update_connexion() -> None:
        """
        Modifie le dumps du json des connexion
        Returns: None
        """
        with open(os.path.join(DOCS_PATH, "connexion/liste_connexion.json"), 'r', encoding="utf-8") as data:
            col = json.load(data)

        n_date, new_data = Connexion.get_connexion()

        with open(os.path.join(DOCS_PATH, "connexion/liste_connexion.json"), 'r', encoding="utf-8") as w:
            writer = json.load(w)
            # Ajout de l'heure dans le JSON
            if n_date not in list(writer.keys()):
                col.update({n_date: {}})

            for user in new_data:
                if user not in col[n_date].keys():
                    col[n_date].update({user: 1})
                else:
                    col[n_date] = {user: col[n_date][user]+1}

        with open(os.path.join(DOCS_PATH, "connexion/liste_connexion.json"), 'w', encoding="utf-8") as f:
            f.write(json.dumps(col, indent=6))



print(Connexion.update_connexion())

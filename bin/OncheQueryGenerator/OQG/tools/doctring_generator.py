from dataclasses import dataclass, field
from typing import Union, List, Tuple, Any


@dataclass(slots=True, repr=False, order=False, init=False)
class DocstringGenerator:
    """
    Génère les docstrings des fonctions auto-générées
    """
    @staticmethod
    def generate_params(params: List[Any]) -> str:
        """
        Prend les paramètres de la fonction pour rendre le tout au format reSutructuredText
        :param params: Liste des paramètres
        :return: Le string des paramètres
        """
        pass

    @staticmethod
    def generate_description(table: str, operation: str, row: Union[str, None] = None) -> str:
        """
        Génère la description générale en fonction de la table de l'opération et de la ligne
        :param table: nom de la table
        :param operation: l'opération effectuée
        :param row: nom de la ligne
        :return: La description
        """
        pass

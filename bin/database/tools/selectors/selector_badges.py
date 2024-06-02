"""==================================================
   Python class BadgesBdd générée par OQG BDD TOOLS GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 17:14:40.515389
=================================================="""

import datetime

from dataclasses import dataclass

from bin.database.tools.entities.Badges import Badges

from bin.database.bbd import Link


@dataclass(init=False)
class BadgesBdd(Link):
    def is_in_id(self, id_: int) -> bool:
        query = "SELECT * FROM badges WHERE badges_id = %s;"
        params = (id_,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'badges {id_} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Badges {id_} n'est pas dans la base de donnée.")
        return False

    def is_in_nom(self, nom: str) -> bool:
        query = "SELECT * FROM badges WHERE badges_nom = %s;"
        params = (nom,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'badges {nom} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Badges {nom} n'est pas dans la base de donnée.")
        return False


    def add_badges(self, nom: str) -> None:
        query = 'INSERT INTO badges (badges_nom);'
        params = (nom,)
        if not self.is_in_nom(nom):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'badges {nom} existe')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def update_badges_nom(self, id_: int, nom: str) -> None:
        query = "UPDATE badges SET badges_nom = %s WHERE badges_id = %s;"
        params = (id_, nom)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de nom de badges effectué par {nom}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def delete_badges_id(self, id_: int) -> None:
        query = "DELETE FROM badges WHERE badges_id = %s;"
        params = (id_,)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Suppression de id de badges effectué')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def id2nom(self, id_: int) -> str:
        query = 'SELECT badges_nom FROM badges WHERE badges_id = %s;'
        params = (id_,)
        return self.get_results(query, params)


    def get_badges_id(self, id_: int) -> Badges:
        query = 'SELECT * FROM badges WHERE badges_id = %s;'
        params = (id_,)
        return Badges(*self.get_results(query, params, ind_='all'))

    def get_badges_nom(self, nom: str) -> Badges:
        query = 'SELECT * FROM badges WHERE badges_nom = %s;'
        params = (nom,)
        return Badges(*self.get_results(query, params, ind_='all'))


    def get_badges_from_id(self, from_: list | tuple, to_: list | tuple) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id BETWEEN % AND %;'
        params = (from_, to_,)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]

    def get_badges_ge_id(self, to_: int) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id >= %s;'
        params = (to_,)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]

    def get_badges_eq_id(self, to_: int) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id == %s;'
        params = (to_,)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]

    def get_badges_ne_id(self, to_: int) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id <> %s;'
        params = (to_,)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]

    def get_badges_gt_id(self, to_: int) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id > %s;'
        params = (to_,)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]

    def get_badges_le_id(self, to_: int) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id =< %s;'
        params = (to_,)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]

    def get_badges_lt_id(self, to_: int) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id < %s;'
        params = (to_,)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]

    def get_badges_in_id(self, list_: list | tuple) -> list[Badges]:
        query = f'SELECT * FROM badges WHERE badges_id IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Badges(*row) for row in self.get_results(query, params, ind_='all')]


    def get_badges_like_start_nom(self, deb: str) -> list:
        query = f"SELECT * FROM badges WHERE badges_nom LIKE '{deb}%';"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_like_between_nom(self, deb: str, fin: str) -> list:
        query = f"SELECT * FROM badges WHERE badges_nom LIKE '{deb}%{fin}';"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_like_end_nom(self, fin: str) -> list:
        query = f"SELECT * FROM badges WHERE badges_nom LIKE '%{fin}';"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_like_mid_nom(self, mil: str) -> list:
        query = f"SELECT * FROM badges WHERE badges_nom LIKE '%{mil}%';"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_regexp_nom(self, text: str) -> list:
        query = f"SELECT * FROM badges WHERE badges_nom REGEXP '{text}';"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_instr_lt_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM badges WHERE INSTR(badges_nom, '{text}') < {occ};"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_instr_gt_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM badges WHERE INSTR(badges_nom, '{text}') > {occ};"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_instr_le_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM badges WHERE INSTR(badges_nom, '{text}') <= {occ};"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_instr_ge_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM badges WHERE INSTR(badges_nom, '{text}') >= {occ};"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_instr_eq_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM badges WHERE INSTR(badges_nom, '{text}') == {occ};"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_badges_instr_ne_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM badges WHERE INSTR(badges_nom, '{text}') <> {occ};"
        return [Badges(*row) for row in self.get_results(query, params=(), ind_='all')]


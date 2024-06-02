"""==================================================
   Python class StickersBdd générée par OQG BDD TOOLS GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 17:14:40.514795
=================================================="""

import datetime

from dataclasses import dataclass

from bin.database.tools.entities.Stickers import Stickers

from bin.database.bbd import Link


@dataclass(init=False)
class StickersBdd(Link):
    def is_in_id(self, id_: int) -> bool:
        query = "SELECT * FROM stickers WHERE stickers_id = %s;"
        params = (id_,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'stickers {id_} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Stickers {id_} n'est pas dans la base de donnée.")
        return False

    def is_in_nom(self, nom: str) -> bool:
        query = "SELECT * FROM stickers WHERE stickers_nom = %s;"
        params = (nom,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'stickers {nom} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Stickers {nom} n'est pas dans la base de donnée.")
        return False


    def add_stickers(self, nom: str, collection: int) -> None:
        query = 'INSERT INTO stickers (stickers_nom, stickers_collection);'
        params = (nom, collection,)
        if not self.is_in_nom(nom):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'stickers {nom} existe')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def update_stickers_nom(self, id_: int, nom: str) -> None:
        query = "UPDATE stickers SET stickers_nom = %s WHERE stickers_id = %s;"
        params = (id_, nom)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de nom de stickers effectué par {nom}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_stickers_collection(self, id_: int, collection: int) -> None:
        query = "UPDATE stickers SET stickers_collection = %s WHERE stickers_id = %s;"
        params = (id_, collection)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de collection de stickers effectué par {collection}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def delete_stickers_id(self, id_: int) -> None:
        query = "DELETE FROM stickers WHERE stickers_id = %s;"
        params = (id_,)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Suppression de id de stickers effectué')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def id2nom(self, id_: int) -> str:
        query = 'SELECT stickers_nom FROM stickers WHERE stickers_id = %s;'
        params = (id_,)
        return self.get_results(query, params)


    def get_stickers_id(self, id_: int) -> Stickers:
        query = 'SELECT * FROM stickers WHERE stickers_id = %s;'
        params = (id_,)
        return Stickers(*self.get_results(query, params, ind_='all'))

    def get_stickers_nom(self, nom: str) -> Stickers:
        query = 'SELECT * FROM stickers WHERE stickers_nom = %s;'
        params = (nom,)
        return Stickers(*self.get_results(query, params, ind_='all'))


    def get_stickers_from_id(self, from_: list | tuple, to_: list | tuple) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id BETWEEN % AND %;'
        params = (from_, to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_from_collection(self, from_: list | tuple, to_: list | tuple) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection BETWEEN % AND %;'
        params = (from_, to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_ge_id(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id >= %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_ge_collection(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection >= %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_eq_id(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id == %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_eq_collection(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection == %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_ne_id(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id <> %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_ne_collection(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection <> %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_gt_id(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id > %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_gt_collection(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection > %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_le_id(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id =< %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_le_collection(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection =< %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_lt_id(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id < %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_lt_collection(self, to_: int) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection < %s;'
        params = (to_,)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_in_id(self, list_: list | tuple) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_id IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]

    def get_stickers_in_collection(self, list_: list | tuple) -> list[Stickers]:
        query = f'SELECT * FROM stickers WHERE stickers_collection IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Stickers(*row) for row in self.get_results(query, params, ind_='all')]


    def get_stickers_like_start_nom(self, deb: str) -> list:
        query = f"SELECT * FROM stickers WHERE stickers_nom LIKE '{deb}%';"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_like_between_nom(self, deb: str, fin: str) -> list:
        query = f"SELECT * FROM stickers WHERE stickers_nom LIKE '{deb}%{fin}';"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_like_end_nom(self, fin: str) -> list:
        query = f"SELECT * FROM stickers WHERE stickers_nom LIKE '%{fin}';"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_like_mid_nom(self, mil: str) -> list:
        query = f"SELECT * FROM stickers WHERE stickers_nom LIKE '%{mil}%';"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_regexp_nom(self, text: str) -> list:
        query = f"SELECT * FROM stickers WHERE stickers_nom REGEXP '{text}';"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_instr_lt_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM stickers WHERE INSTR(stickers_nom, '{text}') < {occ};"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_instr_gt_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM stickers WHERE INSTR(stickers_nom, '{text}') > {occ};"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_instr_le_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM stickers WHERE INSTR(stickers_nom, '{text}') <= {occ};"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_instr_ge_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM stickers WHERE INSTR(stickers_nom, '{text}') >= {occ};"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_instr_eq_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM stickers WHERE INSTR(stickers_nom, '{text}') == {occ};"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_stickers_instr_ne_nom(self, text: str, occ: int) -> list:
        query = f"SELECT * FROM stickers WHERE INSTR(stickers_nom, '{text}') <> {occ};"
        return [Stickers(*row) for row in self.get_results(query, params=(), ind_='all')]


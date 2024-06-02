"""==================================================
   Python class OnchoisBdd générée par OQG BDD TOOLS GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 17:36:31.472089
=================================================="""

import datetime

from dataclasses import dataclass

from bin.database.tools.entities.Onchois import Onchois

from bin.database.bbd import Link


@dataclass(init=False)
class OnchoisBdd(Link):
    def is_in_id(self, id_: int) -> bool:
        query = "SELECT * FROM onchois WHERE onchois_id = %s;"
        params = (id_,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'onchois {id_} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Onchois {id_} n'est pas dans la base de donnée.")
        return False

    def is_in_nom(self, nom: str) -> bool:
        query = "SELECT * FROM onchois WHERE onchois_nom = %s;"
        params = (nom,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'onchois {nom} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Onchois {nom} n'est pas dans la base de donnée.")
        return False

    def is_in_oid(self, oid: int) -> bool:
        query = "SELECT * FROM onchois WHERE onchois_oid = %s;"
        params = (oid,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'onchois {oid} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Onchois {oid} n'est pas dans la base de donnée.")
        return False


    def add_onchois(self, oid: int, niveau: int, nom: str, message: int, date: datetime) -> None:
        query = 'INSERT INTO onchois (onchois_oid, onchois_niveau, onchois_nom, onchois_message, onchois_date);'
        params = (oid, niveau, nom, message, date,)
        if not self.is_in_oid(oid):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'onchois {oid} existe')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def update_onchois_oid(self, id_: int, oid: int) -> None:
        query = "UPDATE onchois SET onchois_oid = %s WHERE onchois_id = %s;"
        params = (id_, oid)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de oid de onchois effectué par {oid}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_onchois_niveau(self, id_: int, niveau: int) -> None:
        query = "UPDATE onchois SET onchois_niveau = %s WHERE onchois_id = %s;"
        params = (id_, niveau)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de niveau de onchois effectué par {niveau}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_onchois_nom(self, id_: int, nom: str) -> None:
        query = "UPDATE onchois SET onchois_nom = %s WHERE onchois_id = %s;"
        params = (id_, nom)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de nom de onchois effectué par {nom}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_onchois_sexe(self, id_: int, sexe: str) -> None:
        query = "UPDATE onchois SET onchois_sexe = %s WHERE onchois_id = %s;"
        params = (id_, sexe)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de sexe de onchois effectué par {sexe}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_onchois_age(self, id_: int, age: int) -> None:
        query = "UPDATE onchois SET onchois_age = %s WHERE onchois_id = %s;"
        params = (id_, age)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de age de onchois effectué par {age}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_onchois_qualite(self, id_: int, qualite: int) -> None:
        query = "UPDATE onchois SET onchois_qualite = %s WHERE onchois_id = %s;"
        params = (id_, qualite)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de qualite de onchois effectué par {qualite}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_onchois_message(self, id_: int, message: int) -> None:
        query = "UPDATE onchois SET onchois_message = %s WHERE onchois_id = %s;"
        params = (id_, message)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de message de onchois effectué par {message}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_onchois_date(self, id_: int, date: datetime) -> None:
        query = "UPDATE onchois SET onchois_date = %s WHERE onchois_id = %s;"
        params = (id_, date)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de date de onchois effectué par {date}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def delete_onchois_id(self, id_: int) -> None:
        query = "DELETE FROM onchois WHERE onchois_id = %s;"
        params = (id_,)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Suppression de id de onchois effectué')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def id2nom(self, id_: int) -> str:
        query = 'SELECT onchois_nom FROM onchois WHERE onchois_id = %s;'
        params = (id_,)
        return self.get_results(query, params)

    def id2oid(self, id_: int) -> int:
        query = 'SELECT onchois_oid FROM onchois WHERE onchois_id = %s;'
        params = (id_,)
        return self.get_results(query, params)


    def get_onchois_id(self, id_: int) -> Onchois:
        query = 'SELECT * FROM onchois WHERE onchois_id = %s;'
        params = (id_,)
        return Onchois(*self.get_results(query, params, ind_='all'))

    def get_onchois_nom(self, nom: str) -> Onchois:
        query = 'SELECT * FROM onchois WHERE onchois_nom = %s;'
        params = (nom,)
        return Onchois(*self.get_results(query, params, ind_='all'))

    def get_onchois_oid(self, oid: int) -> Onchois:
        query = 'SELECT * FROM onchois WHERE onchois_oid = %s;'
        params = (oid,)
        return Onchois(*self.get_results(query, params, ind_='all'))


    def get_onchois_from_id(self, from_: list | tuple, to_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id BETWEEN % AND %;'
        params = (from_, to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_from_oid(self, from_: list | tuple, to_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid BETWEEN % AND %;'
        params = (from_, to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_from_niveau(self, from_: list | tuple, to_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau BETWEEN % AND %;'
        params = (from_, to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_from_age(self, from_: list | tuple, to_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age BETWEEN % AND %;'
        params = (from_, to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_from_qualite(self, from_: list | tuple, to_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite BETWEEN % AND %;'
        params = (from_, to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_from_message(self, from_: list | tuple, to_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message BETWEEN % AND %;'
        params = (from_, to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_from_date(self, from_: list | tuple, to_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date BETWEEN % AND %;'
        params = (from_, to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ge_id(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id >= %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ge_oid(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid >= %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ge_niveau(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau >= %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ge_age(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age >= %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ge_qualite(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite >= %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ge_message(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message >= %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ge_date(self, to_: datetime) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date >= %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_eq_id(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id == %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_eq_oid(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid == %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_eq_niveau(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau == %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_eq_age(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age == %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_eq_qualite(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite == %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_eq_message(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message == %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_eq_date(self, to_: datetime) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date == %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ne_id(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id <> %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ne_oid(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid <> %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ne_niveau(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau <> %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ne_age(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age <> %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ne_qualite(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite <> %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ne_message(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message <> %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_ne_date(self, to_: datetime) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date <> %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_gt_id(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id > %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_gt_oid(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid > %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_gt_niveau(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau > %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_gt_age(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age > %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_gt_qualite(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite > %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_gt_message(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message > %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_gt_date(self, to_: datetime) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date > %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_le_id(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id =< %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_le_oid(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid =< %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_le_niveau(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau =< %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_le_age(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age =< %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_le_qualite(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite =< %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_le_message(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message =< %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_le_date(self, to_: datetime) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date =< %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_lt_id(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id < %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_lt_oid(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid < %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_lt_niveau(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau < %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_lt_age(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age < %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_lt_qualite(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite < %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_lt_message(self, to_: int) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message < %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_lt_date(self, to_: datetime) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date < %s;'
        params = (to_,)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_in_id(self, list_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_id IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_in_oid(self, list_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_oid IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_in_niveau(self, list_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_niveau IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_in_age(self, list_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_age IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_in_qualite(self, list_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_qualite IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_in_message(self, list_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_message IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]

    def get_onchois_in_date(self, list_: list | tuple) -> list[Onchois]:
        query = f'SELECT * FROM onchois WHERE onchois_date IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Onchois(*row) for row in self.get_results(query, params, ind_='all')]


    def get_onchois_like_start_nom(self, deb: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_nom LIKE '{deb}%';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_like_between_nom(self, deb: str, fin: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_nom LIKE '{deb}%{fin}';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_like_end_nom(self, fin: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_nom LIKE '%{fin}';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_like_mid_nom(self, mil: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_nom LIKE '%{mil}%';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_regexp_nom(self, text: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_nom REGEXP '{text}';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_lt_nom(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_nom, '{text}') < {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_gt_nom(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_nom, '{text}') > {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_le_nom(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_nom, '{text}') <= {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_ge_nom(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_nom, '{text}') >= {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_eq_nom(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_nom, '{text}') = {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_ne_nom(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_nom, '{text}') <> {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_like_start_sexe(self, deb: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_sexe LIKE '{deb}%';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_like_between_sexe(self, deb: str, fin: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_sexe LIKE '{deb}%{fin}';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_like_end_sexe(self, fin: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_sexe LIKE '%{fin}';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_like_mid_sexe(self, mil: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_sexe LIKE '%{mil}%';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_regexp_sexe(self, text: str) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE onchois_sexe REGEXP '{text}';"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_lt_sexe(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_sexe, '{text}') < {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_gt_sexe(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_sexe, '{text}') > {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_le_sexe(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_sexe, '{text}') <= {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_ge_sexe(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_sexe, '{text}') >= {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_eq_sexe(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_sexe, '{text}') = {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_onchois_instr_ne_sexe(self, text: str, occ: int) -> list[Onchois]:
        query = f"SELECT * FROM onchois WHERE INSTR(onchois_sexe, '{text}') <> {occ};"
        return [Onchois(*row) for row in self.get_results(query, params=(), ind_='all')]

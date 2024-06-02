"""==================================================
   Python class TopicBdd générée par OQG BDD TOOLS GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 17:34:58.677496
=================================================="""

import datetime

from dataclasses import dataclass

from bin.database.tools.entities.Topic import Topic

from bin.database.bbd import Link


@dataclass(init=False)
class TopicBdd(Link):
    def is_in_id(self, id_: None) -> bool:
        query = "SELECT * FROM topic WHERE topic_id = %s;"
        params = (id_,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'topic {id_} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Topic {id_} n'est pas dans la base de donnée.")
        return False

    def is_in_oid(self, oid: int) -> bool:
        query = "SELECT * FROM topic WHERE topic_oid = %s;"
        params = (oid,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'topic {oid} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Topic {oid} n'est pas dans la base de donnée.")
        return False


    def add_topic(self, oid: int, operateur: int, nom: str, date: datetime, message: int, lien: str, forum: int) -> None:
        query = 'INSERT INTO topic (topic_oid, topic_operateur, topic_nom, topic_date, topic_message, topic_lien, topic_forum);'
        params = (oid, operateur, nom, date, message, lien, forum,)
        if not self.is_in_oid(oid):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'topic {oid} existe')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def update_topic_oid(self, id_: None, oid: int) -> None:
        query = "UPDATE topic SET topic_oid = %s WHERE topic_id = %s;"
        params = (id_, oid)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de oid de topic effectué par {oid}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_topic_operateur(self, id_: None, operateur: int) -> None:
        query = "UPDATE topic SET topic_operateur = %s WHERE topic_id = %s;"
        params = (id_, operateur)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de operateur de topic effectué par {operateur}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_topic_nom(self, id_: None, nom: str) -> None:
        query = "UPDATE topic SET topic_nom = %s WHERE topic_id = %s;"
        params = (id_, nom)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de nom de topic effectué par {nom}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_topic_date(self, id_: None, date: datetime) -> None:
        query = "UPDATE topic SET topic_date = %s WHERE topic_id = %s;"
        params = (id_, date)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de date de topic effectué par {date}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_topic_message(self, id_: None, message: int) -> None:
        query = "UPDATE topic SET topic_message = %s WHERE topic_id = %s;"
        params = (id_, message)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de message de topic effectué par {message}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_topic_lien(self, id_: None, lien: str) -> None:
        query = "UPDATE topic SET topic_lien = %s WHERE topic_id = %s;"
        params = (id_, lien)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de lien de topic effectué par {lien}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_topic_forum(self, id_: None, forum: int) -> None:
        query = "UPDATE topic SET topic_forum = %s WHERE topic_id = %s;"
        params = (id_, forum)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de forum de topic effectué par {forum}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def delete_topic_id(self, id_: None) -> None:
        query = "DELETE FROM topic WHERE topic_id = %s;"
        params = (id_,)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Suppression de id de topic effectué')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def id2oid(self, id_: None) -> int:
        query = 'SELECT topic_oid FROM topic WHERE topic_id = %s;'
        params = (id_,)
        return self.get_results(query, params)


    def get_topic_id(self, id_: None) -> Topic:
        query = 'SELECT * FROM topic WHERE topic_id = %s;'
        params = (id_,)
        return Topic(*self.get_results(query, params, ind_='all'))

    def get_topic_oid(self, oid: int) -> Topic:
        query = 'SELECT * FROM topic WHERE topic_oid = %s;'
        params = (oid,)
        return Topic(*self.get_results(query, params, ind_='all'))


    def get_topic_from_id(self, from_: list | tuple, to_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id BETWEEN % AND %;'
        params = (from_, to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_from_oid(self, from_: list | tuple, to_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid BETWEEN % AND %;'
        params = (from_, to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_from_operateur(self, from_: list | tuple, to_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur BETWEEN % AND %;'
        params = (from_, to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_from_date(self, from_: list | tuple, to_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date BETWEEN % AND %;'
        params = (from_, to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_from_message(self, from_: list | tuple, to_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message BETWEEN % AND %;'
        params = (from_, to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_from_forum(self, from_: list | tuple, to_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum BETWEEN % AND %;'
        params = (from_, to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ge_id(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id >= %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ge_oid(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid >= %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ge_operateur(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur >= %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ge_date(self, to_: datetime) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date >= %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ge_message(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message >= %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ge_forum(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum >= %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_eq_id(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id == %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_eq_oid(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid == %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_eq_operateur(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur == %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_eq_date(self, to_: datetime) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date == %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_eq_message(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message == %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_eq_forum(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum == %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ne_id(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id <> %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ne_oid(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid <> %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ne_operateur(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur <> %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ne_date(self, to_: datetime) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date <> %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ne_message(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message <> %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_ne_forum(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum <> %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_gt_id(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id > %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_gt_oid(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid > %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_gt_operateur(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur > %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_gt_date(self, to_: datetime) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date > %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_gt_message(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message > %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_gt_forum(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum > %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_le_id(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id =< %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_le_oid(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid =< %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_le_operateur(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur =< %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_le_date(self, to_: datetime) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date =< %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_le_message(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message =< %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_le_forum(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum =< %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_lt_id(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id < %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_lt_oid(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid < %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_lt_operateur(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur < %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_lt_date(self, to_: datetime) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date < %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_lt_message(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message < %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_lt_forum(self, to_: int) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum < %s;'
        params = (to_,)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_in_id(self, list_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_id IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_in_oid(self, list_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_oid IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_in_operateur(self, list_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_operateur IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_in_date(self, list_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_date IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_in_message(self, list_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_message IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]

    def get_topic_in_forum(self, list_: list | tuple) -> list[Topic]:
        query = f'SELECT * FROM topic WHERE topic_forum IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Topic(*row) for row in self.get_results(query, params, ind_='all')]


    def get_topic_like_start_nom(self, deb: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_nom LIKE '{deb}%';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_like_between_nom(self, deb: str, fin: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_nom LIKE '{deb}%{fin}';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_like_end_nom(self, fin: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_nom LIKE '%{fin}';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_like_mid_nom(self, mil: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_nom LIKE '%{mil}%';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_regexp_nom(self, text: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_nom REGEXP '{text}';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_lt_nom(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_nom, '{text}') < {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_gt_nom(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_nom, '{text}') > {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_le_nom(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_nom, '{text}') <= {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_ge_nom(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_nom, '{text}') >= {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_eq_nom(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_nom, '{text}') == {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_ne_nom(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_nom, '{text}') <> {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_like_start_lien(self, deb: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_lien LIKE '{deb}%';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_like_between_lien(self, deb: str, fin: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_lien LIKE '{deb}%{fin}';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_like_end_lien(self, fin: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_lien LIKE '%{fin}';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_like_mid_lien(self, mil: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_lien LIKE '%{mil}%';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_regexp_lien(self, text: str) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE topic_lien REGEXP '{text}';"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_lt_lien(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_lien, '{text}') < {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_gt_lien(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_lien, '{text}') > {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_le_lien(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_lien, '{text}') <= {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_ge_lien(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_lien, '{text}') >= {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_eq_lien(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_lien, '{text}') == {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_topic_instr_ne_lien(self, text: str, occ: int) -> list[Topic]:
        query = f"SELECT * FROM topic WHERE INSTR(topic_lien, '{text}') <> {occ};"
        return [Topic(*row) for row in self.get_results(query, params=(), ind_='all')]


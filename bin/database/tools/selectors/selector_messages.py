"""==================================================
   Python class MessagesBdd générée par OQG BDD TOOLS GENERATOR
   Author: recitasse
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-05 18:11:12.349652
=================================================="""

import datetime

from dataclasses import dataclass

from bin.database.tools.entities.Messages import Messages

from bin.database.bbd import Link


@dataclass(init=False)
class MessagesBdd(Link):
    def is_in_id(self, id_: int) -> bool:
        query = "SELECT * FROM messages WHERE messages_id = %s;"
        params = (id_,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'messages {id_} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Messages {id_} n'est pas dans la base de donnée.")
        return False

    def is_in_oid(self, oid: int) -> bool:
        query = "SELECT * FROM messages WHERE messages_oid = %s;"
        params = (oid,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'messages {oid} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Messages {oid} n'est pas dans la base de donnée.")
        return False


    def add_messages(self, oid: int, user: int, topic: int, message: str, date: datetime) -> None:
        query = 'INSERT INTO messages (messages_oid, messages_user, messages_topic, messages_message, messages_date);'
        params = (oid, user, topic, message, date,)
        if not self.is_in_oid(oid):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'messages {oid} existe')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def update_messages_oid(self, id_: int, oid: int) -> None:
        query = "UPDATE messages SET messages_oid = %s WHERE messages_id = %s;"
        params = (id_, oid)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de oid de messages effectué par {oid}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_messages_user(self, id_: int, user: int) -> None:
        query = "UPDATE messages SET messages_user = %s WHERE messages_id = %s;"
        params = (id_, user)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de user de messages effectué par {user}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_messages_topic(self, id_: int, topic: int) -> None:
        query = "UPDATE messages SET messages_topic = %s WHERE messages_id = %s;"
        params = (id_, topic)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de topic de messages effectué par {topic}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_messages_message(self, id_: int, message: str) -> None:
        query = "UPDATE messages SET messages_message = %s WHERE messages_id = %s;"
        params = (id_, message)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de message de messages effectué par {message}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_messages_touser(self, id_: int, touser: int) -> None:
        query = "UPDATE messages SET messages_touser = %s WHERE messages_id = %s;"
        params = (id_, touser)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de touser de messages effectué par {touser}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_messages_date(self, id_: int, date: datetime) -> None:
        query = "UPDATE messages SET messages_date = %s WHERE messages_id = %s;"
        params = (id_, date)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de date de messages effectué par {date}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def delete_messages_id(self, id_: int) -> None:
        query = "DELETE FROM messages WHERE messages_id = %s;"
        params = (id_,)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Suppression de id de messages effectué')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def id2oid(self, id_: int) -> int:
        query = 'SELECT messages_oid FROM messages WHERE messages_id = %s;'
        params = (id_,)
        return self.get_results(query, params)


    def get_messages_id(self, id_: int) -> Messages:
        query = 'SELECT * FROM messages WHERE messages_id = %s;'
        params = (id_,)
        return Messages(*self.get_results(query, params, ind_='all'))

    def get_messages_oid(self, oid: int) -> Messages:
        query = 'SELECT * FROM messages WHERE messages_oid = %s;'
        params = (oid,)
        return Messages(*self.get_results(query, params, ind_='all'))


    def get_messages_from_id(self, from_: list | tuple, to_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id BETWEEN % AND %;'
        params = (from_, to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_from_oid(self, from_: list | tuple, to_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid BETWEEN % AND %;'
        params = (from_, to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_from_user(self, from_: list | tuple, to_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user BETWEEN % AND %;'
        params = (from_, to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_from_topic(self, from_: list | tuple, to_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic BETWEEN % AND %;'
        params = (from_, to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_from_touser(self, from_: list | tuple, to_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser BETWEEN % AND %;'
        params = (from_, to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_from_date(self, from_: list | tuple, to_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date BETWEEN % AND %;'
        params = (from_, to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ge_id(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id >= %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ge_oid(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid >= %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ge_user(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user >= %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ge_topic(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic >= %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ge_touser(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser >= %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ge_date(self, to_: datetime) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date >= %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_eq_id(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id == %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_eq_oid(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid == %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_eq_user(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user == %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_eq_topic(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic == %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_eq_touser(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser == %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_eq_date(self, to_: datetime) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date == %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ne_id(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id <> %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ne_oid(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid <> %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ne_user(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user <> %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ne_topic(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic <> %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ne_touser(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser <> %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_ne_date(self, to_: datetime) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date <> %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_gt_id(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id > %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_gt_oid(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid > %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_gt_user(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user > %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_gt_topic(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic > %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_gt_touser(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser > %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_gt_date(self, to_: datetime) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date > %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_le_id(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id =< %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_le_oid(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid =< %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_le_user(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user =< %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_le_topic(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic =< %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_le_touser(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser =< %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_le_date(self, to_: datetime) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date =< %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_lt_id(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id < %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_lt_oid(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid < %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_lt_user(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user < %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_lt_topic(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic < %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_lt_touser(self, to_: int) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser < %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_lt_date(self, to_: datetime) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date < %s;'
        params = (to_,)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_in_id(self, list_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_id IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_in_oid(self, list_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_oid IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_in_user(self, list_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_user IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_in_topic(self, list_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_topic IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_in_touser(self, list_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_touser IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]

    def get_messages_in_date(self, list_: list | tuple) -> list[Messages]:
        query = f'SELECT * FROM messages WHERE messages_date IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Messages(*row) for row in self.get_results(query, params, ind_='all')]


    def get_messages_like_start_message(self, deb: str) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE messages_message LIKE '{deb}%';"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_like_between_message(self, deb: str, fin: str) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE messages_message LIKE '{deb}%{fin}';"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_like_end_message(self, fin: str) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE messages_message LIKE '%{fin}';"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_like_mid_message(self, mil: str) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE messages_message LIKE '%{mil}%';"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_regexp_message(self, text: str) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE messages_message REGEXP '{text}';"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_instr_lt_message(self, text: str, occ: int) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE INSTR(messages_message, '{text}') < {occ};"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_instr_gt_message(self, text: str, occ: int) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE INSTR(messages_message, '{text}') > {occ};"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_instr_le_message(self, text: str, occ: int) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE INSTR(messages_message, '{text}') <= {occ};"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_instr_ge_message(self, text: str, occ: int) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE INSTR(messages_message, '{text}') >= {occ};"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_instr_eq_message(self, text: str, occ: int) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE INSTR(messages_message, '{text}') = {occ};"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]

    def get_messages_instr_ne_message(self, text: str, occ: int) -> list[Messages]:
        query = f"SELECT * FROM messages WHERE INSTR(messages_message, '{text}') <> {occ};"
        return [Messages(*row) for row in self.get_results(query, params=(), ind_='all')]



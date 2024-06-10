"""==================================================
   Python class PinedBdd générée par OQG BDD TOOLS GENERATOR
   Author: recitasse
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-05 18:11:12.348808
=================================================="""

import datetime

from dataclasses import dataclass

from bin.database.tools.entities.Pined import Pined

from bin.database.bbd import Link


@dataclass(init=False)
class PinedBdd(Link):
    def is_in_id(self, id_: int) -> bool:
        query = "SELECT * FROM pined WHERE pined_id = %s;"
        params = (id_,)
        try:
            if self.get_results(query, params):
                self._logger.info(f'pined {id_} existe')
                return True
        except Exception as e:
            self._logger.error(f'Une erreur MySQL est survenue : {e}')
        self._logger.info(f"Pined {id_} n'est pas dans la base de donnée.")
        return False


    def add_pined(self, userid: int, badgeid: int) -> None:
        query = 'INSERT INTO pined (pined_userid, pined_badgeid);'
        params = (userid, badgeid,)
        if not self.is_in_userid(userid):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'pined {userid} existe')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def update_pined_userid(self, id_: int, userid: int) -> None:
        query = "UPDATE pined SET pined_userid = %s WHERE pined_id = %s;"
        params = (id_, userid)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de userid de pined effectué par {userid}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()

    def update_pined_badgeid(self, id_: int, badgeid: int) -> None:
        query = "UPDATE pined SET pined_badgeid = %s WHERE pined_id = %s;"
        params = (id_, badgeid)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Modification de badgeid de pined effectué par {badgeid}')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()


    def delete_pined_id(self, id_: int) -> None:
        query = "DELETE FROM pined WHERE pined_id = %s;"
        params = (id_,)
        if not self.is_in_id(id_):
            cursor = self.connexion.cursor()
            try:
                cursor.execute(query, params)
                self.connexion.commit()
                self._logger.info(f'Suppression de id de pined effectué')
            except Exception as e:
                self._logger.error(f'Une erreur MySQL est survenue : {e}')
            finally:
                cursor.close()



    def get_pined_id(self, id_: int) -> Pined:
        query = 'SELECT * FROM pined WHERE pined_id = %s;'
        params = (id_,)
        return Pined(*self.get_results(query, params, ind_='all'))


    def get_pined_from_id(self, from_: list | tuple, to_: list | tuple) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id BETWEEN % AND %;'
        params = (from_, to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_from_userid(self, from_: list | tuple, to_: list | tuple) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid BETWEEN % AND %;'
        params = (from_, to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_from_badgeid(self, from_: list | tuple, to_: list | tuple) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid BETWEEN % AND %;'
        params = (from_, to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_ge_id(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id >= %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_ge_userid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid >= %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_ge_badgeid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid >= %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_eq_id(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id == %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_eq_userid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid == %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_eq_badgeid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid == %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_ne_id(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id <> %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_ne_userid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid <> %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_ne_badgeid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid <> %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_gt_id(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id > %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_gt_userid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid > %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_gt_badgeid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid > %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_le_id(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id =< %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_le_userid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid =< %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_le_badgeid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid =< %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_lt_id(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id < %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_lt_userid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid < %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_lt_badgeid(self, to_: int) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid < %s;'
        params = (to_,)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_in_id(self, list_: list | tuple) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_id IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_in_userid(self, list_: list | tuple) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_userid IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]

    def get_pined_in_badgeid(self, list_: list | tuple) -> list[Pined]:
        query = f'SELECT * FROM pined WHERE pined_badgeid IN ({",".join(["%s"] * len(list_))});'
        params = tuple(list_)
        return [Pined(*row) for row in self.get_results(query, params, ind_='all')]




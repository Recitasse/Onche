import os

from datetime import datetime
import dateutil.relativedelta

from BDD.bdd import BDD
from config.Variables.variables import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER


class Discours(BDD):
    def __init__(self) -> None:
        super().__init__()

    def take_discours_from_users(self, users: list = None, message_lim: int = 100000, date: tuple = (datetime.now(), datetime.now()-dateutil.relativedelta.relativedelta(year=1))) -> list:
        if not users:
            users = tuple(self.get_results("SELECT onchois_id FROM onchois;", ind_="all"))
        else:
            if not self.__check_type(users):
                raise ValueError("La liste des utilisateurs n'est pas homogène")
            if isinstance(users[0], str):
                placeholder = ', '.join(['%s'] * len(users))
                users = tuple(self.get_results(f"SELECT onchois_id FROM onchois WHERE onchois_nom IN ({placeholder});", params=(*users,), ind_="all"))
            if isinstance(users[0], int):
                users = tuple(self.get_results("SELECT onchois_id FROM onchois;", ind_="all"))
        
        start_date, end_date = date[1].strftime('%Y-%m-%d %H:%M:%S'), date[0].strftime('%Y-%m-%d %H:%M:%S')

        users_placeholder = ', '.join(['%s'] * len(users))
        messages = self.get_results(f"SELECT message_message FROM messages WHERE message_user IN ({users_placeholder}) AND message_date BETWEEN '{start_date}' AND '{end_date}' LIMIT {message_lim};", params=(*users,), ind_="all")
        messages = self.__clean_messages(messages)
        return messages


    @staticmethod
    def __clean_messages(msg_list: list) -> list:
        for i, msg in enumerate(msg_list):
            words = msg.split()
            for j, word in enumerate(words):
                if word.startswith("https") or word.startswith("(None)"):
                    words.pop(j)
            msg_list[i] = ' '.join(words)
        return msg_list

    @staticmethod
    def __check_type(elements: list) -> bool:
        """Vérifie si la liste est bien homogène"""
        is_strings = lambda lst: all(isinstance(item, str) for item in lst)
        is_ints = lambda lst: all(isinstance(item, int) for item in lst)

        if is_strings(elements) or is_ints(elements):
            return True
        return False
    
if __name__ == "__main__":
    p = Discours()
    p.take_discours_from_users()
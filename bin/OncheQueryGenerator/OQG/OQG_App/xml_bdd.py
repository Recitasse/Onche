import xml.etree.ElementTree as ET
import datetime

from config.variables import *
from BDD.bdd import BDD
from utils.fonction import forum_xml

class XMLCreator:
    def __init__(self, root_element_name):
        self.root = ET.Element(root_element_name)

    def add_element(self, parent, tag, text=None, attributes=None):
        """Ajouter un élément avec tags au XML"""
        element = ET.SubElement(parent, tag)
        if text:
            element.text = text
        if attributes:
            for key, value in attributes.items():
                element.set(key, value)
        return element

    def save_to_file(self, filename, indent=True):
        """Ajouter """
        tree = ET.ElementTree(self.root)
        if indent:
            # Use minidom to add indentation
            from xml.dom import minidom
            xmlstr = minidom.parseString(ET.tostring(self.root)).toprettyxml(indent="  ")
            with open(filename, "w") as f:
                f.write(xmlstr)
        else:
            tree.write(filename)


def xml_database(database: str = MYSQL_DATABASE):
    """Créer le fichier de métadonnée xml"""

    bdd = BDD(database=database)
    messages = bdd.get_results("SELECT COUNT(*) FROM messages;")

    recent = bdd.get_results("SELECT MAX(message_date) AS most_recent_date FROM messages;").strftime('%Y-%m-%d %H:%M:%S')
    old = bdd.get_results("SELECT MIN(message_date) AS most_recent_date FROM messages;").strftime('%Y-%m-%d %H:%M:%S')

    list_forum = bdd.get_results("SELECT DISTINCT topic_forum AS unique_forum_count FROM topic;", ind_="all")
    forum_dict = {forum: forum_xml(forum)['name'] for forum in list_forum}

    xml_creator = XMLCreator("database")

    attributes1 = {"version": VERSION}
    version = xml_creator.add_element(xml_creator.root, "version", "", attributes1)

    xml_creator.add_element(version, "messages", f"{messages}")

    attributes2 = {"dernier": recent, "premier": old}
    xml_creator.add_element(version, "date", "", attributes2)

    forums = xml_creator.add_element(version, "forums", "")
    for key, val in forum_dict.items():
        forum = xml_creator.add_element(forums, "forum", "")
        xml_creator.add_element(forum, "nom", str(val), {"id": str(key)})
        
        old = bdd.get_results("SELECT MIN(message_date) AS most_recent_date FROM messages WHERE message_topic IN (SELECT id_topic FROM topic WHERE topic_forum = %s);", params=(key,)).strftime('%Y-%m-%d %H:%M:%S')
        recent = bdd.get_results("SELECT MAX(message_date) AS most_recent_date FROM messages WHERE message_topic IN (SELECT id_topic FROM topic WHERE topic_forum = %s);", params=(key,)).strftime('%Y-%m-%d %H:%M:%S')

        nb_messages = bdd.get_results("SELECT COUNT(*) FROM messages WHERE message_topic IN (SELECT id_topic FROM topic WHERE topic_forum = %s);", params=(key,))
        xml_creator.add_element(forum, "messages", str(nb_messages), {"dernier": recent, "premier": old})

    # pour les tables
    tables_xml = xml_creator.add_element(version, "tables", "")
    tables = bdd.get_results(f"SHOW TABLES FROM {MYSQL_DATABASE};", ind_="all")
    for table in tables:
        xml_creator.add_element(tables_xml, "table", "")
        info_tables = bdd.get_results(f"DESCRIBE {table};", ind_="all")
        t = xml_creator.add_element(tables_xml, "table", "", {"name": table})
        for info in info_tables:
            attribut = {"type": info[1], "Null": info[2]}
            if info[3] == "PRI" or info[3] == "UNI" or info[3] == "MUL":
                key = {"Key": info[3]}
                attribut.update(key)
            if str(info[4]) != "None":
                default = {"Default": str(info[4])}
                attribut.update(default)
            xml_creator.add_element(t, "champ", info[0], attributes=attribut)

    xml_creator.save_to_file(f"{GLOBAL_PATH}bin/OQG_Types/Forum/bdd_metadata.xml", indent=True)

if __name__ == "__main__":
    xml_database()
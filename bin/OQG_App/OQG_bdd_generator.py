import os
from pathlib import Path
from ast import literal_eval
from datetime import datetime
from getpass import getuser

import xml.etree.ElementTree as ET

from config.Variables.variables import *


def metadata() -> str:
    sql_code = "-- MySQL Script généré par OQG BDD GENERATOR\n"
    sql_code += f"-- Author: {getuser()}\n"
    sql_code += f"-- Model: Onche\t Version: {VERSION}\n"
    sql_code += f"-- Made by Recitasse {datetime.now()}\n\n"

    sql_code += f"SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;\n"
    sql_code += f"SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;\n"
    sql_code += f"SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';\n\n"

    sql_code += (f"CREATE SCHEMA IF NOT EXISTS `{MYSQL_DATABASE}` DEFAULT CHARACTER SET utf8mb4;\n"
                 f"USE `{MYSQL_DATABASE}` ;\n")

    return sql_code

def setting() -> str:
    sql_code = "SET SQL_MODE=@OLD_SQL_MODE;\n"
    sql_code += "SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;\n"
    sql_code += "SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;"
    return sql_code

def get_all_xml_files() -> list:
    files = os.listdir(CALICE)
    for file in files:
        if not Path(file).suffix == ".xml":
            raise AttributeError("Tous les fichiers dans le calice doivent être des xml")
    return files


def generate_sql_code_from_xml(file: str) -> str:
    sql_code = f"\n-- -----------------------------------------------------\n"

    with open(f"{CALICE}{file}", 'r', encoding="utf-8") as conf:
        root: ET.Element = ET.fromstring(conf.read())
    table_name = root.attrib['table']
    sql_code += f"-- Table `{MYSQL_DATABASE}`.`{table_name}`\n"
    sql_code += f"-- -----------------------------------------------------\n\n"
    tab_ = "  "
    sql_code += f"CREATE TABLE IF NOT EXISTS `{MYSQL_DATABASE}`.`{table_name}` (\n"
    if root.find('rows'):
        # Rows
        for i, row in enumerate(root.find('rows')):
            default_val = ""
            aut_int = ""
            null = ""
            if 'default' in row.attrib:
                default_val = f" DEFAULT {row.attrib['default']}" if row.attrib['default'] is not None else ''
            if 'auto_increment' in row.attrib:
                aut_int = " AUTO_INCREMENT"
            if 'null' in row.attrib:
                null = f"{'NULL' if literal_eval(row.attrib['null']) else 'NOT NULL'}"
            sql_code += (f"{tab_}{table_name}_{row.attrib['name']} "
                         f"{row.attrib['sql-type']} "
                         f"{null}"
                         f"{aut_int}"
                         f"{default_val},\n")

        # Indexes
        index = root.find('index')
        pk = index.find('primary-key')
        sql_code += f"{tab_}PRIMARY KEY (`{table_name}_{pk.attrib['name']}`)"
        if index.find('unic-index'):
            sql_code += ",\n"

        # Unique Index
        sdl = '\n'
        unic_index = index.find('unic-index')
        if unic_index:
            for i, name in enumerate(unic_index):
                fname = f" {name.attrib['mode']}"
                fvisi = f" VISIBLE"
                sql_code += f"{tab_}UNIQUE INDEX `{table_name}_{name.text}_UNIQUE` (`{table_name}_{name.text}`{fname if name.attrib['mode'] else ''}){fvisi if name.attrib['visible'] else ''}{'' if i+1 == len(unic_index) else sdl}"

        if index.find('foreign-index'):
            sql_code += ",\n"

        # foreign keys
        index_for = []
        constrs = []
        if index.find('foreign-index'):
            for i, row in enumerate(index.find('foreign-index')):
                tmp_index_ = f"{tab_}INDEX `{row.attrib['name']}_idx` (`{table_name}_{row.find('foreign-key').text}` ASC) VISIBLE,{'' if i+1 == len(index.find('foreign-index')) else sdl}"
                constraint = f"\n{tab_}CONSTRAINT `{row.attrib['name']}`\n"
                constraint += f"{tab_*2}FOREIGN KEY (`{table_name}_{row.find('foreign-key').text}`)\n"
                constraint += f"{tab_*2}REFERENCES `{MYSQL_DATABASE}`.`{row.find('reference').attrib['table']}` (`{row.find('reference').attrib['table']}_{row.find('reference').text}`)\n"
                constraint += f"{tab_*2}ON DELETE {row.find('on-delete').text}\n"
                constraint += f"{tab_*2}ON UPDATE {row.find('on-update').text},"

                index_for.append(tmp_index_)
                constrs.append(constraint)
            for el in index_for:
                sql_code += el
            for i, el2 in enumerate(constrs):
                sql_code += el2

        if sql_code[-1] == ',':
            sql_code = sql_code[:-1] + ')'
        else:
            sql_code += ')'

        # Settings
        parameters = root.find('parameters')
        for settings in parameters:
            if settings.tag == 'settings':
                sql_code += f"\nENGINE = {settings.attrib['engine']}\n"
                sql_code += f"DEFAULT CHARACTER SET = {settings.attrib['encoding']}\n"
                sql_code += f"COLLATE = {settings.attrib['collation']}\n"
            if settings.tag == 'comment':
                sql_code += f"COMMENT = '{settings.text}';\n\n"
    return sql_code

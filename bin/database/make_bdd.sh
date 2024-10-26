#!/bin/bash

DB_NAME="Onche"
SQL_SCRIPT="data/Database/src/schema.sql"
DB_USER="utilisateur"
DB_PASS="mot_de_passe"
DB_HOST="localhost"

# Créer la base de données
mysql -u $DB_USER -p$DB_PASS -h $DB_HOST -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

# Exécuter le script SQL pour créer les tables
mysql -u $DB_USER -p$DB_PASS -h $DB_HOST $DB_NAME < $SQL_SCRIPT
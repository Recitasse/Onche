#!/bin/bash

# ========================================
# Install git

sudo apt update -y
sudo apt install git -y

# ========================================
# Install python3.11
sudo apt-get install python3.11
sudo apt update
python3.11 -m pip install --upgrade pip
python3.11 -m pip install virtualenv

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install --upgrade mysql-connector-python

# ========================================
# install mysql
MYSQL_USER="onche"
MYSQL_PASSWORD="OnchePass1#"
MYSQL_DATABASE="Onche"
SQL_SCRIPT="BDD/install/DDBONCHE.sql"

sudo apt install mysql-server
sudo mysql < "$SQL_SCRIPT"
# =======================================
file_path="/etc/hosts"
line_to_search="127.0.6.5       Onche"

# Search for the line in the file
if grep -qF "$line_to_search" "$file_path"; then
    echo "Host déjà présent."
else
    temp_file=$(mktemp)

    echo "$line_to_search" | cat - /etc/hosts > "$temp_file"

    sudo mv "$temp_file" /etc/hosts
fi
sudo systemctl restart mysql.service

# ======================================
# Export variable

installation_path=$(pwd)

cat << EOF > "config/Variables/variables.py"
# CONFIG
GLOBAL_PATH = "${installation_path}/"

# Mysql
SAVE_FREQUENCY = 10
MYSQL_USER = '${MYSQL_USER}'
MYSQL_PASSWORD = '${MYSQL_PASSWORD}'
MYSQL_DATABASE = '${MYSQL_DATABASE}'
MYSQL_HOST = '${MYSQL_HOST}'
MYSQL_PATH_EXPORT = GLOBAL_PATH + "BDD/exports/"

# Encryption
SALT = "1kd0S"

# logger
PATH_BDD_LOG = GLOBAL_PATH + "BDD/bdd.log"
PATH_SCRAPPER_LOG = GLOBAL_PATH + "webscrapper/scrapper.log"
PATH_WEB_BROWSER = GLOBAL_PATH + "webscrapper/browser.log"

# forums xml
FORUM_XML = GLOBAL_PATH + "config/forums.xml"

# Browser
BASE_URL = "https://onche.org/forum/"
USER_AGENT = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_6_7; en-US) Gecko/20100101 Firefox/70.4"
DEFAULT_PROFILE = GLOBAL_PATH + "utils/cryptage/profile/default.json"
EOF

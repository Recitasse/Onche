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
USERS=("BOT_blabla", "BOT_sugg", "BOT_pron", "BOT_goulag", "BOT_anciens", "BOT_mode", "BOT_crypto", "BOT_jv", "BOT_auto")
MYSQL_PASSWORD="OnchePass1#"
MYSQL_DATABASE="Onche"
SQL_SCRIPT="BDD/install/DDBONCHE.sql"

check_user_exists() {
    sudo mysql -sse "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '$MYSQL_USER')"
}

for MYSQL_USER in "${USERS[@]}"; do
    # Check if the user already exists
    if [ $(check_user_exists "$MYSQL_USER") -eq 0 ]; then
        sudo mysql -e "CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';"
        sudo mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'localhost';"
        sudo mysql -e "FLUSH PRIVILEGES;"
        echo "Bot $MYSQL_USER créé avec succès."
    else
        echo "Bot $MYSQL_USER existe déjà."
    fi
done

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

sudo ./${installation_path}/BDD/export/git-lfs-3.4.1/install.sh

cat << EOF > "config/Variables/variables.py"
# CONFIG
GLOBAL_PATH = "${installation_path}/"

# Mysql
SAVE_FREQUENCY = 10
MYSQL_USER = 'onche'
# -- > BOT
USERS=("BOT_blabla", "BOT_sugg", "BOT_pron", "BOT_goulag", "BOT_anciens", "BOT_mode", "BOT_crypto", "BOT_jv", "BOT_auto")
MYSQL_BOT_BLABLA = BOT_blabla
MYSQL_BOT_SUGG = BOT_sugg
MYSQL_BOT_PRON = BOT_pron
MYSQL_BOT_GOULAG = BOT_goulag
MYSQL_BOT_ANCIENS = BOT_anciens
MYSQL_BOT_MODE = BOT_mode
MYSQL_BOT_CRYPTO = BOT_crypto
MYSQL_BOT_JV = BOT_jv
MYSQL_BOT_AUTO = BOT_auto
# -- <
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

# QUERIES
ONHISATEUR_QUERIES = GLOBAL_PATH + "BDD/queries/onchois_analyseur/queries.json"

# SAVE
CYCLIC_EXPORT = 86400
BDD_EXPORT = GLOBAL_PATH + "BDD/export/"
SAVE_SUJET = GLOBAL_PATH + "OncheSTUD/communautes/Sujet/"
EOF

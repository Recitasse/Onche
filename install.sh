#!/bin/bash

# ========================================
# Install git

sudo apt update -y
sudo apt install git -y

# ========================================
# Install python3.11
sudo apt-get install python3.11
sudo apt install python3 python3-tk
python3.11 -m pip install --upgrade pip
python3.11 -m pip install virtualenv

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install --upgrade mysql-connector-python

# ========================================
# APache
sudo apt install apache2
sudo ufw allow in "Apache"
sudo apt-get install php-curl
sudo apt install php libapache2-mod-php php-mysql
php -v

sudo apt install sqlite

# ========================================
# install mysql
if [ "$1" == "local" ]; then
    echo "Base de donnée locale sélectionnée."
elif [ "$1" == "server" ]; then
    echo "Base de donnée server sélectionnée."
    USERS=("BOT_blabla", "BOT_sugg", "BOT_pron", "BOT_goulag", "BOT_anciens", "BOT_mode", "BOT_crypto", "BOT_jv", "BOT_auto")
    MYSQL_PASSWORD="OnchePass1#"
    MYSQL_DATABASE="Onche"
    SQL_SCRIPT="BDD/install/DDBONCHE.sql"

    sudo apt install mysql-server
    sudo mysql < "$SQL_SCRIPT"
    sudo systemctl restart mysql.service

    installation_path=$(pwd)
    file=$(ls ${installation_path}/BDD/export/bdd_*.zip | head -n 1)
else

# ======================================
# Installer le domaine
sudo chmod -R 755 "${installation_path}"
sudo chown -R $USER:$USER "${installation_path}/WebAPP/html/"

vh_conf_file="/etc/apache2/sites-available/BabelOnche.conf"
sudo bash -c "cat > $vh_conf_file" <<EOF
<VirtualHost *:80>
        DocumentRoot ${installation_path}/WebAPP/html/
        ServerName BabelOnche
        ServerAlias www.BabelOnche.com
         <Directory ${installation_path}/WebAPP/html/>
           Options Indexes FollowSymLinks
           AllowOverride None
           Require all granted
         </Directory>
</VirtualHost>
EOF
sudo a2ensite BabelOnche.conf
sudo systemctl restart apache2

# ======================================
# Export variable

#sudo .${installation_path}/BDD/export/git-lfs-3.4.1/install.sh

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

# INFO
VERSION = "0.8.3"
CREATEUR = ["Récitasse"]
DDB = '${ddb}'
TYPE = '${$1}'
EOF

# Run the python api
source "${installation_path}/venv/bin/activate"
nohup python "${installation_path}/WebAPP/API/main.py" &
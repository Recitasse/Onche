#!/bin/bash

if grep -q 'export ONCHE_PATH=' ~/.bashrc; then
    echo "Le ONCHE_PATH existe déjà"
else
    ONCHE_PATH=$(pwd)
    export PATH="$ONCHE_PATH:$PATH"
fi

sudo apt update -y
echo -e "\n"
# ========================================
# Install git
echo "===== GIT INSTALL ====="
sudo apt install git -y
echo -e "\n"

echo "===== REPO GIT ====="
#git clone https://github.com/Recitasse/Onche.git
echo -e "\n"

# ========================================
# Install python3.11
echo "===== INSTAL PYTHON ====="
sudo apt-get install python3.11
echo -e "     Python3.11 installé"
sudo apt install python3 python3-tk
echo -e "     Python3.11 installé"
sudo apt install python3.11-venv
python3.11 -m pip install --upgrade pip
python3.11 -m pip install virtualenv
python3.11 -m venv venv
echo -e "     Virtualenv installé"
source venv/bin/activate
echo -e "     Environnement activé"
echo -e "\n"

echo "===== DÉPENDENCES PYTHON ====="
pip install -r requirements.txt
pip install --upgrade mysql-connector-python
echo "     Dépendences installées"
echo -e "\n"
touch venv/lib/python3.11/site-packages/route.pth
echo "$(pwd)" >> venv/lib/python3.11/site-packages/route.pth

# ========================================
# APache
echo "===== INSTALLATION WEB SERVER ====="
sudo apt install apache2
sudo ufw allow in "Apache"
sudo apt-get install php-curl
sudo apt install php libapache2-mod-php php-mysql
php -v
echo -e "\n"

# ======================================
# Installer le domaine
installation_path=$(pwd)
echo "===== HTTP DOMAIN SERVER ====="
sudo chmod +x /home/$USER/
sudo chmod -R 755 "${installation_path}/WebAPP/html/"
sudo chown -R "www-data":"www-data" "${installation_path}/WebAPP/html/"

vh_conf_file="/etc/apache2/sites-available/BabelOnche.conf"
sudo bash -c "cat > $vh_conf_file" <<EOF
<VirtualHost 127.0.6.5:80>
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
echo -e "\n"

# ========================================
# install mysql
installation_path=$(pwd)
echo "===== INSTALLATION MYSQL ET SQLITE ====="
if [ "$1" == "local" ]; then
    echo "Base de donnée locale sélectionnée."
elif [ "$1" == "server" ]; then
    echo "Base de donnée server sélectionnée."
    MYSQL_USER="onche"
    MYSQL_PASSWORD="OnchePass1#"
    MYSQL_DATABASE="Onche"
    SQL_SCRIPT="BDD/schema/DDBONCHE.sql"

    sudo apt install mysql-server
    echo "     Installation MySQL terminée"
    sudo apt install sqlite
    #mysql -u root -p -e "CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';"
    #mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'localhost';"
    #mysql -u root -p -e "FLUSH PRIVILEGES;"
    echo -e "     Installation SQLite terminée"
    sudo mysql < "$SQL_SCRIPT"
    sudo systemctl restart mysql.service
    echo -e "     Configuration MySQL établie"

    #file=$(find "${installation_path}"/BDD/export/bdd_*.zip | head -n 1)
fi
echo -e "\n"

# ======================================
# Export variable
#sudo .${installation_path}/BDD/export/git-lfs-3.4.1/install.sh

echo "===== GÉNÉRATION DU FICHIER DE CONFIGURATION ====="
mkdir config/Variables
touch config/Variables/variables.py
cat << EOF > "config/Variables/variables.py"
# CONFIG
GLOBAL_PATH = "${installation_path}/"

# Mysql
SAVE_FREQUENCY = 10
MYSQL_USER = '${MYSQL_USER}'
# -- > BOT
MYSQL_BOT_BLABLA = "BOT_blabla"
MYSQL_BOT_SUGG = "BOT_sugg"
MYSQL_BOT_PRON = "BOT_pron"
MYSQL_BOT_GOULAG = "BOT_goulag"
MYSQL_BOT_ANCIENS = "BOT_anciens"
MYSQL_BOT_MODE = "BOT_mode"
MYSQL_BOT_CRYPTO = "BOT_crypto"
MYSQL_BOT_JV = "BOT_jv"
MYSQL_BOT_AUTO = "BOT_auto"
# -- <
MYSQL_PASSWORD = '${MYSQL_PASSWORD}'
MYSQL_DATABASE = '${MYSQL_DATABASE}'
MYSQL_HOST = '${MYSQL_HOST}'
MYSQL_PATH_EXPORT = GLOBAL_PATH + "BDD/exports/"

# Encryption
SALT = "1kd0S"

# logger
PATH_BDD_LOG = GLOBAL_PATH + "BDD/bdd.log"
PATH_API_LOG = GLOBAL_PATH + "WebAPP/API/api.log"
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
DDB = 'Onche'
TYPE = '$1'
EOF
echo -e "     Fichier de configuration effectuée"
echo -e "\n"

# install all types
echo "===== GÉNÉRATION MÉTADONNÉES BDD ====="
python "${installation_path}"/bin/fonctions/xml_bdd.py
echo "      Génération terminée"

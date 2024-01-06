# CONFIG
GLOBAL_PATH = "/home/raphael/Bureau/Programmation/Python/Onche beta/"

# Mysql
SAVE_FREQUENCY = 10
MYSQL_USER = 'onche'
MYSQL_PASSWORD = 'OnchePass1#'
MYSQL_DATABASE = 'Onche'
MYSQL_HOST = 'localhost'
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
BINARY = "/usr/bin/firefox"
PROFILE = GLOBAL_PATH + "utils/browser/profile"
GECKO = GLOBAL_PATH + "utils/browser/geckodriver.exe"
BASE_URL = "https://onche.org/forum/"
USER_AGENT = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_6_7; en-US) Gecko/20100101 Firefox/70.4"
DEFAULT_PROFILE = GLOBAL_PATH + "utils/cryptage/profile/default.json"

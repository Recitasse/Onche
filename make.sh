#!/bin/bash

echo "=== DELETING .VENV ==="
if [ -e .venv/ ]; then
    rm -rf .venv/
fi
echo "deleting done"

echo "=== INSTALL INSTALL SETUPTOOLS ==="

python3.12 -m venv .venv
source .venv/bin/activate

pip install setuptools wheel build

echo "=== INSTALL BIN LIBRARIES ==="
echo " --- Install database package ---"
pip install -e bin/database/.
echo "Done"
echo " --- Install OncheQueryGenerator package ---"
pip install -e bin/OncheQueryGenerator/.
echo "Done"
echo " --- Install WebAPP package ---"
pip install -e bin/WebAPP/.
echo "Done"
echo " --- Install WebScrapper package ---"
pip install -e bin/WebScrapper/.
echo "Done"
echo "=== INSTALL ABACUS LIBRARIES ==="
echo " --- Install Cassandre package ---"
pip install -e Abacus/Cassandre/.
echo "Done"
echo " --- Install Communautees package ---"
pip install -e Abacus/Communautees/.
echo "Done"
echo " --- Install Mimos package ---"
pip install -e Abacus/Mimos/.
echo "Done"
echo " --- Install Profileur package ---"
pip install -e Abacus/Profileur/.
echo "Done"
echo " --- Install Sarapis package ---"
pip install -e Abacus/Sarapis/.
echo "Done"

#echo " --- Install Utils package ---"
#pip install -e utils/.
#echo "Done"

pip install sphinx

pip freeze > requirements.txt

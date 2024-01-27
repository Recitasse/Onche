#!/bin/bash

echo "===== START API ONCHE ====="

lsof -i :5000 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    PIDS=$(lsof -ti :5000)
    for PID in $PIDS; do
        echo "Kill $PID"
        kill -9 $PID
    done
else
    echo "API prête à démarrer"
fi

nohup venv/bin/python3.11 "WebAPP/API/main.py" &
echo -e "     API Onche est lancée"
echo -e "\n"
echo "===== START MYSQL ====="
sudo systemctl restart mysql.servcie
systemctl status mysql.service
echo -e "\n"
echo "===== START APACHE2 ====="
sudo systemctl restart apache2.servcie
systemctl status apache2.service
echo -e "\n"
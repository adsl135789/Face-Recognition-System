#!/bin/bash

sudo apt update

sudo apt install -y mysql-server-8.0
#sudo mysql_secure_installation


# check mysql status
sudo systemctl status mysql

sudo apt install vim
# 設定可以讓外網連線
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
#bind-address = 0.0.0.0 # 這個是指誰都可以連線的意思
sudo systemctl restart mysql #設定完成後要重啟才會生效

sudo apt install build-essential
sudo apt install cmake
sudo apt install python3-pyqt5
sudo apt install pyqt5-dev-tools
sudo apt install python3-pip

# 設定防火牆，資料庫慣用的port為3306，22是給ssh登入使用
sudo apt install ufw
sudo ufw enable
sudo ufw allow 3306
sudo ufw allow 51688
sudo ufw allow 22/tcp
sudo ufw status

# set mysql server start when the system boots 
sudo systemctl is-enabled mysql.service 
#!/usr/bin/sh

yum install git -y

yum install vim -y

yum install epel-release -y

yum install python36 python36-libs python36-devel python36-pip -y

pip3 install --upgrade pip

echo "alias python='/usr/bin/python3.6'" >> ~/.bashrc

echo "alias pip=pip3" >> ~/.bashrc

source ~/.bashrc

python -V

python -m pip -V

pip install pymysql

pip install influxdb

pip install paramiko

pip install requests

pip install pyinstaller

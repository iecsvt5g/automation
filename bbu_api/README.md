
<h1>Please Install on inventec BBU</h1>

### Install Steps ###

## Install 1. Install python3 libs
# fastapi
apt install python3-pip
pip install fastapi # FastAPI
pip install uvicorn[standard] # ASGI Server
#
pip install paramiko==2.6.0
pip install psutil-5.9.4

## 2. Copy codes from server

## 3. Install API
sh update_service.sh




### NOTE ###
api.py              = RestFul API
server.log          = Service log
start_service.sh    = Script to start API
bbu_api.service     = Linux Service
README.md           = README
update_service.sh   = Script to update API from server

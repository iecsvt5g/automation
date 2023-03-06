
<h1>Please Install on inventec BBU</h1>

### Install Steps ###

## Install 1. Install python3 libs (216,155)
# fastapi
```  shell
apt install python3-pip
pip install fastapi # FastAPI
pip install uvicorn[standard] # ASGI Server
#
pip install paramiko==2.6.0
pip install psutil-5.9.4
``` 
## 2. Build mybbu binary
### 2.1 Git clone to server(216)

### 2.2 Login BBU server (155)
```  shell
ssh root@172.32.3.155 
``` 
### 2.3 Copy files from server (155)
```  shell
scp 172.32.3.216:/opt/nex_ia0/bbu_agent/bbu_api/* /opt/bbu_api/
``` 
## 3. Build Binary (155)
```  shell
sh update_service.sh
``` 
## 4. Get result (216)
#
## Build Command
pyinstaller --onefile --hidden-import=api api.py

### NOTE ###
api.py              = RestFul API<br>
server.log          = Service log<br>
start_service.sh    = Script to start API<br>
bbu_api.service     = Linux Service<br>
README.md           = README<br>
update_service.sh   = Script to update API from server<br>

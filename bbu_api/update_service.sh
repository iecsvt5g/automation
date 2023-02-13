mkdir -p /opt/bbu_api
echo "- Stop service"
sudo systemctl stop bbu_api
sleep 3
echo "- Copy from management system"
scp 172.32.3.216:/opt/nex_ia0/bbu_agent/bbu_api/* /opt/bbu_api/

echo "- Update service"
cd /opt/bbu_api
sudo chmod 644 *.service
sudo cp *.service /etc/systemd/system

sudo systemctl daemon-reload
sudo systemctl start  bbu_api
sudo systemctl enable bbu_api
sleep 1
echo "- Check service status"
sudo systemctl status  bbu_api

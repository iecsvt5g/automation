#day=$(date +%y%m%d_%H%M)
day=$(date +%Y-%m-%d -d "3 day ago")
echo "Remove pcap file in history folder before 3 day ago"
find /opt/tcpdump/history/*.pcap ! -newermt $day
find /opt/tcpdump/history/*.pcap ! -newermt $day | xargs rm -rf


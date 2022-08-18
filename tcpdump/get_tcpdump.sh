
day=$(date +%y%m%d_%H%M)
dest="/opt/tcpdump/history"
mkdir -p $dest
file_name="tcpdump-$day.pcap"
echo "> Start tcpdump :"$file_name
date
#sudo timeout 1800 tcpdump -i any  -w $dest/$file_name
sudo timeout 1800 tcpdump -i any -nn sctp -w $dest/$file_name

echo "> Done"

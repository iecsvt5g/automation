
base="/opt/tcpdump"
while :
do
    DATE=`date '+%Y-%m-%d %H:%M:%S'`
    echo $DATE >> $base/log 2>&1
    sh $base/get_tcpdump.sh  >> $base/log 2>&1
    sh $base/cleanup.sh  >> $base/log 2>&1
done

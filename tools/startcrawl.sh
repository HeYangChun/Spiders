#/bin/sh
logfile=/home/andy/workspace/crontask.log

cnt=$(ps -aux |grep scrapy|wc -l)
echo $cnt >> $logfile
if [ $cnt > 1 ];then
    echo "scrapy is running,not need to be started again" >>${logfile} 
    exit
fi

echo "starting scrapy...">>${logfile}
cd /home/andy/workspace/crawler
scrapy crawl tpysylt

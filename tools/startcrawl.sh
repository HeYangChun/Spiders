#/bin/sh
logfile=/home/andy/workspace/crontask.log

cnt=$(ps -aux |grep scrapy|wc -l)

if [ $cnt -gt 1 ];then
    echo "$(date)    scrapy is running,not need to be started again" >>${logfile} 
    exit
fi

echo "$(date)    starting scrapy...">>${logfile}
cd /home/andy/workspace/crawler

echo "$(date)    start crawl hslt..." >>${logfile}
scrapy crawl hslt

echo "$(date)    start crawl mllt..." >>${logfile}
scrapy crawl mllt

echo "$(date)    start crawl pacific..." >>${logfile}
scrapy crawl tpysylt

echo "$(date)    completed." >>${logfile}

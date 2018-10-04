#!/bin/bash
# Create data directories
mkdir -p /data/redis
mkdir -p /data/log/couchdb
mkdir -p /data/

# Start SSHD Service
/usr/sbin/sshd -D &


# Start MongoDB Database
echo -e "\e[96m#------------------------------------------------\e[m"
echo -e "\e[96m#              START COUCHDB DATABASE \e[m"
echo -e "\e[96m#------------------------------------------------\e[m"
/usr/bin/couchdb -b -o /data/log/couchdb/couchdb.stdout -e /data/log/couchdb/couchdb.stderr

## Start redis
#echo -e "\e[96m#------------------------------------------------\e[m"
#echo -e "\e[96m#              START REDIS SERVER \e[m"
#echo -e "\e[96m#------------------------------------------------\e[m"
#redis-server /etc/redis.conf || { echo "\e[31m Failed to start Redis Server. Exiting \e[m" ; exit 1;}
#
## Start  Kue
#echo -e "\e[96m#------------------------------------------------\e[m"
#echo -e "\e[96m#              START KUE WEB SERVER\e[m"
#echo -e "\e[96m#------------------------------------------------\e[m"
#
mkdir -p /data/log/ozone/kue
#FOREVER_LOGFILE="/data/log/ozone/kue/forever.log"
#KUE_LOGFILE="/data/log/ozone/kue/kue.log"
#FOREVER_PIDFILE="/var/run/kue.pid"
#SERVER_PATH="/opt/kue"
#KUE_PORT="3000"
#forever start -a -l ${FOREVER_LOGFILE} -o ${KUE_LOGFILE} --pidFile ${FOREVER_PIDFILE} --sourceDir=${SERVER_PATH} --id "kue" --workingDir=${SERVER_PATH} node_modules/kue/bin/kue-dashboard -p ${KUE_PORT} -r redis://P@ssw0rd@123@127.0.0.1:6379 > /data/log/ozone/kue/kue.out || { echo -e "\e[31m  Failed to start Kue Web Server. Exiting\e[m" ; exit 1;}
#
## Start Ozone Kue Command Processor
#echo -e "\e[96m#------------------------------------------------\e[m"
#echo -e "\e[96m#              START KUE CMD PROCESSOR \e[m"
#echo -e "\e[96m#------------------------------------------------\e[m"
#
mkdir -p /data/log/ozone/kueCmdProcessor
#FOREVER_LOGFILE="/data/log/ozone/kueCmdProcessor/forever.log"
#KUE_LOGFILE="/data/log/ozone/kueCmdProcessor/kueProcessor.log"
#FOREVER_PIDFILE="/var/run/kueCmdProcessor.pid"
#SERVER_PATH="/opt/web/server/components/kue"
#forever start -a -l ${FOREVER_LOGFILE} -o ${KUE_LOGFILE} --pidFile ${FOREVER_PIDFILE} --sourceDir=${SERVER_PATH} --id "kueCmdProcessor" --workingDir=${SERVER_PATH} kueCmdProcessor.js > /data/log/ozone/kueCmdProcessor/kueCmdProcessor.out || { echo -e "\e[31m  Failed to start Kue CMD Processor. Exiting \e[m"  ; exit 1;}
#
## Start Ozone Kue Task Processor
#echo -e "\e[96m#------------------------------------------------\e[m"
#echo -e "\e[96m#              START KUE TASK STATUS PROCESSOR \e[m"
#echo -e "\e[96m#------------------------------------------------\e[m"
#
mkdir -p /data/log/ozone/kueTaskStatusProcessor
#FOREVER_LOGFILE="/data/log/ozone/kueTaskStatusProcessor/forever.log"
#KUE_LOGFILE="/data/log/ozone/kueTaskStatusProcessor/kueProcessor.log"
#FOREVER_PIDFILE="/var/run/kueTaskStatusProcessor.pid"
#SERVER_PATH="/opt/web/server/components/kue"
#forever start -a -l ${FOREVER_LOGFILE} -o ${KUE_LOGFILE} --pidFile ${FOREVER_PIDFILE} --sourceDir=${SERVER_PATH} --id "kueTaskStatusProcessor" --workingDir=${SERVER_PATH} kueTaskStatusProcessor.js > /data/log/ozone/kueTaskStatusProcessor/kueTaskStatusProcessor.out || { echo -e "\e[31m Failed to start Kue Task Status Processor. Exiting \e[m" ; exit 1;}

# Start Lighttpd Server
echo -e "\e[96m#------------------------------------------------\e[m"
echo -e "\e[96m#              START LIGHTTPD SERVER \e[m"
echo -e "\e[96m#------------------------------------------------\e[m"
lighttpd start -f /etc/lighttpd/lighttpd.conf

# Start Ozone Web Server
echo -e "\e[96m#------------------------------------------------\e[m"
echo -e "\e[96m#              START OZONE WEB SERVER \e[m"
echo -e "\e[96m#------------------------------------------------\e[m"
mkdir -p /data/log/ozone/web
FOREVER_LOGFILE="/data/log/ozone/web/forever.log"
SERVER_LOGFILE="/data/log/ozone/web/server.log"
FOREVER_PIDFILE="/var/run/ozone_web.pid"
SERVER_PATH="/opt/web"
# For production
# forever start -a -l ${FOREVER_LOGFILE} -o ${SERVER_LOGFILE} --pidFile ${FOREVER_PIDFILE} --sourceDir=${SERVER_PATH} --id "ozoneWebServer" --workingDir=${SERVER_PATH} server > /data/log/ozone/web/server.out || { echo 'Failed to start Ozone Web Server. Exiting' ; exit 1;}
# forever logs -f 3

# forever server

# For development
forever -c bash grunt-script.sh



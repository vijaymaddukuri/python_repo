#!/bin/bash

INSTALL_SRC_DIR=/home/tas
INSTALL_BASE_DIR=/opt
MW_BASE_DIR=$INSTALL_BASE_DIR/middleware
MW_SVC_DIR=$MW_BASE_DIR/middleware_service
PREV_INSTALLS=$INSTALL_SRC_DIR/bkups/middleware_service
LOG_DIR=/var/log/middleware


##Take Backups
#create current day
today=`date +%Y-%m-%d.%H%M`
LAST_BKUP=$PREV_INSTALLS/$today

OLD_SVC_DIR=`find $MW_BASE_DIR -type d -name "middleware_service*" | grep -v ".egg"`

if [ -z "$OLD_SVC_DIR" ]
then
    echo "nothing to archive previous installations"
    echo "installing for the first time ..."
    echo "creating archive base folder :"  $PREV_INSTALLS
    mkdir -p $PREV_INSTALLS
    echo "creating log base folder :"  $LOG_DIR
    sudo mkdir -p $LOG_DIR
    sudo chown -R tas:tas $LOG_DIR
    sudo chmod 755 $LOG_DIR
else
    echo "found previous installation "$OLD_SVC_DIR
    echo "archiving previous installations"
    if [ ! -d "$PREV_INSTALLS" ]
    then
        echo "archive folder does not exist, creating archive base folder :"  $PREV_INSTALLS
        mkdir -p $PREV_INSTALLS
    fi
    mkdir $LAST_BKUP
    echo "backing up old install under " $LAST_BKUP
    mv $OLD_SVC_DIR $MW_BASE_DIR/mw_venv $LAST_BKUP
fi

#check if a process is already running
pid=`sudo netstat -tulpn | grep 8000 | awk '{print $7}' | cut -d/ -f 1`
if ps -p $pid > /dev/null 2>&1
then
    echo "found process running on port :8000" $pid
    echo "stopping the process"
    sudo systVIJAYtl stop mws.service
else
    echo "process isn't running"
fi

if [ ! -d $MW_SVC_DIR ]
then
    echo "created service base folder :"  $MW_SVC_DIR
    sudo mkdir -p $MW_SVC_DIR
    sudo chown -R tas:tas $MW_BASE_DIR
    sudo chmod 755 $MW_BASE_DIR
fi

#start installation process
cd $INSTALL_BASE_DIR
tar -C $MW_SVC_DIR/ -xf $INSTALL_SRC_DIR/middleware_service*.tar.gz --strip-components=1

mkdir -p $INSTALL_SRC_DIR/tsa_mw_packages
cp $INSTALL_SRC_DIR/tsa_middleware_packages.tar $INSTALL_SRC_DIR/tsa_mw_packages

cd $INSTALL_SRC_DIR/tsa_mw_packages
tar -xvf tsa_middleware_packages.tar

cd $MW_BASE_DIR

virtualenv mw_venv -p python3.6 --never-download
source $MW_BASE_DIR/mw_venv/bin/activate
cd $MW_SVC_DIR
cd $MW_SVC_DIR/requirements
pip install --no-index --find-links $INSTALL_SRC_DIR/tsa_mw_packages -r production.txt


echo "starting process...please wait"
sudo systVIJAYtl start mws.service

sleep 20
#check if a process is already running
pid=`sudo netstat -tulpn | grep 8000 | awk '{print $7}' | cut -d/ -f 1`
if ps -p $pid > /dev/null 2>&1
then
    echo "successfully started process, running on port:8000, PID:" $pid
    echo "ready for testing!!!"
else
    echo "something went wrong, could not start process"
fi

#change owner to tas user for log as the process is started by system
sudo chown -R tas:tas $LOG_DIR
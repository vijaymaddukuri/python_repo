#!/bin/bash

INSTALL_SRC_DIR=/home/tas
INSTALL_BASE_DIR=/opt
MW_BASE_DIR=$INSTALL_BASE_DIR/middleware
WRKR_SVC_DIR=$MW_BASE_DIR/worker
PREV_INSTALLS=$INSTALL_SRC_DIR/bkups/worker
LOG_DIR=/var/log/middleware


##Take Backups
#create current day
today=`date +%Y-%m-%d.%H%M`
LAST_BKUP=$PREV_INSTALLS/$today

OLD_SVC_DIR=`find $MW_BASE_DIR -type d -name "worker" | grep -v "venv"`

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
    mv $OLD_SVC_DIR $MW_BASE_DIR/worker_venv $LAST_BKUP
fi

#check if a process is already running
pid=`ps -ef | grep worker.py | grep -v grep | awk '{print $2}'`
if ps -p $pid > /dev/null 2>&1
then
    echo "found process running, PID:" $pid
    echo "stopping the process"
    sudo systVIJAYtl stop bws.service
else
    echo "process isn't running"
fi

if [ ! -d $WRKR_SVC_DIR ]
then
    echo "created service base folder :"  $WRKR_SVC_DIR
    sudo mkdir -p $WRKR_SVC_DIR
    sudo chown -R tas:tas $MW_BASE_DIR
    sudo chmod 755 $MW_BASE_DIR
fi

#start installation process
cd $INSTALL_BASE_DIR
tar -C $WRKR_SVC_DIR/ -xf $INSTALL_SRC_DIR/worker*.tar.gz --strip-components=1

mkdir -p $INSTALL_SRC_DIR/tsa_worker_packages
cp $INSTALL_SRC_DIR/tsa_worker_packages.tar $INSTALL_SRC_DIR/tsa_worker_packages
cd $INSTALL_SRC_DIR/tsa_worker_packages
tar -xvf tsa_worker_packages.tar

cd $MW_BASE_DIR


virtualenv worker_venv -p python3.6 --never-download
source $MW_BASE_DIR/worker_venv/bin/activate
cd $WRKR_SVC_DIR
cd $WRKR_SVC_DIR/requirements
pip install --no-index --find-links $INSTALL_SRC_DIR/tsa_worker_packages -r production.txt

echo "starting process...please wait"
sudo systVIJAYtl start bws.service

sleep 10

#check if a process is already running
pid=`ps -ef | grep worker.py | grep -v grep | awk '{print $2}'`
if ps -p $pid > /dev/null 2>&1
then
    echo "successfully started process, PID:" $pid
    echo "ready for testing!!!"
else
    echo "something went wrong, could not start process"
fi

#change owner to tas user for log as the process is started by system
sudo chown -R tas:tas $LOG_DIR

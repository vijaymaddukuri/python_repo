    #!/bin/bash

    INSTALL_SRC_DIR=/home/tas
    INSTALL_BASE_DIR=/opt
    TAS_BASE_DIR=$INSTALL_BASE_DIR/tas
    TAS_SVC_DIR=$TAS_BASE_DIR/tenant_automation_service  
    PREV_INSTALLS=$INSTALL_SRC_DIR/bkups/tas
    LOG_DIR=/var/log/tas


    ##Take Backups 
    #create current day
    today=`date +%Y-%m-%d.%H%M`
    LAST_BKUP=$PREV_INSTALLS/$today


    OLD_SVC_DIR=`find $TAS_BASE_DIR -type d -name "tenant_automation_service*" | grep -v ".egg"`
        
    if [  -z "$OLD_SVC_DIR" ]
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
        OLD_SVC_DIR=`find $TAS_BASE_DIR -type d -name "tenant_automation_service*" | grep -v ".egg"`
        echo "found previous installation "$OLD_SVC_DIR
        echo "archiving previous installations"  
        if [ ! -d "$PREV_INSTALLS" ]
        then
            echo "archive folder does not exist, creating archive base folder :"  $PREV_INSTALLS
            mkdir -p $PREV_INSTALLS
        fi
        mkdir $LAST_BKUP
        echo "backing up old install under " $LAST_BKUP
        mv $OLD_SVC_DIR $TAS_BASE_DIR/tas_venv  $LAST_BKUP
    fi

    #check if a process is already running
    pid=`sudo netstat -tulpn | grep 8000 | awk '{print $7}' | cut -d/ -f 1`
    if ps -p $pid > /dev/null 2>&1
    then
        echo "found process running on port :8000" $pid
        echo "stopping the process"
        sudo systVIJAYtl stop tas.service
    else    
        echo "process isn't running"
    fi

    if [ ! -d $TAS_SVC_DIR ]
    then 
        echo "created service base folder :"  $TAS_SVC_DIR
        sudo mkdir -p $TAS_SVC_DIR
        sudo chown -R tas:tas $TAS_BASE_DIR
        sudo chmod 755 $TAS_BASE_DIR
    fi 

    #start installation process
    cd $INSTALL_BASE_DIR
    tar -C $TAS_SVC_DIR/ -xf $INSTALL_SRC_DIR/tenant_automation_service*.tar.gz --strip-components=1


    mkdir -p $INSTALL_SRC_DIR/tsa_tams_packages
    cp $INSTALL_SRC_DIR/tsa_tams_packages.tar $INSTALL_SRC_DIR/tsa_tams_packages
    cd $INSTALL_SRC_DIR/tsa_tams_packages
    tar -xvf tsa_tams_packages.tar
    cd $TAS_BASE_DIR


    virtualenv tas_venv -p python3.6 --never-download
    source $TAS_BASE_DIR/tas_venv/bin/activate
    cd $TAS_SVC_DIR/requirements
    pip install --no-index --find-links $INSTALL_SRC_DIR/tsa_tams_packages -r production.txt
    
    echo "starting process...please wait"
    sudo systVIJAYtl start tas.service

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

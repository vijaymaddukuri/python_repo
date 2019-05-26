#!/bin/bash


BACKUP_LOG_DIR=/var/log/tas
MIDDLEWARE_LOG_DIR=/var/log/middleware

DIRS=($BACKUP_LOG_DIR $MIDDLEWARE_LOG_DIR)

echo "cleaning up log files if any..."
for DIR in ${DIRS[*]}
do
  if [ -d "$DIR" ]
   then
        # should clean up any files like  `*.log.1.gz` or *.log.gz  or  *.log
        for i in $DIR/*.log*;
        do
            if [ -f "$i" ]
            then
                echo "cleaned up one or more log archive files :" $i
                rm -rf $i
            fi
        done
    fi
done

# Clean up previous archive if any
if [ -d /home/tas/bkups ]
   then
    echo "cleaning up previous installation archives..."
    sudo rm -rf /home/tas/bkups
fi

# setting default file for bridgeburner
if [ -d /etc/bridgeburner/client/ ]
   then
    echo "putting default toml file for bb client..."
    sudo cp /home/tas/bridgeburner.toml /etc/bridgeburner/client/
fi

echo "Clearing bash history..."
sudo cat /dev/null > ~/.bash_history
history -c

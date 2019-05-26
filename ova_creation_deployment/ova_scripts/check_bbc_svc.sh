#!/bin/sh

#check if the process is already running
value=`sudo systVIJAYtl is-active bridgeburner`

active="active"
if [ $value != $active ]
then
  exec &>> /var/log/tas/bbc_svc.log
  sudo systVIJAYtl start bridgeburner

  # wait for 20 secs to confirm service start status
  sleep 20
  value=`sudo systVIJAYtl is-active bridgeburner`
  if [ $value = $active ]
  then
      echo  `date` "bridgeburner client service started successfully"
      break
  else
       echo `date` "unable to restart bridgeburner client service. Please contact administrator"
  fi

fi


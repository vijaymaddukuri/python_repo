# OVA config clean up scripts: 

Currently located at /home/tas of ova

1.  `ova_startup_script.py`: Startup script use to configure VM and service. The command 

    #### Middleware service
        $ python3.6 /root/ova_startup_script.py middleware
    #### Backup service
        $ python3.6 /root/ova_startup_script.py backup
    
    should be added to the file `/etc/rc.d/rc.local` (depending on the service to be configured), to start on boot.
    
2. `clean_up_app_logs.sh`: Script to clean up any application logs (generated during testing) in the ova environment before re-exporting the ova

3. `clear_ovaconfig.sh`: Script to undo the ova environment configurations before re-exporting the ova
4. 'bridgeburner.toml' : base .toml file required to be copied as /etc/bridgeburner/client/bridgeburner.toml (done as part of the clear_ovaconfig.sh script before re-exporting the ova) in the backup service

### Backup Service/Middleware Service : 
Currently located at /opt directory of respective ova's
* /opt/tas : Backup Service directory
* /opt/middleware : Middleware Service directory


### Steps to incorporate changes to the ova
1.  Import the ova

2.  On powering on the VM,
    * The VM gets configured and starts the specific services (using the script, `ova_startup_script.py`)
    
3.  Update the code and test the functionality

    * Tenant Automation Service
        
        1. You should already have a tar.gz from the latest tas build
  
        2. ssh to VM (TAS_SVC_VM_IP) and create directory `/home/tas` (please ignore this step if `/home/tas` already exists)        
        3. scp to copy tar file from dist folder in local machine to /home/tas in VM
        4. scp .../dist/tenant_automation_service-*.tar.gz root@<TAS_SVC_VM_IP>:/home/tas
        5. Also copy `install_tas_svc.sh` from this repo to root@<TAS_SVC_VM_IP>:/home/tas

                ./install_tas_svc.sh

        6. Running the `install_tas_svc.sh` will do the following tasks 
            * create necessary folders for the installation
            * stop the running webserver process if any
            * backs up the current version of code to /home/bkups/tas/<DATE> for archive purposes
            * replace the latest code in `/opt/tas` path. 
            * creates required python virtual environments if any
            * run the required installation process on the latest code
            * also brings up the web service process if there are no errors during installation.

        7. If there are errors while running the script manually debug the issue 

    * Middleware Service
        
        1. You should already have a tar.gz from the latest middleware build
  
        2. ssh to VM (MIDDLEWARE_SVC_VM_IP) and create directory `/home/tas` (please ignore this step if `/home/tas` already exists)        
        3. scp to copy tar file from dist folder in local machine to /home/tas in VM
        4. scp .../dist/middleware_service-0.0.1.tar.gz root@<MIDDLEWARE_SVC_VM_IP>:/home/tas
        5. Also copy `install_middleware_svc.sh` from this repo to root@<MIDDLEWARE_SVC_VM_IP>:/home/tas

                ./install_middleware_svc.sh

        6. Running the `install_middleware_svc.sh`  will do the following tasks 
            * create necessary folders for the installation
            * stop the running webserver process if any
            * backs up the current version of code to /home/bkups/middleware_service/<DATE> for archive purposes
            * replace the latest code in `/opt/middleware` path. 
            * creates required python virtual environments if any
            * run the required installation process on the latest code
            * also brings up the web service process if there are no errors during installation.
            
        7. If there are errors while running the script, please manually debug the issue 
        8. If there are no errors, you are good to proceed for functional testing

    * Worker (Backup Worker)
        
        1. You should already have a tar.gz from the latest worker build
  
        2. ssh to VM (MIDDLEWARE_SVC_VM_IP) and create directory `/home/tas` (please ignore this step if `/home/tas` already exists)        
        3. scp to copy tar file from dist folder in local machine to /home/tas in VM
        4. scp .../dist/worker-0.0.1.tar.gz root@<MIDDLEWARE_SVC_VM_IP>:/home/tas
        5. Also copy `install_middleware_svc.sh` from this repo to root@<MIDDLEWARE_SVC_VM_IP>:/home/tas

                ./install_worker_svc.sh

        6. Running the `install_worker_svc.sh` will do the following tasks 
            * create necessary folders for the installation
            * stop the running webserver process if any
            * backs up the current version of code to /home/bkups/worker/<DATE> for archive purposes
            * replace the latest code in `/opt/middleware` path. 
            * creates required python virtual environments if any
            * run the required installation process on the latest code
            * also brings up the worker process if there are no errors during installation.
            
        7. If there are errors while running the script, please manually debug the issue 
        8. If there are no errors, you are good to proceed for functional testing


4.  Once testing is complete, it is necessary to clean up the ova of any logs and local configuration values before it is ready to ship. Below steps are to be run for the same

     1.  Run `clean_up_app_logs.sh` to cleanup any of the application logs.

        /root/clean_up_app_logs.sh        

    2. Run `clear_ovaconfig.sh` to clean up the base configurations done by the startup script.
    
        /root/clear_ovaconfig.sh
    
5.  Finally export the ova, after making sure all the local configuration is wiped out from ova

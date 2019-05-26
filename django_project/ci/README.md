Prerequisite:

 - We need write and execution permissions to copy the cherrypy packages.


Steps to copy the cherrypy packages:

Step1:

    - untar the tenant_automation_service-cherrypy_<vesion> package in any folder, except tmp directory:

        command: tar -xvf  tenant_automation_service-cherrypy_<vesion>

Step2:

    Go to the directory where tenant_automation_service-cherrypy folder is extracted.

Step3 (Fresh install):

    - Give execution permissions to the shell script - configure_tsa_salt.sh

    - Execute the configure_tsa_salt.sh shell script for fresh install

        command:
        tar -xvf  tenant_automation_service-cherrypy_<vesion>
        cd tenant_automation_service-cherrypy_<vesion>
        cd configure_tsa_salt_<version>
        chmod -R 777 configure_tsa_salt.sh
        ./configure_tsa_salt.sh -u <username> -p <password>

                     [or]
Step4 (Salt directory upgrade):

    - Give execution permissions to the shell script upgrade_salt_dir.sh
    - Execute the upgrade_salt_dir.sh shell script.
        command:
        tar -xvf  tenant_automation_service-cherrypy_<vesion>
        cd tenant_automation_service-cherrypy_<vesion>
        cd configure_tsa_salt_<version>
        chmod -R 777 upgrade_salt_dir.sh
        ./upgrade_salt_dir.sh


Step4: Version compatibility details:

    Installation of CherryPy package is very specific to salt-master version.

        1. For Salt-master version - 2018.3.2-1.el7 following artifacts will work:
                salt-api-2018.3.2-1.el7.noarch.rpm
                python-cherrypy-5.6.0-2.el7.noarch.rpm

           Note: Command to fetch salt-master version from terminal: rpm -qa | grep salt-master

        2. For different version of Salt-master we need to download respective salt-api and python-cherrypy versions.

        4. Remove the existing rpm's located in /srv/install/centos directory

        5. And copy the downloaded rpm's into the "/srv/install/centos" directory.




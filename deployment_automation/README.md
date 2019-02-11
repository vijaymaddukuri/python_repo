#Prerequisites:

    - Python 3.5 or above need to be installed

    - Paramiko python module should be installed

    - Yaml module also need to installed

        Example: pip install paramiko
                 pip install pyyaml
                 pip install requests

    - If internet is not there to install python, download the python from below FTP:

      - Go to the Jump Host
      - Login to FTP server from WEB: https://ftp.emc.com/action/login?domain=ftp.emc.com
      - Goto python folder and download, python3.7 zip

    - Untar the python zip folder in any directory.

    - Set the PATH environmental variables:

        Example:  Path: C:\python3.5\;C:\python3.5\Lib;C:\python3.5\Lib\site-packages


# Clone the project:

    Step1: Clone the git repo in the default location "C:\" or any other location

            Git repo: https://github.emcrubicon.com/AAI/deployment_automation.git


# Steps to copy certificates from BB server to BB Client

    Step1: After cloning the project, goto the directory

           Example: C:\deployment_automation\bb_certificate_generation

    Step2: Open bb_certificate_generation -> config.yaml and update the BB Server, BB Client and NAT Server details.

    Step3: From the command prompt go the project directory

        Example: C:\deployment_automation\bb_certificate_generation

    Step4: Execute the python file update_bb_certificates.py

        Example: Command to run the python script

           - python update_bb_certificates.py

# Steps to validate middleware API's:

   Step1: Upload mw and worker yaml files to Middleware VM (Optional)

     - Go to cofig -> middleware folder and open the config.yaml file
     - Fill the details
     - GO to cofig -> worker folder and open the config.yaml file
     - Fill the details.

   Step2: Execute the middleware validation script:

       - To execute the middleware validation python script, we need to fill config.yaml
       - Go to config directory and open config.yaml and fill below details:
            - MW_DETAILS
       - After filling the config.yaml, execute the middleware_worker_validation.py from command prompt.

           Here are the options to execute middleware_worker_validation.py script:

                Option1: python middleware_worker_validation.py (default)

                    Validation: End points, health and services validation

                         - Middleware and worker services
                         - Health check
                         - Consul connectivity
                         - Bridgeburner connectivity
                         - Vulnerability end point connectivity

                Option2: python middleware_worker_validation.py -a

                    arg: <'-a' or "--allapi">: To run all available MW APIs

                    Validation:
                        - Along with end point validation, option to run all middleware APIS
                                        (backup, monitoring, security and vulnerability)

                Option3: python middleware_worker_validation.py -b

                    arg: <'-b' or "--backupapi">: To run MW backup API
                    Validation:
                        - Option to run backup middleware API

                Option4: python middleware_worker_validation.py -s

                    arg: <'-s' or "--securityapi">: To run MW security API

                Option5: python middleware_worker_validation.py -m

                    arg: <'-m' or "--monitoringapi">: To run MW monitoring API

                Option6: python middleware_worker_validation.py -v

                    arg: <'-v' or "--vulnerabilityapi">: To run MW vulnerability API

                Option7: python middleware_worker_validation.py -y

                    arg: <'-y' or "--uploadyaml">: To upload middleware and worker yaml files to MW vm

                    Validation:
                        - Option to upload middleware and worker yaml files to Middleware VM


# Steps to validate TAS API's:

   Step1: Upload tas config.yaml files to TAS VM (Optional)

     - Go to cofig -> tas folder and open the config.yaml file
     - Fill the details

   Step2: Execute the tas validation script:

       - To execute the tas validation python script, we need to fill config.yaml

       - Go to config directory and open config.yaml and fill below details:
            - NAT_VM
            - TAS_DETAILS
            - VM_DETAILS

       - After filling the config.yaml, execute the tas_validation.py from command prompt.

           Here are the options to execute tas_validation.py script:

               Option1: python tas_validation.py (default)

                    Validation: End points, health and services validation

                         - TAS services
                         - Health check
                         - Salt master connectivity
                         - Netwroker endpoint connectivity
                         - DSM end point connectivity
                         - Nimsoft end point connectivity

               Option 2: python tas_validation.py -a

                    arg: <'-a' or "--allapi">: To run all available TAS APIs

                    Validation:
                        - Along with end point validation, option to run all TAS APIS
                                                        (backup, monitoring and security)

               Option3: python tas_validation.py -b

                    arg: <'-b' or "--backupapi">: To run TASbackup API
                    Validation:
                        - Option to run backup TAS API

               Option4: python tas_validation.py -s

                    arg: <'-s' or "--securityapi">: To run TAS security API

               Option5: python tas_validation.py -m

                    arg: <'-m' or "--monitoringapi">: To run TAS monitoring API

               Option6: python tas_validation.py -v

                    arg: <'-v' or "--vulnerabilityapi">: To run TAS vulnerability API

               Option7: python tas_validation.py -y

                    arg: <'-y' or "--uploadyaml">: To upload TAS and worker yaml files to MW vm

                    Validation:
                        - Option to upload config.yaml files to TAS VM
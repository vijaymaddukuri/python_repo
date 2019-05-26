## BackupService
Backup Service automates the configuration of backup policies on a given VM.
Wiki link - https://docs.VIJAYrubicon.com/display/VEB/Backup+Automation

### Software Requirments

    Python 3.5


### Clone Repo

    # git clone git@github.com:AAI/ONBFactory.git


### Python Virtual Environment

1. Create Python virtual environment
    
        $ virtualenv <name-of-folder>
    
2. Activate virtual environment 
    
        $ source <path-to-folder>/bin/activate
    
3. Deactivate virtual environment
    
        $ deactivate
    

### Install requirements

* Install python project dependencies for dev environment
    
    
        $ pip3 install -r requirements/local.txt

* Install python project dependencies for production environment


        $ pip3 install -r requirements/production.txt

### Endpoint Configuration

 * Please change the following Configurations in <root>/config.yaml
   
       - Salt Master Details (Can be found in /etc/salt/master File in Salt-Master)
       - Networker Server Details (Contact your administrator)
   
### Command to run the Project

1.  Local
    
        $ python manage.py runserver
    

2. production

        $ python manage.py collectstatic
        $ gunicorn --bind 0.0.0.0:$PORT --access-logfile - ONBFactory.wsgi:application
    

### Run Flake8 before commit (run on the root of the project)

        $ flake8


### Apps.py - What is this and how it is used

    https://docs.djangoproject.com/en/2.0/ref/applications/#application-configuration


### Swagger API View

    http://localhost:8000/api/v1/swagger/


### Build and Run the project locally 

1. Execute build.sh from project root - to generate build artifacts in the dist directory

        $ ./build.sh

2. Find the tar.gz file in the dist directory under project root and command to untar it

        $ tar -xzvf tenant_automation_service-0.0.1.tar.gz

        $ cd tenant_automation_service-0.0.1

3. Install the dependencies for the project in the exploded folder tenant_automation_service-0.0.1

        $ python setup.py install
        
        Note: Make sure to use python 3.5 for installing the dependencies

4. Command to run the Project

        $ gunicorn --bind 0.0.0.0:8000 --access-logfile - ONBFactory.wsgi:application


### Running BackupService in docker-compose
1. Clone repo

    
        $ git clone git@github.com:AAI/ONBFactory.git
        $ cd ONBFactory
    
2. Install `docker-compose` (requires [Docker](https://docs.docker.com/engine/installation/))
   
   https://docs.docker.com/compose/install/


3. Bring up services defined in `docker-compose.yml`

    Ensure the Docker images are up-to-date. The initial pull of all images will take several minutes.

   
        $ docker-compose pull

        $ docker-compose up -d
   
4. Logs

    Logs can be checked with:

    
        $ docker-compose logs -f <service>

        # i.e. show last 10 logs and then follow
        $ docker-compose logs -f --tail 10 backup-service*`
    

    Or can just follow all logs for all services

   
         $ docker-compose logs -f --tail 10
   

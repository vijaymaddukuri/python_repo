dir=$(pwd)

release=$(cat /etc/*release | grep 'CentOS\|Ubuntu')
if [[ $release == *"CentOS"* ]]; then
 echo "Running CentOS Installers for pip"
 sudo yum -y install epel-release 
 sudo yum -y install python-pip
 #pip install virtualenv  
fi
if [[ $release == *"Ubuntu"* ]]; then
 echo "Running Ubuntu Installers for pip"
 sudo apt-get -y install python-pip
 #pip install virtualenv
fi

#Download the Firefox geckodriver,untar,give permissions and set PATH
cd /usr/local/bin
sudo rm -rf gecko*
sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
sudo tar -xvzf geckodriver*
sudo chmod +x geckodriver
export PATH=$PATH:/usr/local/bin/geckodriver
echo $PATH 

#Untar the Test Automation folder and set PYTHONPATH
cd $dir
tar -xvf new_project_automation.tar
export PYTHONPATH=$PYTHONPATH:$dir/new_project_automation

#Run virtualenv in which dependent packages will be downloaded
#virtualenv venv2.7 -p python2.7
#source venv2.7/bin/activate

#Install the dependencies/packages required 
cd new_project_automation
pip install -r requirements.txt

#Run the test Automation
robot tests/




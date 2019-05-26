dir=$(pwd)

cd /tmp && \
    wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz && \
    tar -xvf setuptools-1.4.2.tar.gz && \
    cd setuptools-1.4.2 && \
    python2.7 setup.py install && \
    curl https://bootstrap.pypa.io/get-pip.py | python2.7 - && \
    pip install virtualenv
virtualenv venv2.7 -p python2.7
source venv2.7/bin/activate
pip2.7 install jmespath
pip2.7 install pyyaml
pip2.7 install requests
pip2.7 install robotframework
pip2.7 install robotframework-requests
pip2.7 install robotframework-httplibrary
pip2.7 install simple-yaml
pip2.7 install selenium
pip2.7 install robotframework-selenium2library
pip2.7 install paramiko
cd $dir && cd ..
dir=$(pwd)
export PYTHONPATH=$PYTHONPATH:$dir/TAveche
cd $dir/TAveche/robot_tests/backup_service_automation
http_proxy="http://10.131.236.9:3128"
https_proxy="https://10.131.236.9:3128"

no_proxy="10.100.249.38, 10.100.249.44, 10.100.249.48"
wget http://10.100.249.44:8000/api/v1/
robot -b debuglogs.txt -L DEBUG:INFO -x junit.xml -d logs --timestampoutputs backup_automation.robot
deactivate

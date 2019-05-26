cd /tmp/$1  
virtualenv venv -p python3.6
source venv/bin/activate
python3.6 setup.py install
pkill gunicorn
no_proxy="10.100.249.38, 10.100.249.44, 10.100.249.48"
gunicorn --bind 0.0.0.0:8000 --access-logfile - ONBFactory.wsgi:application --daemon

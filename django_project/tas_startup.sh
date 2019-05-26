source /opt/tas/tas_venv/bin/activate
cd /opt/tas/tenant_automation_service
value=$(grep -A3 'workers:' config.yaml | grep no_of_proc); value=${value//*no_of_proc/}; value=$(echo $value | tr -d ':') value=$(echo $value | tr -d ' ')
echo "Number of workers : "$value
gunicorn --bind 0.0.0.0:8000 --access-logfile - ONBFactory.wsgi:application --workers=$value --timeout=600

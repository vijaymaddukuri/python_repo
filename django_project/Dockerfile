FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /backup-service

# Adds our application code to the image
#TODO we will get tar file from repo

COPY ./dist/tenant_automation_service-0.0.1.tar.gz backup-service
WORKDIR backup-service
RUN apt-get install xz-utils && tar -C /backup-service/ -xf /backup-service/tenant_automation_service-0.0.1.tar.gz

#TODO Version will change once get artifacts from repo
WORKDIR tenant_automation_service-0.0.1

RUN python setup.py install
EXPOSE 8000

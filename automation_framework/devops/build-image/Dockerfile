FROM artifactory.core.rcsops.com/devops-centos7-build

ENV http_proxy=10.131.236.9:3128 https_proxy=10.131.236.9:3128 LANG=en_US.UTF-8

MAINTAINER vijay.maddukuri@VIJAY.com

RUN yum_install curl epel-release java-1.8.0-openjdk-devel libxslt tar rpm-build \
 git perl-Git \
 && yum clean all

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0" >> /home/jenkins/.bashrc
RUN yum groupinstall -y 'development tools'
RUN yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel xz-libs

ENV APPLICATION_DIR="/srv/application"
# Install required packages
RUN yum update -y; yum clean all
RUN yum -y install wget

RUN wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz && \
                tar -xvf setuptools-1.4.2.tar.gz && \
                cd setuptools-1.4.2 && \
                python2.7 setup.py install && \
                curl https://bootstrap.pypa.io/get-pip.py | python2.7 - && \
                pip install virtualenv
RUN pip2.7 install jmespath
RUN pip2.7 install pyyaml
RUN pip2.7 install requests
RUN pip2.7 install robotframework
RUN pip2.7 install robotframework-requests
RUN pip2.7 install robotframework-httplibrary
RUN pip2.7 install simple-yaml
RUN pip2.7 install robotframework-selenium2library
RUN pip2.7 install paramiko


USER build
LABEL license= name=artifactory.core.rcsops.com/appdirector-brooklyn_centos6 vendor="VIJAY Inc."

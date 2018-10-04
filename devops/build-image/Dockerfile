FROM artifactory.core.rcsops.com/devops-centos7-build

ENV http_proxy=10.131.1.2:3128 https_proxy=10.131.1.2:3128 LANG=en_US.UTF-8

MAINTAINER vijaymaddukuri@yahoo.com

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
#PYTHON 3.2
RUN yum -y groupinstall "Development tools"
RUN yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
RUN yum -y install epel-release
RUN yum -y install python34
RUN yum -y install python34-devel
RUN yum -y install python34-setuptools
RUN cd /usr/lib/python3.4/site-packages/ && python3 easy_install.py pip
RUN pip3.4 install virtualenv
RUN wget https://artifactory.core.rcsops.com:443/artifactory/core-generic-local/VMware-ovftool-3.5.0-1274719-lin.x86_64.bundle
RUN chmod a+x VMware-ovftool-3.5.0-1274719-lin.x86_64.bundle
RUN yes | ./VMware-ovftool-3.5.0-1274719-lin.x86_64.bundle


USER build
LABEL license= name=artifactory.core.rcsops.com/appdirector-brooklyn_centos6 vendor="Virtustream Inc."

FROM sylus2207/djangovh:latest

ENV http_proxy=10.131.236.9:3128 https_proxy=10.131.236.9:3128 LANG=en_US.UTF-8

MAINTAINER vicky@VIJAY.com

RUN yum_install curl epel-release java-1.8.0-openjdk-devel libxslt tar rpm-build \
 git perl-Git  \
 && yum clean all

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0" >> /home/jenkins/.bashrc

RUN yum install ansible -y
RUN echo "$PWD"
RUN sudo mkdir sample_code
RUN sudo mkdir tmp/sample_code
USER root

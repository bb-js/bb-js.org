FROM centos:7
MAINTAINER the5fire "thefivefire@gmail.com"
ENV REFRESHED_AT 2015-01-28
ENV PYTHONUNBUFFERED 1

RUN rpm -iUvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
RUN yum -y update
RUN yum -y install gcc
RUN yum -y install python-devel python-pip

RUN mkdir /code
WORKDIR /code
ADD ./ /code/
RUN pip install -r /code/requirements.txt
WORKDIR /code/src/

EXPOSE 8001
EXPOSE 10843

CMD /code/src/bb_server.py 8001

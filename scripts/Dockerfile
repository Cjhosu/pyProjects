FROM registry.cmmint.net/cmm/centos6-python36
COPY list_incidents.py $APP_HOME/
USER root
ENV PATH "$PATH:/bin/sh"
RUN yum -y install nc
RUN pip install requests
CMD python ./list_incidents.py

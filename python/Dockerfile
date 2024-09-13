FROM ubuntu

RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install python3 libapache2-mod-wsgi-py3
RUN apt-get -y install python3-dev libldap2-dev libsasl2-dev ldap-utils
RUN ln /usr/bin/python3 /usr/bin/python
RUN apt-get -y install python3-pip
RUN pip install --upgrade pip
RUN pip install django ptvsd
RUN pip install tzdata
RUN pip install djangorestframework
RUN pip install PyJWT
RUN pip install python-ldap
RUN pip install mysql-connector-python
RUN pip install requests
RUN pip install Celery
RUN pip install redis

ADD ./demo_site.conf /etc/apache2/sites-available/000-default.conf
RUN cp /etc/apache2/mods-available/rewrite.load /etc/apache2/mods-enabled/ && \
    cp /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/
RUN mkdir /var/log/secsaas
RUN chmod 777 /var/log/secsaas

EXPOSE 80 3500
CMD ["apache2ctl", "-D", "FOREGROUND"]

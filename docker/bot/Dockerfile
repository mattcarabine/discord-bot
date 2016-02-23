FROM python:2.7

# Set-up libcouchbase
RUN apt-get update && apt-get -y install libev4

RUN wget http://packages.couchbase.com/clients/c/libcouchbase-2.5.3_wheezy_amd64.tar
RUN tar xf libcouchbase-2.5.3_wheezy_amd64.tar
RUN dpkg -i libcouchbase-2.5.3_wheezy_amd64/*.deb

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD docker/bot/run.sh /run.sh
RUN chmod +x /run.sh
CMD /run.sh
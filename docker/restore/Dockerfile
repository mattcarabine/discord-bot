FROM couchbase/server:enterprise-4.1.0
RUN apt-get update && apt-get install -y python-pip
RUN pip install awscli

ADD docker/restore/run.sh /run.sh
RUN chmod +x /run.sh
WORKDIR /
CMD /run.sh

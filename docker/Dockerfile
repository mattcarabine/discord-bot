FROM python:2.7

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD docker/run.sh /run.sh
RUN chmod +x /run.sh
CMD /run.sh
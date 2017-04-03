FROM python:2.7

RUN pip install pyyaml
RUN pip install requests
RUN pip install lxml
RUN pip install twilio

ADD config.yaml /
ADD poll.py /

ENTRYPOINT [ "python", "./poll.py" ]

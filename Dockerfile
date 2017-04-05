FROM python:2.7

RUN pip install pyyaml
RUN pip install requests
RUN pip install lxml
RUN pip install twilio

ADD gamechecker.py /
ADD test_gamechecker.py /
ADD resources/ /resources/

RUN ["python", "test_gamechecker.py"]

ADD config.yaml /

ENTRYPOINT [ "python", "gamechecker.py" ]

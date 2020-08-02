FROM python:3.6.1-alpine

WORKDIR /teeny-weeny

ADD . /teeny-weeny

RUN pip install -r requirements.txt

CMD ["python3","main.py"]

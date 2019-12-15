FROM python:3.7-slim

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py /bin

CMD python3 /bin/main.py

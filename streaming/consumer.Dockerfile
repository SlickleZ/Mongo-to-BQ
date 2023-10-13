FROM python:3.11.6

WORKDIR /consumer

COPY requirements.txt gsa.json /consumer/
RUN pip install -r requirements.txt

COPY src/consumer.py .
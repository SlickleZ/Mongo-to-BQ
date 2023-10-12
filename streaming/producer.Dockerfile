FROM python:3.11.6

WORKDIR /producer

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/producer.py .
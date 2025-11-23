FROM python:3.12-slim

WORKDIR /pdfapp
COPY . /pdfapp

RUN pip install -r requirements.txt

CMD["python", "main.py"]
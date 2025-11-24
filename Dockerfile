FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y python3-tk tk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /pdfapp
COPY . /pdfapp

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

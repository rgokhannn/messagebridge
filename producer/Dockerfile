FROM python:3.8-slim

WORKDIR /producer

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py .

CMD ["python", "producer.py"]
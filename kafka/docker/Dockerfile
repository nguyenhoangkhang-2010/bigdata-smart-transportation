FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir \
    pyarrow==21.0.0 \
    confluent-kafka==2.11.1 \
    requests==2.32.5 \
    pydantic-settings

COPY backend /app/backend
COPY kafka/producers /app/kafka/producers

CMD ["python", "-m", "kafka.producers.tlc_producer"]
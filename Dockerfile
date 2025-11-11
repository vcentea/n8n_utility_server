FROM python:3.12-alpine

RUN apk add --no-cache poppler-utils

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PORT=2277
ENV TEMP_PATH=/tmp/pdf_service

RUN mkdir -p /tmp/pdf_service

EXPOSE 2277

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}


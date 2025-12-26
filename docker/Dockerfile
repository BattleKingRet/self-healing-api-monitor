FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

ENV APP_NAME="self-healing-api-monitor"
ENV ENV="prod"
ENV LOG_LEVEL="INFO"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

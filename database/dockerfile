FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
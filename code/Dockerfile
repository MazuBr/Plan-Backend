
FROM python:3.11.9-slim
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8000
ENV PORT 8000

CMD ["python3", "main.py"]
# exec uvicorn main:app --host 0.0.0.0 --port $PORT --ssl-keyfile /app/src/cert/key.pem --ssl-certfile /app/src/cert/cert.pem
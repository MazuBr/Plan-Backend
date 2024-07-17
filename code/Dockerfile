
FROM python:3.11.9-slim
WORKDIR /app
COPY code/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY code /app/code
EXPOSE 8000

CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-certfile", "/app/code/cert/cert.pem", "--ssl-keyfile", "/app/code/cert/key.pem"]

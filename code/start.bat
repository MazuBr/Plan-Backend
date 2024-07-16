@echo off
python -m uvicorn main:app --ssl-certfile cert/cert.pem --ssl-keyfile cert/key.pem --reload
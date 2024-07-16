@echo off
python -m uvicorn main:app --ssl-certfile cert.pem --ssl-keyfile key.pem --reload
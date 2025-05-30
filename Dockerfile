FROM python:3.13-slim

WORKDIR /parser_drianberris

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
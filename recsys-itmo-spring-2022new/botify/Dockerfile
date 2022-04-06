<<<<<<< HEAD
FROM python:3.7-slim-buster
=======
FROM python:3.8-slim-buster
>>>>>>> eb316f8... HW done

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY botify ./botify
COPY data ./data

RUN mkdir -p ./log

ENV PYTHONPATH "${PYTHONPATH}:/app"
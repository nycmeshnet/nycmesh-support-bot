# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 

# Note: .env file is not coppied due to .dockerignore.  When deploying to server .env is recreated though GitHub actions secrets and then liked to container through a volume.
COPY . .

RUN pip3 install -e .

CMD supportbot-server
# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update; \
    apt-get install -y --no-install-recommends \
            iputils-ping \
            jq \
            traceroute \
            ssh \
            sshpass \
    ; \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 

# Note: .env file is not coppied due to .dockerignore.  When deploying to server .env is recreated though GitHub actions secrets and then liked to container through a volume.
COPY . .

RUN chmod u+r+x bin/nn_stats.sh
ENV PATH="${PATH}:/app/bin"

ENV PYTHONUNBUFFERED=True

WORKDIR /app/supportbot
RUN pip3 install -e .

WORKDIR /app/mesh-database-client
RUN pip3 install -e .

WORKDIR /app

CMD supportbot-server
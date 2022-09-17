# syntax=docker/dockerfile:1

FROM byxorna/nycmesh-tool:latest AS mesh-tool

FROM python:3.9-slim-buster

COPY --from=mesh-tool /nycmesh-tool /app/bin/nycmesh-tool

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

RUN pip3 install -e .

CMD supportbot-server
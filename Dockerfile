# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

# Note: Eventaully many files will be omitted. Images build with current Dockerfile should not be pushed to a public repository.
COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install -e .

CMD supportbot-server
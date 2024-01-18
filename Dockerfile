FROM ubuntu:latest
LABEL authors="riko"

ENTRYPOINT ["top", "-b"]
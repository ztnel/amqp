FROM ubuntu:latest

# Grab dependencies and generate locale
RUN apt update && apt upgrade -y && apt install -y python3 python3-pip sudo locales && locale-gen en_US.UTF-8

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "./p1/entry.sh" ]
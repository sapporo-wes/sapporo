FROM python:3.7-slim

WORKDIR /opt/NIG-api

RUN apt update \
 && apt install -y \
    build-essential \
    curl \
    silversearcher-ag \
    tree \
    unzip \
    vim \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/NIG-api
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
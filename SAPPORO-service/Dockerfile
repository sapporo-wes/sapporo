FROM python:slim

WORKDIR /opt/SAPPORO-service

RUN apt update && \
    apt install -y \
    build-essential \
    iproute2 \
    jq \
    procps && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp

RUN pip install -U pip wheel setuptools && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

COPY entry_point.sh /opt/SAPPORO-service

CMD ["tail", "-f", "/dev/null"]

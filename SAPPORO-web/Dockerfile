FROM python:slim

WORKDIR /opt/SAPPORO-web

RUN apt update && \
    apt install -y \
    build-essential \
    iproute2 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp

RUN pip install -U pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

COPY entry_point.sh /opt/SAPPORO-web
ADD https://raw.githubusercontent.com/eficode/wait-for/master/wait-for /opt/SAPPORO-web

CMD ["tail", "-f", "/dev/null"]

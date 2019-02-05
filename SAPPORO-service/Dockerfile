FROM python:alpine

WORKDIR /opt/SAPPORO-service

RUN apk --update add --no-cache \
    gcc \
    libc-dev \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    pcre-dev

COPY requirements.txt /tmp

RUN pip install -U pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

CMD ["tail", "-f", "/dev/null"]

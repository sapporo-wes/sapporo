FROM python:alpine

WORKDIR /opt/SAPPORO-web

RUN apk --update add --no-cache \
    gcc \
    libc-dev \
    linux-headers \
    pcre-dev

COPY requirements.txt /tmp

RUN pip install -U pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

COPY entrypoint.sh /opt/SAPPORO-web

CMD ["tail", "-f", "/dev/null"]
FROM python:alpine

WORKDIR /opt/SAPPORO-service

RUN apk --update add --no-cache \
    gcc \
    jq \
    libc-dev \
    libc6-compat \
    libltdl \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    pcre-dev

COPY requirements.txt /tmp

RUN pip install -U pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

COPY entry_point.sh /opt/SAPPORO-service

CMD ["tail", "-f", "/dev/null"]

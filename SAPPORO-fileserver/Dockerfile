FROM minio/minio:latest

RUN curl -L https://dl.minio.io/client/mc/release/linux-amd64/mc > /usr/local/bin/mc && \
    chmod +x /usr/local/bin/mc

CMD ["server", "/data"]

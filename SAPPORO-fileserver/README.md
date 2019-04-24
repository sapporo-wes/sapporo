# SAPPORO-fileserver

SAPPORO-fileserver is divided into file storage for input and file storage for output. File storage for input uses nginx. The file storage for output uses [Minio](https://www.minio.io) which is a simple S3 compatible object storage.

[Japanese Document](https://hackmd.io/s/rJHpJwkdE)

## Deployment

Using docker-compose.

```shell
$ git clone https://github.com/suecharo/SAPPORO.git
$ cd SAPPORO/SAPPORO-fileserver
$ vim docker-compose.yml

# Edit HERE!
environment:
    MINIO_ACCESS_KEY: access_key
    MINIO_SECRET_KEY: secret_access_key

$ docker-compose up -d
```

## Usage of File Storage for Input

First, examine the path of dir in `docker-compose.yml` and edit `nginx.conf`.

```shell
$ pwd
/home/ubuntu/SAPPORO/SAPPORO-fileserver
$ vim nginx.conf

    server {
        listen 80;
        listen [::]:80;
        server_name localhost;
        root /home/ubuntu/SAPPORO/SAPPORO-fileserver/data;    # HERE
        location / {
            autoindex on;
        }

$ docker-compose restart input
```

In your browser, access to `localhost:1124`.

You can get the file URL, after change `localhost:1124` to `sapporo-fileserver-input`.

```
http://localhost:1124/input/small.ERR034597_1.fq

# ->

http://sapporo-fileserver-input/input/small.ERR034597_1.fq
```

## Usage of File Storage for Output


In browser, access to `localhost:1123`.

![Mineo Login](https://i.imgur.com/m1ghCUn.png)

Enter the Access Key and Secret Key set above.

![Minio Home](https://i.imgur.com/zKFAXzd.png)

---

Create a bucket. You can do this from the browser or from CLI.

The following is an example of using CLI.

```shell
$ docker-compose exec app mc config host add sapporo http://0.0.0.0:80 access_key secret_access_key
$ docker-compose exec app mc mb sapporo/sapporo
```

This will create a bucket called `sapporo`.

---

In Workflow Prepare, specify SAPPORO-fileserver instead of S3.

![Test](https://i.imgur.com/y0Tv7JZ.png)

---

The result is output as follows.

![Output](https://i.imgur.com/scZJbcm.png)

The entity of output exists under `SAPPORO/SAPPORO-fileserver/data/sapporo`.

```shell
$ cd data/sapporo
$ ls
cwl_upload
$ cd cwl_upload
$ ls
small.ERR034597_1_fastqc.html  small.ERR034597_1.trimmed_fastqc.html  small.ERR034597_1.trimmed.fq
```

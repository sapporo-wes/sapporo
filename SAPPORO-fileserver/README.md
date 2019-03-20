# SAPPORO-fileserver

SAPPORO-service is file storage for managing data. We are using [Minio](https://www.minio.io), which is a simple S3 compatible object storage.

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

In browser, go to `localhost: 1123`.

![Mineo Login](https://i.imgur.com/m1ghCUn.png)

Enter the Access Key and Secret Key set above.

![Minio Home](https://i.imgur.com/zKFAXzd.png)

---

Create a bucket. You can do this from the browser or from CLI.

The following is an example of using CLI.

```shell
$ docker-compose exec app mc config host add sapporo http://0.0.0.0:1123 access_key secret_access_key
$ docker-compose exec app mc mb sapporo/sapporo
```

This will create a bucket called `sapporo`.

## Usage

First, check the IP of Docker Host of SAPPORO-service.

```bash
$ cd ../SAPPORO-service
$ docker-compose exec app ip route
default via 192.168.112.1 dev eth0    # THIS!!
192.168.224.0/20 dev eth0 scope link  src 192.168.224.3
```

---

In Workflow Prepare, specify SAPPORO-fileserver instead of S3.

![Test](https://i.imgur.com/zBbrkv0.png)

---

The result is output as follows.

![Output](https://i.imgur.com/Aay2M07.png)

The entity of output exists under `SAPPORO/SAPPORO-fileserver/data/sapporo`.

```shell
$ cd data/sapporo
$ ls
cwl_upload
$ cd cwl_upload
$ ls
curl_fastq_stderr.log           fastqc_trimed_fastq_stdout.log  fastq.trimed.fq         upload_url.txt
fastqc_fastq_stderr.log         fastq_fastqc.html               s3_upload_stderr.log
fastqc_fastq_stdout.log         fastq.fq                        trimmomatic_stderr.log
fastqc_trimed_fastq_stderr.log  fastq.trimed_fastqc.html        trimmomatic_stdout.log
```

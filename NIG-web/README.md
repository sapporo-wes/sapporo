# NIG-web

- ユーザがブラウザ経由でアクセスし操作を行う Web サーバ
- 後ほど、Nginx などの Web サーバをフロントとしておくが開発段階では Django の内部サーバを用いる
  - Host の 8011 が内部の 8000 に Port Forward されている

## 実行環境

- とりあえず、末竹の MBP の PC 環境

```bash
$ docker --version
Docker version 18.09.0, build 4d60db4

$ docker-compose version
docker-compose version 1.23.2, build 1110ad01
docker-py version: 3.6.0
CPython version: 3.6.6
OpenSSL version: OpenSSL 1.1.0h  27 Mar 2018
```

## 内部で使われているプログラムの Version

```bash
root@657fd187a29a:/opt/NIG-web# python -V
Python 3.7.0

root@c911f1f35876:/opt/NIG-web# python
Python 3.7.0 (default, Oct 16 2018, 07:14:15)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.get_version()
'2.1.4'
```

- bootstrap
  - 4.1.3
- jquery
  - 3.3.1

### pip package の更新方法

```bash
# コンテナ内で行い、再起動する
$ pip install ${package_name}
$ pip freeze > /opt/NIG-web/requirements.txt
```

## 起動方法

```bash
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app bash
```

## Django Start Project Memo

```bash
$ mkdir NIG-web
$ cd NIG-web
$ django-admin.py startproject config .
$ python3 manage.py startapp app
$ mkdir templates
$ mkdir static
$ mkdir static/js
$ mkdir static/css
$ curl -L https://github.com/twbs/bootstrap/releases/download/v4.1.3/bootstrap-4.1.3-dist.zip -o bootstrap-4.1.3-dist.zip
$ unzip bootstrap-4.1.3-dist.zip
$ rm -rf bootstrap-4.1.3-dist.zip
$ mv css/bootstrap.min.css ./static/css/
$ mv js/bootstrap.bundle.min.js ./static/js/
$ rm -rf css
$ rm -rf js
$ curl -L https://code.jquery.com/jquery-3.3.1.slim.min.js -o ./static/js/jquery-3.3.1.slim.min.js
```

# SAPPORO-web

- ユーザがブラウザ経由でアクセスし操作を行う Web サーバ
- 後ほど、Nginx などの Web サーバをフロントとしておくが開発段階では Django の内部サーバを用いる
  - Host の 8011 が内部の 8000 に Port Forward されている
- ユーザがアクセスするフロントエンド Web システム
- ユーザ毎のログイン認証制御あり
- 解析結果データをストアしてユーザに提供 (http ダウンロード)
- 解析パイプライン実行環境ごとに有効なワークフロー (CWL) リストを API Server から取得してユーザに提示する
  - ユーザは自分が実行したい環境とワークフローを意識した上でリクエストする前提
- 解析パイプライン実行時に必要な credential 情報は２種類ある
  - 各データベース(JGA, AGD, TMM) へのアクセス権限
    - config で記述できるとよい（使うデータしだいなので）
  - 解析環境へのアクセス権限 (SAPPORO スパコン, 東北大スパコン)
    - Web Server <-> API Server 間のシステムトークンとして持つ（ユーザは意識しなくてよい）
- 入力データによって解析パイプラインの実行環境は決まる
  - JGA + TMM の組み合わせ → 東北大スパコンで実行
  - AGD + JGA の組み合わせ → SAPPORO スパコンで実行
  - 権限的に不可能な組み合わせが指定された場合はエラーにすべき → 何らか Validation が必要

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
root@657fd187a29a:/opt/SAPPORO-web# python -V
Python 3.7.0

root@c911f1f35876:/opt/SAPPORO-web# python
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
$ pip freeze > /opt/SAPPORO-web/requirements.txt
```

## 起動方法

```bash
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app bash
$ ./migrate.sh
$ ./run_server.sh

# ブラウザで localhost:8011 にアクセス
```

## Django Start Project Memo

```bash
$ mkdir SAPPORO-web
$ cd SAPPORO-web
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

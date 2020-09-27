Title: AWS Lambdaで swftools を使う
Date: 2020-09-27 22:47:09
Modified: 2020-09-27 22:47:09
Category: aws
Tags: aws
Slug: swftools-in-lambda
Summary: AWS Lambdaで swftools を使うためのやったこと

## はじめに

radiko を lambda からダウンロードするときに、 `swfextract` コマンドを AWS Lambda 上で使う必要があったので準備方法をメモしておく。

## 手順

- http://www.swftools.org/download.html

`swftools` にはバイナリの配布がないので lambda向けにビルドする。

#### 1. 作業ディレクトリを作成

```shell
❯ mkdir workspace && cd workspace
❯ mkdir bin
❯ mkdir lib

// lambda用のコンテナを使う
❯ docker run -v "$PWD":/var/task -it lambci/lambda:build-python3.8 bash
```

#### 2. コンテナ内で swftools をビルドする

```shell
$ yum install -y zlib-devel libjpeg-devel giflib-devel freetype-devel gcc gcc-c++
$ curl -O http://www.swftools.org/swftools-0.9.2.tar.gz
$ tar -zxvf swftools-0.9.2.tar.gz
$ cd swftools-0.9.2
$ ./configure
$ make
$ cp ..

// 必要なファイルをコピーする
$ cp /usr/local/bin/swfextract bin/
$ cp /lib64/libgif.so* lib/
$ cp /lib64/libjpeg.so* lib/
$ cp /lib64/libpng.so* lib/
$ cp /lib64/libfreetype.so* lib/
$ cp /lib64/libSM.so* lib/
$ cp /lib64/libICE.so* lib/
$ cp /lib64/libpng15.so* lib/
$ cp /lib64/libxcb.so* lib/
$ cp /lib64/libX11.so* lib/
$ cp /lib64/libXau.so* lib/
$ cp /lib64/libuuid.so* lib/
```

#### 3. Pythonから `swfextract` を使う

少し簡略化してるけど、.swfをダウンロードして `swfextract` を使うまでの処理。

```python
import os
import subprocess

import requests

os.environ['PATH'] = os.environ['PATH'] + ':/var/task/bin'

def download_authkey():
  url = os.environ.get('RADIKO_SWF_URL', '')
  filepath = os.path.join(os.sep, 'tmp', 'player-release.swf')
  authkey_path = os.path.join(os.sep, 'tmp', 'authkey.png')

  with open(filepath, "wb") as f:
    res = requests.get(url)
    f.write(res.content)
  # swfextract /tmp/player-release.swf -b 12 -o /tmp/authkey.png
  subprocess.call(['swfextract', filepath, '-b', '12', '-o', authkey_path])

# Download authkey.png
download_authkey()
```

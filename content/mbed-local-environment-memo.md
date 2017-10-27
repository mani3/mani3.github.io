title: [mbed] mbed のオフライン環境をメモ
Date: 2017-10-26 19:14:17
Modified: 2017-10-26 19:14:17
Category: development
Tags: mbed
Slug: mbed-local-environment-memo
Summary: mbed のローカル環境を準備したときのメモ

mbed のオフラインでビルドする環境を用意したかったので試しました。

基本的にはここにある方法を見て作業しました。

- https://os.mbed.com/users/MACRUM/notebook/mbed-offline-development/

（2017/10/25 時点）

## 環境

- macOS 10.12.6
- Xcode 9.0.1 インストール済み

## GCC_ARM 準備

`brew tap PX4/homebrew-px4` はエラーになってしまったので以下で行けた。

```
$ brew tap PX4/px4
$ brew update
$ brew install gcc-arm-none-eabi
```

## Python 環境

Python 3.6 で `pip install mbed-cli` して、 `mbed import` したが以下のようなエラーが出てしまってうまくいかなかった。

```
$ mbed import https://developer.mbed.org/teams/mbed-os-examples/code/mbed-os-example-blinky
Traceback (most recent call last):
  File "/Users/kazuyashida/anaconda3/bin/mbed", line 7, in <module>
    from mbed.mbed import main
  File "/Users/kazuyashida/anaconda3/lib/python3.6/site-packages/mbed/mbed.py", line 1065
    sorted_scms = sorted(sorted_scms, key=lambda (m, _): not m)
                                                 ^
SyntaxError: invalid syntax
```

普通に [mbed-cli](https://github.com/ARMmbed/mbed-cli) に `It is not compatible with Python 3.` って書いてあった 😭


mbed 用に Anaconda で Python 2.7 の環境を用意した。

```
// Python 2.7 の環境作成
$ conda create -n mbed python=2.7 anaconda

// Python 2.7 の環境に入る
$ source activate mbed

// mbed-cli をインストールする
(mbed) $ pip install mbed-cli

// mbed コマンドが使用できる
(mbed) $ mbed import https://developer.mbed.org/teams/mbed-os-examples/code/mbed-os-example-blinky
```

## mbed os 2 

今回 [mbed HRM1017](https://os.mbed.com/platforms/mbed-HRM1017/) を使っていて、これが mbed os 2 だったので準備する。

### 空のプロジェクトを作成

普通に `mbed new` してしまうと mbed os 5 が落ちてきてしまったので `--create-only` で mbed-os や mbed library をインポートしないようする。

```
(mbed) $ mbed new hello-world --create-only
(mbed) $ cd hello-world
```

[mbed-dev](https://os.mbed.com/users/mbed_official/code/mbed-dev/) をダウンロードしてくる

```
(mbed) $ curl -O https://os.mbed.com/users/mbed_official/code/mbed-dev/archive/af195413fb11.tar.gz
(mbed) $ tar -pxvzf af195413fb11.tar.gz

// なんとなくディレクトリ名を変更しておく
(mbed) $ mv af195413fb11 mbed-dev
``` 

## Hello World を作成

以下のような `main.cpp` を作成する

```
#include "mbed.h"

int main() {
    printf("Hello World!!\r\n");
}
```

```
(mbed) $ ls
af195413fb11.tar.gz main.cpp            mbed-dev            mbed_settings.py
```

## ビルド

```
(mbed) $ mbed detect

[mbed] Detected HRM1017, port /dev/tty.usbmodem1412, mounted /Volumes/MBED
[mbed] Supported toolchains for HRM1017
+--------+-----------+-----------+-----+---------+-----+-------+
| Target | mbed OS 2 | mbed OS 5 | ARM | GCC_ARM | IAR | ARMC6 |
+--------+-----------+-----------+-----+---------+-----+-------+
+--------+-----------+-----------+-----+---------+-----+-------+
Supported targets: 0
```

ビルドする前に `mbed detect` してみたけど何もでない。けれど以下でビルドはできた。

```
(mbed) $ mbed compile -t GCC_ARM -m HRM1017
Building project hello-world (HRM1017, GCC_ARM)

...

Image: ./BUILD/HRM1017/GCC_ARM/hello-world.hex


// ファイルを mbed へコピーする
(mbed) $ cp ./BUILD/HRM1017/GCC_ARM/hello-world.hex /Volumes/MBED/
```

screen 経由で Hello World!! が表示されることを確認してめでたく環境が準備できた 💃

ここからがはじまりだけど、試行錯誤して疲れた

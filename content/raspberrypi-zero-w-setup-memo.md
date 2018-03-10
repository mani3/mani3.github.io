Title: Raspberry Pi Zero W セットアップ メモ 
Date: 2018-03-10 01:02:31
Modified: 2018-03-10 01:02:31
Category: raspberrypi
Tags: raspberry pi 
Slug: raspberrypi-zero-w-setup-memo
Summary: Rasberry Pi Zero Wの設定メモ

###### 1. [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) のダウンロード

###### 2. [Etcher](https://etcher.io/) をインストール

###### 3. Etcher を使って Raspbian を SDカードに書き込む

###### 4. SDカードをマウントして以下のファイルを更新する

```bash
// rootwait のあとに `modules-load=dwc2,g_ether` を追加する
$ vim /Volumes/boot/cmdline.txt

// `dtoverlay=dwc2` を追加する
$ vim /Volumes/boot/config.txt

// ssh というからのファイルを作成
$ touch /Volumes/boot/ssh
```

###### 5. Raspberry Pi に SDカード を指して、USB ケーブルで macOS と Raspberry Pi をつなぐ

###### 6. `ssh pi@raspberrypi.local` で入って色々設定する

```bash
// 言語設定
$ sudo apt-get update
$ sudo apt-get -y install language-pack-ja
$ sudo locale-gen ja_JP.UTF-8
$ sudo localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

// wifi の設定を追加
$ sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
network={
  ssid="xxxx"
  psk="xxxx"
}

// エディタなど
$ curl -o .vimrc https://raw.githubusercontent.com/amix/vimrc/master/vimrcs/basic.vim
$ sudo apt-get install vim tmux

// piユーザのパスワード変更
$  passwd

// 開発ツールなど
$ sudo apt-get install clang cmake ninja-build libpthread-workqueue0 wiringpi 
```

<!-- uuid-dev libicu-dev icu-devtools libbsd-dev libedit-dev libxml2-dev libsqlite3-dev swig libpython-dev libncurses5-dev pkg-config libblocksruntime-dev libcurl4-openssl-dev autoconf libtool systemtap-sdt-dev -->

いろいろいじってから思い出しながら書いたので足りてないものもあるかもしれない。

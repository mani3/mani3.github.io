title: PortAudio を macOS で使う
Date: 2017-11-09 23:06:00
Modified: 2017-11-09 23:06:00
Category: development
Tags: development
Slug: portaudio-build
Summary: Xcode 9.1 で portaudio を導入するまで

最近、サウンドプログラミング系の書籍を読んで、ソースを写経してます。
その中で [PortAudio](http://portaudio.com/) というマルチプラットフォームな Audio 系のライブラリがあったのでビルド手順をメモしておく

### 環境

- Xcode 9.1
- PortAudio v19

あらかじめ `xcode-select` で Xcode 9.1 に設定しておく

```sh
$ sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

### ビルド

```sh
// 最新のソースをダウンロード
$ curl -O http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz

// 解凍
$ tar -pxvzf pa_stable_v190600_20161030.tgz

// portaudio ディレクトリへ
$ cd portaudio

// ビルド
$ ./configure && make

// .a ファイルは i386 も含まれてた
$ file lib/.libs/libportaudio.a
lib/.libs/libportaudio.a: Mach-O universal binary with 2 architectures: [i386:current ar archive random library] [x86_64:current ar archive random library]
lib/.libs/libportaudio.a (for architecture i386):   current ar archive random library
lib/.libs/libportaudio.a (for architecture x86_64): current ar archive random library
```

これで、`lib/.libs/libportaudio.a` ができているので、これと `include/portaudio.h` を Xcode で使う。

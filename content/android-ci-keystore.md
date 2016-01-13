title: KeyStoreの扱い方
Date: 2015-12-16 14:00:00
Modified: 2015-12-16 14:00:00
Category: development
Tags: android
Slug: android-ci-keystore
Summary: AndroidでJenkinsを利用するときのKeyStoreの扱い

## KeyStore

Androidアプリをビルドするときに署名するために必要なKeyStoreファイル．

プライベートなリポジトリであってもKeyStoreファイルを入れとくことに抵抗がある．
かといってJenkinsサーバに個別でKeyStoreを準備するのも面倒だなと思ってやってみた．

## ジョブ

KeyStoreのファイルサイズはそんな大きくないので，Base64にして
ジョブのShell Script上で復号する．

環境: MacOSX 10.10.5

### KeyStoreファイルからbase64に変換

事前にBase64文字列を用意しておく

```
$ cat src.keystore| base64
/u3+7QAAAAIAAAABAA...
```

### base64からKeyStoreに変換

ジョブのShell ScriptでKeyStoreを復号する

```
$ echo '/u3+7QAAAAIAAAABAA...' | base64 -D > dest.keystore
```

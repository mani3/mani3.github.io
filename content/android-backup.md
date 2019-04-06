Title: Android アプリのバックアップ方法
Date: 2019-03-01 23:32:59
Modified: 2019-03-01 23:32:59
Category: android
Tags: android
Slug: android-backup
Summary: Pixel3 XL に機種変更して、Androidアプリのバックアップ方法を試した。

## バックアップするAndroidアプリ

機種変更をする前に Justaway というアプリを使っていたのですが、Pixel3 にもインストールを行おうとしたらすでにストアでの公開は終了していました。。

@justawayfactory/status/1029287452094001152

* Justaway 
    * [https://aska.hatenablog.com/entry/2016/09/07/022034](https://aska.hatenablog.com/entry/2016/09/07/022034)

アプリ本体とアプリ内のデータのバックアップと取って新しいデバイスにインストール＆リストアします。

## adb コマンドを使ってアプリをバックアップ

```sh
// インストールされているアプリを一覧する
❯ adb shell pm list packages
...
package:info.justaway
...

// apk ファイルの場所を確認する
❯ adb shell pm path info.justaway
package:/data/app/info.justaway-2/base.apk

// apkファイルを sdcard にコピーする
❯ adb shell cp /data/app/info.justaway-2/base.apk /sdcard/

// apkファイルをローカルにコピーする
❯ adb pull /sdcard/base.apk ./
/sdcard/base.apk: 1 file pulled. 17.2 MB/s (2969358 bytes in 0.165s)

// デバイスをつなぎかえて新しいデバイスにアプリをインストールする
❯ adb install base.apk
Success
```

## アプリ内のデータをバックアップ

```sh
// アプリ内(info.justawayのみ)のデータのバックアップ
// 以下を実行すると backup.ab というファイルを生成される
❯ adb backup -apk info.justaway
* daemon not running; starting now at tcp:5037
* daemon started successfully
Now unlock your device and confirm the backup operation...
```

↑これを実行するとAndroidデバイス側でパスワードの入力が求められます。
このパスワードはリストアするときに使用します。

```sh
// アプリ内データのリストア
❯ adb restore backup.ab
Now unlock your device and confirm the restore operation.
```

## 参考

* https://9to5google.com/2017/11/04/how-to-backup-restore-android-device-data-android-basics/
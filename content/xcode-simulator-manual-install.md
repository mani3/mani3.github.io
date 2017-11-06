title: [Xcode] アプリをiOSシミュレータにインストールする方法
Date: 2017-11-06 21:53:00
Modified: 2017-11-06 21:53:00
Category: ios
Tags: ios
Slug: xcode-simulator-manual-install
Summary: Xcode 8.3でビルドしたアプリを iPhoneX(Xcode 9) のシミュレータにインストールする方法

AppStoreにあるアプリは `arm64` や `armv7s` のアーキテクチャ用にビルドされているので、iOSのシミュレータ(x86_64)では動かない。
通常 Xcode 上で Simulator 向きにビルドすると指定した iOS のシミュレータが起動して、アプリがインストールされて、アプリが起動する。

今回試したことは Xcode 8.3 でビルドしたアプリを iPhoneX のシミュレータにインストールすることをやってみた。
iPhoneX の実機は手に入れられないけど、すでにリリース済みのアプリが iPhoneX 上でどう見えるか確認したかった。

簡単に言うと `xcrun simctl` で指定したシミュレータにアプリ `.app` をインストールすることができた。

## 準備

- Xcode 8.3
- Xcode 9.1

## 方法

###### 1. Xcode 8.3 でシミュレータ向きでビルドする 

例えば Sunshine というプロジェクトをビルドすると `DerivedData/Sunshine/Build/Products/Debug-iphonesimulator/Sunshine.app` という `.app` のファイルができる。これを Xcode9 のiPhoneXのシミュレータにインストールする。

###### 2. `xcode-select` を指定する

```sh
// xcode-select で現在指定されているXcodeのバージョンを確認する
$ xcode-select -p
/Applications/Xcode.app/Contents/Developer

// もし、Xcode.9.0.1.app とかにしている場合以下のように切り替え出来る
$ sudo xcode-select -s /Applications/Xcode.9.0.1.app/Contents/Developer
```

###### 3. `xcrun simctl list` を実行する。 iPhone X の `UUID` を見つける

```sh
$ xcrun simctl list
== Device Types ==
:
-- iOS 11.0 --
    iPhone 5s (9668B904-7C6B-4294-BF38-BE4BC6098397) (Shutdown)
    iPhone 6 (CA93BEB4-1958-4CE1-A340-F42D601F1D38) (Shutdown)
    iPhone 6 Plus (55F57AC9-9EC1-4ACE-BC79-78AF75F5E820) (Shutdown)
    iPhone 6s (4821B437-3C5C-4C23-A552-FC90E73D251F) (Shutdown)
    iPhone 6s Plus (CB161B2C-C9D1-4AF2-8A53-85E46F26875E) (Shutdown)
    iPhone 7 (76A6BFA8-8642-4BE8-84F1-BA4F3AA5FEDE) (Shutdown)
    iPhone 7 Plus (CC2C49BC-27FA-4D96-94B7-92EDEEA29FB6) (Shutdown)
    iPhone 8 (99F42933-D269-4659-B04C-95EE4A1D15E8) (Shutdown)
    iPhone 8 Plus (7CE5F805-F206-4AA9-8BC3-B04F26C7C3A0) (Shutdown)
    iPhone SE (0B2D4C27-C1FF-4401-82CC-EA1BC37EB75B) (Shutdown)
    iPhone X (E15D50A6-55F5-4903-BF99-494FDBC4984D) (Shutdown)     <--- コレ
:
```

###### 4. `xcrun simctl boot <UUID>` で指定したシミュレータを起動する

```sh
$ xcrun simctl boot E15D50A6-55F5-4903-BF99-494FDBC4984D
```

###### 5. `xcrun simctl install <UUID> xxx.app` でアプリをインストールする

```sh
// Sunshine.app をインストールする例   
$ xcrun simctl install E15D50A6-55F5-4903-BF99-494FDBC4984D DerivedData/Sunshine/Build/Products/Debug-iphonesimulator/Sunshine.app
```

###### 6. `xcrun simctl shutdown <UUID>` で起動したシミュレータをシャットダウンする

```sh
$ xcrun simctl shutdown E15D50A6-55F5-4903-BF99-494FDBC4984D
```

これであとはシミュレータアプリを起動するとインストールされてることが確認できる。

シミュレータアプリ（Simulator.app）起動中だと `xcrun simctl` からシミュレータを起動しようとすると既に起動中だよと怒られるので、 シミュレータアプリは一度閉じてから試したほうがいいです。




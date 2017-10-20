title: [iOS] SensorTag CC2650 をさってみた
Date: 2017-10-18 22:02:13
Modified: 2017-10-18 22:02:13
Category: development
Tags: ios
Slug: ios-sensortag-cc2650
Summary: iOS から SensorTag CC2650 をさわってみたのでメモ

せっかく、SensorTag を借りたので iOS でBLE接続してみたのでメモしておきます。

## SensorTag CC2650

- [SensorTag](http://www.tij.co.jp/tool/jp/cc2650stk)
- [ユーザガイド](http://processors.wiki.ti.com/index.php/CC2650_SensorTag_User%27s_Guide)

## デモ

周辺にある SensorTag を検出して Read できる情報を読んだり、 Configuration の書き込みができるようになってます。

![demo]({attach}images/cc2650.gif)

こちらにソースコードがあります。

- https://github.com/mani3/CC2650

## SensorTag からもらった Data

`Data+CC2650.swift` ところに SensorTag から送られてくる Data を計測値に変換しています。

IR Temperature はこんな感じ

```swift
extension Data {

    /// object temperature
    var object: Float {
        let data = Data(self[0..<2]).to(type: UInt16.self) >> 2
        let temperature = Float(data) * SCALE_LSB
        return temperature
    }

    /// Ambience temperature
    var ambience: Float {
        let data = Data(self[2..<4]).to(type: UInt16.self) >> 2
        let temperature = Float(data) * SCALE_LSB
        return temperature
    }
}
```

あと、加速度・ジャイロ・磁気の値が本当にあっているかはあやしい気がする。。

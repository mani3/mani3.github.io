title: [iOS] Optional型に Extension を生やす
Date: 2017-10-20 21:00:11
Modified: 2017-10-20 21:00:11
Category: development
Tags: swift
Slug: ios-swift-optional-extension
Summary: この前はじめて、Optional型に Extension を生やすことができることを知ったのでメモ

### Optional extension

こんな感じにかけます。

```swift
extension Optional {
    var describing: String {
        return String(describing: self)
    }
}
```

いつも `print` や `NSLog` で Optional型を入れると `Expression implicitly coerced from 'String?' to Any` とか `default value` 入れろとか言われるのでその辺りが簡単になるかなと思います。

### 使い方

![サンプル]({attach}images/swift-optional-extension.png)

👋

title: Swift Stringに半角カナの濁点を入れたときのメモ
Date: 2017-07-11 00:35:26
Modified: 2017-07-11 00:35:26
Category: development
Tags: swift
Slug: ios-swift-string-characters-count
Summary: 半角カナの濁点を入れると String.CharacterView は1文字として扱われるようだ 


半角カナの濁点を入れると `characters` だと濁点を入れた文字が一文字としてカウントされてた。



文字コードは濁点の分もある

```swift
"ﾐ".utf16.count             // 1
"ﾐ".characters.count        // 1

"ｼﾞ".utf16.count            // 1
"ｼﾞ".characters.count       // 2

Array("ﾐ".unicodeScalars)   // [65424]
Array("ﾐ".characters)       // ["ﾐ"]
Array("ｼﾞ".unicodeScalars)  // [65404, 65438]
Array("ｼﾞ".characters)      // ["ｼﾞ"]

// 0xff90=ﾐ
// なんて読むかわからないが ﾐ に濁点がついても 1文字でカウントされた
"\u{ff90}\u{ff9e}"                   // "ﾐﾞ"
"\u{ff90}\u{ff9e}".characters.count  // 1
```


`.range` を使ってみると `characters` ではなく `unicodeScalars` で扱われているようだった。 


```swift
"ｺﾞｺﾞｺﾞｺﾞあ".characters.count      // 5
"ｺﾞｺﾞｺﾞｺﾞあ".utf16.count           // 9
"ｺﾞｺﾞｺﾞｺﾞあ".unicodeScalars.count  // 9
"ｺﾞｺﾞｺﾞｺﾞあ".range(of: "あ")       // lowerBound 8, upperBound 9

"1234あ".characters.count          // 5
"1234あ".utf16.count               // 5
"1234あ".unicodeScalars.count      // 5
"1234あ".range(of: "あ")           // lowerBound 4, upperBound 5
```

半角カナの濁点を使う場合は、`Range` で指定する文字数には気をつけようと思う


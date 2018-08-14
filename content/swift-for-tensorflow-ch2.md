Title: Swift for TensorFlow を使って単純なパーセプトロン
Date: 2018-05-31 23:55:31
Modified: 2018-05-31 23:55:31
Category: swift
Tags: swift tensorflow
Slug: swift-for-tensorflow-ch2
Summary: Swift for TensorFlow を使って、 `AND`, `OR`, `NAND`, `XOR` を実装してみる。

Swift for TensorFlow を使って、 `AND`, `OR`, `NAND`, `XOR` を実装してみる。

[ゼロから作るDeep Learning](https://www.oreilly.co.jp/books/9784873117584/) の第2章のサンプルコードを Swift for TensorFlow で書いてみただけです。

## AND

```swift
func AND(a: [[Double]]) -> [Double] {
    let shape = TensorShape([Int32(a.count), Int32(a[0].count)])
    let x = Tensor(shape: shape, scalars: a.reduce([], +))
    let w = Tensor(shape: shape, repeating: 0.5)
    let b = -0.7
    let y = (x * w).sum(squeezingAxes: 1) + b
    return (y > 0).scalars.map { $0 ? 1.0 : 0.0 }
}

print(AND(a: [[0, 0], [0, 1], [1, 0], [1, 1]])) /// => [0.0, 0.0, 0.0, 1.0]
```

## OR

```swift
func OR(a: [[Double]]) -> [Double] {
    let shape = TensorShape([Int32(a.count), Int32(a[0].count)])
    let x = Tensor(shape: shape, scalars: a.reduce([], +))
    let w = Tensor(shape: shape, repeating: 0.5)
    let b = -0.2
    let y = (x * w).sum(squeezingAxes: 1) + b
    return (y > 0).scalars.map { $0 ? 1.0 : 0.0 }
}

print(OR(a: [[0, 0], [0, 1], [1, 0], [1, 1]])) /// => [0.0, 1.0, 1.0, 1.0]
```

## NAND

```swift
func NAND(a: [[Double]]) -> [Double] {
    let shape = TensorShape([Int32(a.count), Int32(a[0].count)])
    let x = Tensor(shape: shape, scalars: a.reduce([], +))
    let w = Tensor(shape: shape, repeating: -0.5)
    let b = 0.7
    let y = (x * w).sum(squeezingAxes: 1) + b
    return (y > 0).scalars.map { $0 ? 1.0 : 0.0 }
}

print(NAND(a: [[0, 0], [0, 1], [1, 0], [1, 1]])) /// => [1.0, 1.0, 1.0, 0.0]
```

## XOR

```swift
func XOR(a: [[Double]]) -> [Double] {
    let s1 = NAND(a: a)
    let s2 = OR(a: a)
    return AND(a: zip(s1, s2).map { [$0, $1] })
}

print(XOR(a: [[0, 0], [0, 1], [1, 0], [1, 1]])) /// => [0.0, 1.0, 1.0, 0.0]
```

とりあえず出力結果があってたので大丈夫そう。
何か間違ってたらごめんなさい🙇‍

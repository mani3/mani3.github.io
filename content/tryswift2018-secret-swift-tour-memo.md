Title: try! Swift 2018 裏 Swfit Tour メモ 
Date: 2018-03-03 21:13:43
Modified: 2018-03-03 21:13:43
Category: ios
Tags: ios, swift
Slug: tryswift2018-secret-swift-tour-memo
Summary: try! Swift 2018 の 裏Swift Tourを写経してみただけ

裏Swift Tourの内容がおもしろかったのでコードとともにメモしておきます。

## 代入

代入すると返り値があるとは知りませんでした。 `.map` などの高階関数の使い方もなるほどなと思いました。

```swift
var myVariable = 42
let r = (myVariable = 50)
type(of: r) // => (): 空のTuple

struct Obj {
    var myVariable = 50
}
var obj: Obj? = Obj()
obj?.myVariable = 50
type(of: (obj?.myVariable = 50)) // => Optional<()>: Optional の空のTuple

(obj?.myVariable = 50).map { /* 代入が上手くいったときだけ処理する */ }
```

## Optional Chaining

[precedencegroup](https://github.com/apple/swift-evolution/blob/master/proposals/0077-operator-precedence.md)なるものがあるんですね。

```swift
/// オペレータを 💩 にしようと思ったけどエラー↓できなかった
/// error: '💩' is considered to be an identifier, not an operator

precedencegroup FoldedIntoOptionalChaining {
    assignment: true
}
infix operator ⭐: FoldedIntoOptionalChaining
func ⭐ (left: Int, right: Int) -> Int {
    return left + right
}

obj?.myVariable ⭐ 50 // ==> 100
obj = nil
obj?.myVariable ⭐ 50 // ==> nil
```

## クロージャ

```swift
struct SomeClass {
    /// var v: Int!
    
    /// これは nil でもない、Optional型でもない
    lazy var v: Int = { preconditionFailure("Variable '\(#function)' used before being innitialized") }()
    
    /// これらはビルドが通る
    let a: Int = { preconditionFailure() }()
    let b: Void = { fatalError() }()
    let c: Never = { while(true) {} }()
}
```

たまにどうしても `!` つけたくないときがあるのでそのときは使ってみようと思う。

## inout

```swift
func f(_ arg: inout String) {
    arg = "🐣"
    arg = "🐓"
}

var testString = "🥚" {
    didSet {
        print("changed: \(testString)")
    }
}
f(&testString) /// => "🐓" (didSetは一度しか呼ばれない)
```

`didSet` がある場合は、 `inout` にコピーが渡されるため最後の値がコピー元に入るので一度しか呼ばれないらしい。
`didSet` がない場合は、コピーではなく参照を渡しているので `arg = "🐣"` の時点で `testString` に "🐣" が代入される。

Swiftは知らないことばかりだとと痛感させられた。。

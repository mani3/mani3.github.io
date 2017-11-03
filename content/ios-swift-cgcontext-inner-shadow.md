title: [iOS] CoreGraphics で Inner Shadow のExtension
Date: 2017-11-03 21:40:57
Modified: 2017-11-03 21:40:57
Category: ios
Tags: ios
Slug: ios-swift-cgcontext-inner-shadow
Summary: Inner Shadow の CGContext の Extensionを用意した

CGContext には [setShadow(offset:blur:color:)](https://developer.apple.com/documentation/coregraphics/cgcontext/1455205-setshadow) があるのでドロップシャドウを付けることは簡単にできますが、インナーシャドウがそのまま実現できるAPIはなそうです。

## Inner Shadow

- [Inner Shadows in Quartz](https://blog.helftone.com/demystifying-inner-shadows-in-quartz/)

こちらのインナーシャドウの実装の説明が記載されています。
とても理解しやすかったです。これを Swift 用に `CGContext` の Extension として用意した。

```swift
extension CGContext {
    func innserShadow(path: CGPath, color: UIColor, offset: CGSize, blur: CGFloat) {
        saveGState()
        addPath(path)
        clip()
        let opaque = color.withAlphaComponent(1)
        beginTransparencyLayer(auxiliaryInfo: nil)
        setShadow(offset: offset, blur: blur, color: color.cgColor)
        setBlendMode(CGBlendMode.sourceOut)
        setFillColor(opaque.cgColor)
        addPath(path)
        fillPath()
        endTransparencyLayer()
        restoreGState()
    }
}
```    

## 使い方

#### 四角形

```swift
let square = CGRect(x: rect.midX / 2, y: rect.midY / 2, width: rect.midX, height: rect.midY)
context.setFillColor(UIColor.green.cgColor)
context.addRect(square)
let path = context.path!
context.fillPath()
context.innserShadow(path: path, color: UIColor.black, offset: CGSize.zero, blur: 20)
```

![square]({attach}images/cgcontext_square.jpg)


#### 三角形

```swift
var path = CGMutablePath()
path.move(to: CGPoint(x: rect.midX / 2, y: rect.height - rect.midY / 2))
path.addLine(to: CGPoint(x: rect.midX, y: rect.midY / 2))
path.addLine(to: CGPoint(x: rect.width - rect.midX / 2, y: rect.height - rect.midY / 2))
path.addLine(to: CGPoint(x: rect.midX / 2, y: rect.height - rect.midY / 2))
context.setFillColor(UIColor.green.cgColor)
context.addPath(path)
context.fillPath()
context.innserShadow(path: path, color: UIColor.black, offset: CGSize.zero, blur: 20)
```

![square]({attach}images/cgcontext_triangle.jpg)

#### 円

```swift
var path = CGMutablePath()
path.addArc(center: c, radius: r, startAngle: 0, endAngle: CGFloat.pi*2, clockwise: true)
context.addPath(path)
context.setFillColor(UIColor.green.cgColor)
context.fillPath()
context.innserShadow(path: path, color: UIColor.black, offset: CGSize.zero, blur: 10)
```

![square]({attach}images/cgcontext_circle.jpg)


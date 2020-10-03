Title: iOS (Swift) で線画抽出する
Date: 2020-10-03 18:16:51
Modified: 2020-10-03 18:16:51
Category: ios, swift
Tags: ios, swift
Slug: ios-line-extraction
Summary: iOS + Metal Shader Language を使って線画抽出します


## はじめに

Core Image から MSL (Metal Shader Language) をつかって、画像から線画抽出します。

アルゴリズムは、以下のやりかたを参考にしてます。<br>
グレースケールに変換して、3 x 3 の max pooling を行いいわゆる膨張処理を行い、元の画像との差分を取ることで線画にしてます。 
同じ方法をiOSで試してみます。

- [https://www.kaggle.com/wakamezake/convertlinedrawing](https://www.kaggle.com/wakamezake/convertlinedrawing)



## 準備

- Xcode 12.0.1
- `MTL_COMPILER_FLAGS`: `-fcikernel`
- `MTLLINKER_FLAGS`: `-fcikernel`


## Metalファイル

- グレースケール
- 元画像との差分処理
- 3 x 3 の max pooling 処理

この３つを CoreImage のフィルタを作成しておく。

```c
#include <metal_stdlib>
using namespace metal;


#include <CoreImage/CoreImage.h>
extern "C" {
  namespace coreimage {

    half4 grayscale(sample_h s) {
      half y = 0.2126 * s.r + 0.7152 * s.g + 0.0722 * s.b;
      return half4(y, y, y, s.a);
    }
    
    half4 difference(sampler_h s, sampler_h t) {
      half4 sc = s.sample(s.coord());
      half4 tc = t.sample(t.coord());
      
      half r = 1 - abs(sc.r - tc.r);
      half g = 1 - abs(sc.g - tc.g);
      half b = 1 - abs(sc.b - tc.b);
      return half4(r, g, b, sc.a);
    }
    
    /// Max pooling: 3 x 3
    half4 max_pooling(sampler_h s) {
      float2 dc = s.coord();
      
      float w = s.size().x;
      float h = s.size().y;
      
      half v1 = s.sample(dc + float2(-1.0 / w, -1.0 / h)).r;
      half v2 = s.sample(dc + float2( 0.0 / w, -1.0 / h)).r;
      half v3 = s.sample(dc + float2( 1.0 / w, -1.0 / h)).r;
      half v4 = s.sample(dc + float2(-1.0 / w,  0.0 / h)).r;
      half v5 = s.sample(dc + float2( 0.0 / w,  0.0 / h)).r;
      half v6 = s.sample(dc + float2( 1.0 / w,  0.0 / h)).r;
      half v7 = s.sample(dc + float2(-1.0 / w,  1.0 / h)).r;
      half v8 = s.sample(dc + float2( 0.0 / w,  1.0 / h)).r;
      half v9 = s.sample(dc + float2( 1.0 / w,  1.0 / h)).r;
      
      half p1 = fmax3(fmax3(v1, v2, v3), fmax3(v4, v5, v6), fmax3(v7, v8, v9));
      return half4(p1, p1, p1, 1);
    }
  }
}
```

iOS14から、 CoreImage(CIKernel) からだと `group::destination_h` が使えなくなっていた。<br>
メソッド名も CIKernel から呼ぶ際は、 `float4` を返すようにしないと、メソッド名が見つからないエラーが出ます。

- [CIKernel](https://developer.apple.com/documentation/coreimage/cikernel)

## CIImage から呼び出す

CIKernelから作ったフィルタを呼び出すために、extension として記述する。


```swift
import CoreImage

extension CIImage {

  func grayscale(metalLib: Data) -> CIImage? {
    let name = "grayscale"
    guard let kernel = try? CIColorKernel(functionName: name, fromMetalLibraryData: metalLib) else {
      return self
    }
    let image = kernel.apply(extent: extent, roiCallback: { _, r in r }, arguments: [self])
    return image
  }

  func maxPooling(metalLib: Data) -> CIImage? {
    let name = "max_pooling"
    guard let kernel = try? CIKernel(functionName: name, fromMetalLibraryData: metalLib) else {
      return self
    }

    let image = kernel.apply(extent: extent, roiCallback: { _, r in r }, arguments: [self])
    return image
  }

  func difference(metalLib: Data, dilated: CIImage) -> CIImage? {
    let name = "difference"
    guard let kernel = try? CIKernel(functionName: name, fromMetalLibraryData: metalLib) else {
      return self
    }

    let image = kernel.apply(extent: extent, roiCallback: { _, r in r }, arguments: [self, dilated])
    return image
  }
}
```

## 使い方

使うときは、default.metallib ファイルを読み込んで、CIImage に変換して各フィルタ処理を行う。 

```swift
guard let url = Bundle.main.url(forResource: "default", withExtension: "metallib") else {
  fatalError("Not found default.metallib.")
}
guard let data = try? Data(contentsOf: url) else {
  fatalError("The default.metallib can not read as Data.")
}

let image = UIImage(named: name)!
let ciImage = CIImage(image: image)

/// 線画抽出
guard let grayscale = ciImage?.grayscale(metalLib: data),
      let dilated = grayscale.maxPooling(metalLib: data),
      let line = grayscale.difference(metalLib: data, dilated: dilated) else {
  fatalError("Can not convert grayscale or dilated image.")
}
if let cgImage = CIContext().createCGImage(line, from: line.extent) {
  let converted = UIImage(cgImage: cgImage)
}
```

## 実際に処理したときの画像

各フィルタ処理したときの画像を出力してみてみました。
線画抽出は、それなりにできたのでよさそう。OpenCVを入れなくてもCoreImageで行けたので結構よかった。

|元画像|グレースケール|線画抽出|
|:--|:--|:--|
|<img src="{attach}images/line-extraction-lena.png" width=240>|<img src="{attach}images/line-extraction-grayscale.png" width=240>|<img src="{attach}images/line-extraction-line.png" width=240>|

title: DroidKaigi メモ
Date: 2016-02-20 01:16:53
Modified: 2016-02-20 01:16:53
Category: development
Tags: android
Slug: droidkaigi-2016
Summary: DoroidKaigi 2016 メモ

# DroidKaigi

## 1日目

### OSSの動向をとらえた実装方針

`10:00 ~ Keynote`

すごい勢いでライブラリを紹介してた

#### Rearch

- [Github/Trending java](https://github.com/trending/java?since=daily)
- [Android Weekly](http://androidweekly.net/#latest-issue)
- [Android Arsenal](https://android-arsenal.com/)
- [Android Gems](http://www.android-gems.com/)

#### Memo

##### Java8

- [Retrolambda](https://github.com/orfjackal/retrolambda)
- [Lightweight-Stream-API](https://github.com/aNNiMON/Lightweight-Stream-API)
- [ThreeTenABP](https://github.com/JakeWharton/ThreeTenABP)
    - JSR-310

##### Views

- [Support Library Design](http://android-developers.blogspot.jp/2015/05/android-design-support-library.html)
- [Calligraphy](https://github.com/chrisjenx/Calligraphy)
    - Fontを適用できる
- [ViewAnimator](https://github.com/florent37/ViewAnimator)

##### Data Binding

- [Android Data Binding](http://developer.android.com/intl/ja/tools/data-binding/guide.html)

##### Networking

- [Retrofit](http://square.github.io/retrofit/) + [OkHttp](http://square.github.io/okhttp/)

##### Parcelables

- [Paceler](https://github.com/johncarl81/parceler)
- [Icepick](https://github.com/frankiesardo/icepick)

##### Image Loader

- [Glide](https://github.com/bumptech/glide)

#### Effect

- [Blurry](https://github.com/wasabeef/Blurry)

##### DB/ORM

- [Android Orma](https://github.com/gfx/Android-Orma)

##### Debugger

- [Stetho](https://github.com/facebook/stetho)

とりあえず使ってみたいやつだけ

### TV向けAndroid開発Tipsと最新事情

`11:30 ~ #DroidKaigiB`

##### TV向けデバイス

- 試すなら [Android Fire TV Stick](http://www.amazon.co.jp/Amazon-W87CUN-Fire-TV-Stick/dp/B00ZVNYLS8)が一番安くていいかも

##### TIPS

- Leanbackライブラリ(TV用UIパターン)
- オーバスキャン&セーフティエリア考慮(上下27dp，左右48dp)
- 画面サイズはフルHDを想定
- 10ft(3mくらい) 離れてTVを見てることを想定したUI/UXが必要

ゲームアプリとかTV向けにビルドするだけでそのまま動くけど，Android TV自体スペックがそんなに高くないので注意が必要

### Go MobileでAndroidアプリ開発

`13:00 ~ #DroidKaigiC`

##### Androidで動くツール

- `GOOS=linux GOARCH=arm go build` でとりあえず動く
- ただピュアGoのみ
- 端末内にサーバ立てるのが容易

##### Go Moblie

- SDKアプリ (`gomobile bind`)
    - goをライブラリ(aar)として利用できる
- Nativeアプリ (`gomobile build`)
    - goのみでapkファイルが生成される
    - Google Playに申請できない(resが含められない)
    - [Flappy Gopher](https://github.com/golang/mobile/tree/master/example/flappy)

### Advanced Android Espresso

`14:00 ~ #DroidKaigiD`

- https://github.com/chiuki/espresso-samples
- RecyclerViewではonDataが使えない
    - onDataはAdapterViewで使える，RecyclerViewはViewGroupを継承してるので使えない

### How Instant Run Works

`15:10 ~ #DroidKaigiD`

- Dex Sharding(default: 10)というのでdexを分割してる
- Data BindingやKotlinを使っている場合は注意が必要

### Androidの省電力について考える

`15:50 ~ #DroidKaigiB`

##### 歴史

- メーカー，キャリアが努力(省エネアプリとか)
- キャリアとかがガイドラインを出す(知らない。。)
- Android 6.0からOSレベルで対策が入る(Dozeとか)

##### Google

- Fused Location Provider
- Sensor Batching (Android 4.4~)
- Job Scheduler (Android 5.0~)
- Battery Saver (Android 5.0~)

##### Android 6.0 ~

- Doze
    - 対象のアプリのみGCMのHigh priorityにするとDozeを抜ける
    - テストするときは `adb shell dumpsys battery unplug` とか
- App standby
    - ホワイトリスト登録用のダイアログ表示するとか
    - [http://developer.android.com/training/monitoring-device-state/doze-standby.html](http://developer.android.com/training/monitoring-device-state/doze-standby.html)

### 実践Android Studioプラグイン開発

`16:30 ~ #DroidKaigiB`

##### Java6，IntelliJが必要
##### 参考になるリポジトリ

- [intellij-sdk-docs](https://github.com/JetBrains/intellij-sdk-docs)
- [android-parcelable-intellij-plugin](https://github.com/mcharmas/android-parcelable-intellij-plugin)
- [android-drawable-importer-intellij-plugin](https://github.com/winterDroid/android-drawable-importer-intellij-plugin)
- [adb-idea](https://github.com/pbreault/adb-idea)
- [Android Studio code](http://tools.android.com/build)

## 2日目

### Support Libraryのススメ

`10:00 ~ keynote`

- バグがあったら [b.android.com](http://b.android.com)まで(スクリーンショット付で)
- Fragmentはv4の方を使ったほうがいい，designとかのライブラリがv4のFragmentを元にしてる
- CoordinatorLayout.Behaviorを使ってみようっと

### 生まれ変わったUI Automatorを使いこなす
`11:30 ~ #DroidKaigiB`

##### 自動テストツール: Ui Automator2

- ブラックボックステスト向け
- Android Studio対応になった
- Lolipop以上のUI Automatorを使ったほうがいい

##### 使い方

- UiDeviceを初期化する
- findObjectに注意する
- UiSelector/UIObject, BySelector/UIObject2の違いに注意する
- スクロールはfindObjectは使わない、UiScrollableを使う

##### 待ち合わせ

- UiSelector/UiObjectの操作 + 同期メソッドを使う
- BySelector/UiObject2 Until~を一緒に使う

##### Tips

- バックキー: UiDevice#waitを使う
- UI監視 UiWatcher UIが見つからない時にコールされる
- タイムアウト値
|  | UiDevice | UiObject | UiObject2 |
|:--|:--:|:--:|:--:|
| Idle Timeout| o | x | o |
| Selector Timeout | x | o | x |
| Action Acknowledgment Timeout | x | o | x |

- WebView操作できるメソッドはない
    - Appiumがおすすめ

##### 使いどころ

- Espressoと併用がおすすめ
- 基本Espressoで書いて、EspressoできないとこをUiAutomator2を使う
    - システムダイアログを押すとか(Espressoではできない)


### パフォーマンスを追求したアプリを作るには
`13:00 ~ #DroidKaigiB`

#### パフォーマンスの指標になるもの

- 電力消費
- UI
- その他(通信、メモリ、プロセッサ)

#### 電力消費

- 計測は未給電で行う `dumpsys battery unplug` or `set usb 0`
- wifiでADB接続 -> 更新停止 -> USBでADB接続 が良さそう

##### 電流消費量を知るには..

- framework-res.apk
- res/xml/power_profile.xml
- デバイスベンダーの電力消費の申告値が記載されてる(目安)
- 0.1はデフォルト

##### バッテリー消費の可視化ツール

- `dumpsys batterystats`とかで見ることができるけど以下が便利
- [Battery Historian](https://github.com/google/battery-historian)

#### UI

##### 利用者の反応指標

- ユーザがアクションしてから250ms以下で応答すればとりあえずストレスにならない

##### レンダリングの歴史

- GB: CPU使用
- Honeycomb : ハードディスクアクセラレータ
- ICS: ハードディスクアクセラレータ
- JetBean: VSyncによるフレーム最適化

ほぼ60fpsで描画される

##### Jank

間に合わない場合Jankが発生する-> Jankを減らすことが大事

##### Viewレンダリング

- onMeasure，onLayout，onDrawの各段階ごとにHierarcy Viewerで描画時間が閲覧できる
- Drawに最も時間がかかるのが一般的
- Measureが遅い場合大抵レイアウトのネストが原因
- Overdrawを確認する -> Hierarchy ViewerでPSDファイルに出力して確認できる
- dumpsys gfxinfo (GPU プロファイル)

#### その他(通信、メモリ、プロセッサ)

##### 通信の最適化

- AT&T ARO 通信最適化ツール

##### メモリの最適化

- dumpsys meminfo プロセスID指定で見れる
- Heap dump
- Leak Canary

##### CPUの最適化

- dumpsys cpuinfo
- Systrace
- Trepn Powor Profiler (Qualcommプロセッサデバイスのみ．Bluetoothもみれる)

### Advanced Kotlin for Android
`14:00 ~ #DroidKaigiB`

- Swiftぽい，簡単そう

# 資料

- [http://unsolublesugar.com/20160218/134940/](http://unsolublesugar.com/20160218/134940/)
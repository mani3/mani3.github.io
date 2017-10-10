title: DroidKaigi 2017 メモ
Date: 2017-03-10 23:18:58
Modified: 2017-03-10 23:18:58
Category: development
Tags: android
Slug: droidkaigi-2017
Summary: DoroidKaigi 2017 メモ

# DroidKaigi

## 1日目


### 逆引き マテリアル デザイン

`10:40 ~ #DroidKaigi4`

- [スライド](http://yaraki.github.io/slides/droidkaigi2017/)
- CameraViewも作ってる

#### マテリアルデザイン

- ガイドライン
    - Adobe After Efectでつくった動画
    - 絶対従わないといけないものではない
    - 概念の上に自分のUIを作っていく
    - 随時更新されてる [What's New](https://material.io/guidelines/material-design/whats-new.html) で更新内容を確認できる
    - [日本語版のガイドライン](https://material.io/jp/guidelines/)
    - 余談 [Typographyのページ](https://material.io/guidelines/style/typography.html#typography-styles)
        - Jonathan Lee (material design偉い人)
            - 織田信長扱いｗｗ
- マテリアルデザインと言えばアニメーション

#### Components

- FAB
    - 影、アニメーション、ガイドライン通りの動作
    - 右下でなくても良い
    - サポートライブラリではできないのでガイドラインに従ってほしいこと
        - 主要なアクションで使う -> ガイドラインに記載
        - リストの一番下が隠れないようにpaddingいれるとか
    - これは開発者が任意で行うもので、サポートライブラリではどうしようもないので、開発者がガイドラインに従う必要がある 
- Grid Lists
    - `android:foreground="?attr/selectableItemBackground"`
    - タッチフィードバックのないアプリが多い
    - 押せたということがユーザにわかるように
    - Android 6.0以下で使う場合、ForegroundLinearLayout で検索
- [Patterns Launch Screen](https://plus.google.com/+AndroidDevelopers/posts/Z1Wwainpjhd)
    - ブランディング画面を表示
    - コンテンツを表示するのが最優先
    - やりかた
        - style で背景として設定する

#### カスタマイズ

- スタイルとテーマの違いがわかればよい？
- `@style/foobar`、 `?attr/foobar`
- スタイル
    - `styles.xml`
        - `parent` は明示的な継承
        - `parent` を書かない場合、暗黙的な継承
- テーマ
    - `themes.xml` Key-Valueマップ style と同じ
    - テーマ内の属性を参照できる
    - `?attr/actionBarSize` キーで取ってこれる    
- Text Field
    - エラーテキストカラーを変更する場合
    - [TextInputLayout](https://developer.android.com/reference/android/support/design/widget/TextInputLayout.html)
    - `styles.xml` に `TextAppearance.Design.Error` を継承して値を設定する
    - `app.errorTextAppearance` 特殊なスタイル
        - `support/design/res/values/styles.xml` を見る
        - `support/design/res/color/design_error.xml` を見るとテーマから取得してることができる
        - `textColorError` をテーマとしてつかえばよさそう

#### Animation

- View同士を協調して動かす
    - Elevation dp
        - どのコンポーエントがどの高さか書いてある
        - FAB と Snackbar が `8dp` -> 被ってはいけない
        - FAB を CoordinatorLayout をつかえばあってに避けてくれる
    - `app:layout_dodgeInsetEdges` を使えば、 FAB と同じように避けてくれる
    - `app:layout_insetEdge` を使えば、 Snackbar と同じように避けてくれる
    - `app:layout_anchor` , `app:layout_anchor_gravity` , `@id/_bottooom_sheet` に追従して動く
- 状態の変化を動かす
    - Motion
        - 画像が拡大縮小する例
    - Transition - Activityだけではない
    - 19 Kitkat で導入
    - `TransitionManager.beginDelayedTransition` を使えばできる
        - root以下の 今のViewの状態を保存する
        - root以下の propertiyが変更されたことを検知
        - その差分をアニメーションする
    - `ChangeBounds` は位置や大きさを検知・アニメーションする
    - [Choreography](https://material.io/guidelines/motion/choreography.html#) -> こうゆうアニメーションがいいですよ
        - arcに従ってアニメーションする場合: `PathMotion`
        - 複数のアニメーション `TransitionPropagation` 、startDelayで細かく調整
        - この２つはまだ Support library に入ってない



### Android Security 最前線！！

`11:50 ~ #DroidKaigi3`

- Naoki Yano: Yahoo 株式会社
- Nougat は security周りのアップデートがいっぱい

#### using scoped directory access
- Android 6以前
    - 外部ストレージへすべてアクセス許可されてしまう
- 7.0
    - strageVollumeを作成してリクエスト
    - 特定のディレクトリのみアクセス
    - StorageVolume
    - StorageManageer - volumeを取得するもの
    - sv.createAccessIntentでユーザに許可をだす
        - privmaryストレージかどうかで挙動が変わる
            - primaryストレージのときのみ気をつける
    - 許可ダイアログ - OpenExternalDirectoryActivity
    - Target API低くアプリも影響を受ける

#### direct boot

- Android 6以前
    - 端末が暗号化されている場合アンロックが必要
- 7.0
    - アンロック前にアクセスする場合ダイレクトブートモードで動作する
- `android:directBootAware`: 暗号化ストレージに対応
- `BOOT_COMPLETED` (6以下), `LOCKED_BOOT_COMPLETED (7以上) 使用可能の通知ブロードキャストされる     
- Context#createDevieProtectedStorageContext()でアクセス
- 7以上でもBOOT_COMPLETED呼ばれるがunlock後に呼ばれる
- `ApplicationInfo#deviceProtectedDataDir`

#### network security config

- 7.0以上
    - カスタムCA証明書を使うための簡単なAPI
    - デフォルトはユーザが追加したCAは使われない
- `network-security-config`
    - `domain-config`, `trust-anchors`, `certificates` でCAファイルを指定
    - `network-security-config` はマニフェストに追加必要
    - `debug-override` でdebugのときのCAの切り替えも可能
    - `baes-config` もある
- android 7 default
    - base-config - trust-anchors - cert system のみ
    - 6未満と同じにしたい userを追加する
- 設定アプリからCAを入れる必要がなくなった



### Androidリアルタイム通信アプリ作成Tips

`12:40 ~ #DroidKaigi3`

- [スライド](https://speakerdeck.com/srym/android-realtime-library)
- Fumihiko Shinoyama
    - セッション始まる前に、懸垂万能説について語ってた
    - 3つの比較

#### WebSocket

- [rfc](https://tools.ietf.org/html/rfc6455)
- websocket リクエスト HTTPの拡張
- OkHttp 3.5 が websocket サポート
- バイナリをサポート
- `ws://`, `wss://` で OkHttp を初期化するだけ
- socket.ioは roomとかの実装があり、wsはないので実装が必要ブロードキャストも
- server でフックできる
- Radis pub/sub - わりとやり方が確立されてる

#### Firebase Realtime Database
 
- ローカルのデータベースに書き込んで、同期してる
- 同期されたことが通知される
- security rules が定義が簡単にできる
- Android
    - AS Firebase Pluginで簡単
    - google-services.jsonも自動
    - push(): メッセージのユニークIDがつく
- 能動的に取得する場合
- ValueEvent をなんとかする
- タイムスタンプは-1を掛けて逆順にしておく(Tips)
- オフラインサポート
- バイナリのサポートなし
- Server側でフックできない分、定期巡回が必要

#### Realm

- Realm mobile Database
    - getter&setterはmust
    - RealmResult: ライブオブジェクト
    - 変更の通知もある
- Realm object server
    - Developer Edition is Free
    - `RealmRecyclerViewAdapter` を使うと最初に一覧を取得するだけで、データが更新されれば自動でViewに反映される
- Firebaseとは異なり、クエリ・リレーションがあり
- pro版だとサーバ側でフックできる
- Realmがおすすめ



### Data Bindingで開発を気持ちよくしよう

`12:40 ~ #DroidKaigi3`

- [スライド](https://speakerdeck.com/oldergod/the-data-binding-library)

- データとUIを接続してくれる
- XMLもカスタムできる
- dataBinding 有効 build.grade
- DataBindingUtil.setcontentViewを使うだけ
- modelのデータを反映
    - @{} だけ
    - デフォルトのテキスト @{ ?? }
    - @string もそのまま使える
    - @{ showScore.checked ? Voew.Visible :    } viewのIDがそのまま使える
    - app:ImageResourcesが使える
- イベント
    - bootomnavigation
    - @{}
- XMMLでデータを定義する <layout> の中
- UI Update
    - モデルに定義
    - BaseObserveable を付ける
    - notifyPreopertyChangeedを呼ぶだけ
- View -> Model
    - @={} を使うだけ
- 中では
    - zero relection
    - bitwise フラグで冠されてる
    - getなくても書ける
    - get is has は略して書ける
- custom
    - app:imageUrl
    - @BindingAdapterを掛けばOK
    - @{} の中で計算もできる
    - ラムダも使える
- NPさよなら
    - nilが発生しても空文字に解釈される
- syntax highlighting
- AS Tips
    - layout にnamepaseをいれる
    - UIでtoolsで値が入った状態でプレビューできる
- DataBinding最高
- サンプルコード
    - oldergod/DataBindingDemo
    - 資料の手順ごとにブランチが切ってある
- 質問
    - 欠点
    - デバッグに苦労はする（DataBindingのエラーがたくさん出る）
    - BaseObservable
    - BR.match 定数を見つけられない -> ビルドができる
    - 最近は ObservableField を使う
    - Listの増減
    - ObservableListを使ってる


### 解剖Kotlin ~バイトコードを読み解く~

`15:10 ~ #DroidKaigi4`

- トクバイアプリ - Kotlin 100%
- Javaバイトコードをみてkotlinがイメージできれば怖くない
- Kotlin デコンパイルしてくれるPluginがある
- 前半
    - null許容型
    - var name: String? = null ?: nullあり
    - var name: String = "" nullなし
    - str?.length
    - str!!.length
    - 引数もnull許容かどうか明示される
    - text? let { }
    - ?: Javaコードを見るとnullチェックしてるだけ
    - !!: exeption
    - 特にすごいことをやってない
    - 関数型
    - var onClick: (view) -> Unit
    - ラムダ式、関数リテラル
        - Function2)null.
        - バイトコードを読む必要がある
        - singletonを内部で作ってる
    - クロージャ
        - 無名クラスをnewしてるだけ
        - 中に変数がある場合、 IntRefみたいなコンテナが生成されるだけ
    - Java8のやり方とほとんど同じ
    - 拡張関数
    - 対象のクラスの第一引数該当のクラスを指定されるstatic関数
    - ExtensionUK
    - プロパティ
    -
    ```
    ```
    - バッキングフィールド
    - val == let
    - まとめ
    - Kotlinは全然難しいことをしてない
- 設計
    - null
    - text?.let { semitransparent(it) }
    - data binding または kotlin android extension を使う方向
    - null安全の設計を考えられる
    - 拡張関数
    - 静的関数Utils群をちゃんと運用するだけでも・・
- まとめ
    - ボイラープレートコードを隠蔽してくれる


### オフラインファーストなアプリケーション開発

`16:00 ~ #DroidKaigi3`

- @zaki50
- Realm / uPhyca Inc
    - オフラインファースト
    - Webの考え方
    - ブラウザがローカルにストレージを持てるようになってから
        - 以前はcookie、google gear(JS)
    - デスクトップの利用時間はかわらない
    - mobile app の利用時間が増えている
    →オフラインの必要性
    - gmailとか、オフラインでも利用できる
    - サーバ通信
    - object -> json -> sarver object
    - 図がわかりやすそう
    - データベースの課題
    - オフライン用とオンライン用の実装が必要
    - データ同期
    - 結構難しい問題が多い
    - Realm的解決
    - この3つの課題はRealmが解決してくれる
    - Realm Mobile Platform
    - オフライン時の変更衝突を自動解決してくれる
        - デフォルトがかなり賢い（カスタムも可能）
    - 同期以上の使い方もできる
        - サーバ側で validation()
        - アプリはローカルDBに保存するだけ
    - デモ
    - Realm Mobile Database
    - データの買い込みする場合は executeTransactionが必ず必要あり
    - REalmResultを作っただけでは読み込みは行われない
        - フィールドにアクセスしたタイミングで読み込みが発生する
    - 更新/削除: フィールドに値を入れるだけ
    - 変更通知
        - AddChangeListenerがある
        - SQLiteでやろうとしたらEventを関しを書いておく必要がある。。確かに
        - Server からの同期も同じロジックでできる
        - seveerに対してユーザ認証・syncConfigurationは必要
    - デモ
    - 衝突解決(デフォルト)
        - 削除は優先
        - 同じプロパティは編集あとがち
        - リストへの挿入は時間順
        - Operational Transform
    - CAP定理
        - consistency
        - Availabilty
        - partition Tolerance
        - 2つまでしか同時に満たすことができない(2000)
    - 一貫性
        - 同じ結果が見える
    - 寛容性
        - 残った者でなんとかする
        - なにかがなければ動かない
    - 分断耐性
        -
    - 一般的なRDS: 1.2.
    - Apache HBase, MongoDB: 1,3
    - DNSなど Realm Mobile Platform 2, 3
    - 一貫性を保証しない -
        - Eventual Consistency - いつかは一貫したデータになる
        - Strong Eventual Consistency
        - Strongがつくと常に同じ結果になる
    - 難しいことはRMPに任せる
    - Developer Editionは商用で使ってもらっても大丈夫
    - マイグレーションについて
    - 分散の場合、削除・更新はできない。プロパティの追加はマイグレーションされる
    - 削除するものは一定期間は残すとか運用を考えてほしい
    - ローカルのみはご自由に
    - オフラインかどうか通知する方法
    - 現在はない
    - clean architecture?
    - cellerのときwifiのときの通信


- 
### Reverse engineering is not just for hackers!

`17:10 ~ #DroidKaigi5`

- [スライド](https://speakerdeck.com/jonreeve/reverse-engineering-is-not-just-for-hackers)

- Jon Reeve @themighttyjon
    - adb shell pm list packages -f -3
    - aapt
    - in Android SDK
    - aapt dum dadgin my.apk
    - xml, stringsのしてできる
    - The APK
    - META-INF: certificate, signature file hashes to veerify origin adn integrify
    - resources arse compiled res
    - classes dex: Dalvik Executable - JVM
    - lib: native code
    - apktool
    - ibotpeaches.github.io/Apktool
    - rebuild for debug
        - jarsigner -verbose -signed ~
    - androguard
    - python androlyzer.py -s
    - iPython
    - other tools
    - ClassyShark
        - android-classyshark
        - GUI and CLI
        - dex method counts, package stucture, size
        - .dex, .so...
    - radare2
    - Play Store Apps
        - JaDX
        - Show Java
    - Santoku
        - santoku-linux.com/features
    - IDA Pro
    - CodeInspect
    - JEB / JEB2
    - Security
    -
    - goo.gl/Cy96UO


### What's New in RxJava 2.0

`18:00 ~ #DroidKaigi3`

- [スライド](https://speakerdeck.com/hkurokawa/whats-new-in-rxjava-2)
- RxJava2
    - Reactive Streams に対応 - 何かの仕様
    - Java 9 Flow API としての動き
    - 非同期の処理のスタンダード
    - publisher subscriber subscription proessor
    - オペレータには含まれていない(filter)
    - subscriptionを使うとpublisherにどのデータがほしいかリクエストできる
        - requestとcancelがある
    - onnextにnullは返せない
    - pcessor ?
    - backpressure
        - ない場合
        -
        - OutMemoryErrorがお消える
        - ある
    - package rx -> io.~
    - backpressure-aware対応メソッドと非対応メソッドの2種類存在
    - observable
    - flowable (bpあり)
    - Avoid null
    - Reactive Streams 対応メリット
    - Akka, Actorと統合できる
    - Java 9
- Sngle maybe completable
    - 必ず1つ値を返すもの: sibgle
    - 0固化1つか: meybe
    - 0個返す: completable
- performance imprevement
    - BPがなくなったからとか
- RxJava2 以降が必要か？
    - 1は2017まで、2018 Marchまで
    - Sngle maybe completableはわかりやすい
    - RxAndroid、Retrofit、RxBinding 対応済み
    - RxJava2interop
- 移行するときは
    - Read What's different in 2.0を読む
    - どうしてもnullがつらいときはシングルのenumを返すとか
    - Search Structurally
    - nullチェックしている箇所を検索できる
    - map に気をつける
    - RxJava1の便利メソッドを使いたいときはRxJava2Extension使う
- まとめ
    - RxJava2に移行してみたらどうでしょうか。
- hkurokawa: speakerdeck







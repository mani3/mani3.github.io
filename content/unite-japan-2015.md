title: Unite Japan 2015 Memo
Date: 2015-04-16 10:01:34
Modified: 2015-04-16 10:01:34
Category: development
Tags: unity
Slug: unite-japan-2015
Summary:

# Unite Japan 2015 day 1

2015/04/13  ホテル日航東京 1F

## コロプラUnity 5プロジェクト ～白猫プロジェクトにおけるUnity 4からUnity 5への移行事例～

Room2 14:00~

### コロプラ

#### スリングショットブレイブズ？

- Unity のバージョンを上げてしまうと・・
- パブリッシュしているタイトルは強制アップデートをできるだけ行わない運用
- Unityのバージョンをあげると複数AssetBundleを用意しないと聞けない
-- チェックコストが上がる

#### Unity 5移行

- エラーをとってく
    - 小文字のアクセサが大文字になってたりする
- API Updaterで基本的には移行できる
- 仕様が変わってしまったAPIを修正
    - Cloth 頂点単位で移動距離を指定？
    - TextureFormat
    - AnimationStateMachine
    - BB10Player
- うまく動作していない箇所
    - 白猫のタイトルのアニメーションが動かない
        - ルートモーションの仕組みが変更
        - ApplyRootMotionのチェックを外す
    - アウトラインが膨らむ
        - COMPUTE_VIEW_NORMAL
    - CubeMapが反映されない
        - Unity5からTexGenがなくなった
        - VertexShaderでCubeMapのUV計算を行う
    - RenderTextureでカメラ破棄しようとすると一緒になくなる
        - cameraからRenderTextureを外してからcameraをdestroy
    - 厚みのない板にモーションをつけると落ちる
        - OpenGLES3.0とMetalのチェックを外すと治る？
    - DynamicBatchingでiOSが落ちる -> 原因不明
    - CharactorControlの挙動がわかっている
        - SphereCollider -> CapsulColliderに変更
    - LightMapの動的切り替えができない
        - Unity4でたまたまできていたらしい

#### 結局

+ αアニメーションが反映されない
+ IL2CPPでバイナリサイズが減ったら
    - 4.6.4のパッチ(2回)でil2cppのバイナリサイズが削減されてる

上記二つが解決したらUnity5でリリース予定


#### メモ
- iOS 64bitサポートが6月からマストなのでアプリサイズ、Unityのアップデート(4.6.3移行)での確認必要
- [Unity5移行このへんかな](http://blogs.unity3d.com/2014/06/23/unity5-api-changes-automatic-script-updating/)


## Unity ユーザーエクスペリエンスチームの目標とビジョン

Room1 15:00~

- Unityのユーザエクスペリエンスをよくしてますよというお話
- Unity5からのAudioMixerのシンプルにしようとスライダーとか極力減らして、UIテストしたらオーディオエンジニアからは使いにくいとなったらしい
- UnityのUIのテスト実際の様子は見せれないけど下のような感じ
    - [Kids React to old Computer](https://www.youtube.com/watch?v=PF7EpEnglgk)
    - (動画自体はおもしろい)
- Persona Project
    - いろいろなユーザタイプ(Unity歴何年とか)を作成すること
    - \#unityux DeveloperとしてUnity開発の様子を写真をあげてほしい


 ## スケルトンを用いた2Dキャラクターアニメーション開発 虎の巻

Room1 17:00~

- スプライトシート、スプライトエディタ、ポビットポイントを使用したデモ
    - https://bitbucket.org/veli/2danimationtools

## Unity for New ニンテンドー3DS

- Unity 5ベース
- New ニンテンドー3DSの登録ディベロッパーは利用可能
- 既存のNintendo3DSは厳しい（アプリによっては動作するけど
- 2015年夏にNintendoにβ版提出
- New 3DSはスペックはミドルレンジのスマートフォン(Nexus 5)くらい？
- New 3DSはil2cppのみ

#### ねじ巻きナイト2

- New 3DS版に移行中
- 3DSの仕様
    - ピクセルシェーダは固定（vertexシェーダは書ける）
    - 画面が3つある(上下画面と視差用の画面)
    - タッチ画面
    - 400x240
- 3画面とも60fps、CPU使用率59%
- \#if (UNITY_IOS || UNITY_N3DS)
- デモ

#### 今後

- 3DSはフレームバッファを再利用できる
    - Screen.setReactive(false) or Screen.SetDirty()みたいなものをUnityで用意するか
- 3Dボリュームの扱い


## Unity 5オーディオ新機能の真髄

Room1 19:00~

- AudioClipの改善
- AudioSourceの改善
- Audio Profiler, Audio Mixer追加
- AudioMixer上でホワイトノイズ作れて、組み合わせて風の音や金属音を作っていたのでUnity上でやれることが多くなった印象
- Native Audio Plugin SDK + example project
  - https://bitbucket.org/Unity-Technologies/nativeaudioplugins
- Linear / non-linear music example project
  - https://bitbucket.org/Unity-Technologies/audiodemos
- Presentation
  - http://files.unity3d.com/janm/UniteAsia2015.pdf


# Unite Japan 2015 day 2

2015/04/14  ホテル日航東京 1F

## Unity パフォーマンス・チューニング

Room1 10:30~

- Profilierを使う
    - CPU, Memory使用率など
    - 各オブジェクトのメモリサイズまで確認できる
    - オブジェクト間の参照も確認できる
- GC
    - classをstructに置き換えるとGCする時間が短縮される
- onGUIは使わない
- MonoBehaviorクラスは遅い-> 必要ないところは使わない
- transformもたくさん使うと思い

###まとめ
- オブジェクトの再利用を検討する
- Profilerを使ってゲーム動作を見て最適な方法を選択する


## Unityプロジェクトをひも解き把握するには

- プロジェクトの中身を把握するにはどうすれば良いかという話
- プロジェクト->シーン->オブジェクト->コンポーネント
- 実行時にシーンが持つコンポーネントを知る
- オブジェクトの役割と参照関係を知る
- オブジェクトが作られる条件を知る
- コンポーネントの動くタイミングを知る
- コンポーネントの接続方法を知る
- オブジェクトの動きを把握するとシーンの構造が分かる
- 参照関係を閲覧できるEditor拡張のデモを行っていたが未公開

## Unity GUI 開発テクニック指南

14:00~

- Unity Frame debugerを使えばドローコールの回数とか把握できる
- Batching

- 各コンポーネントにキャンバスをつける
- Unity Sprite Packerを使う
- 動かないオブジェクトはPexel Parfect指定

## 観客の皆さんも参加！Unityロードマップ・オープンディスカッション！

15:00~

- バグ修正が遅い -> 週一回パッチリリースを行うようにした
- 5.1 6月~
- 5.2 9月~ β
    - il2cpp for Android
- 5.2以降はリリースサイクルを短くできたものをリリースするようにする
- Booはなくなる (Unity5 からdeprecated)

## Unity新ネットワークシステムの未来

17:00~

- Raknet 5.1まで
- Multiplay Foundationを5.1から使って欲しい
    - UDPベース
    - Low Level APIはC++
    - High Level APIはC#


## Unityで音を制す

18:00~

- ADX2
- Sofdec2
- ファイルマジックPro

- CRI ADXの導入事例
- 試用は無料
- 初期費 35万円 + リリース初月 40万円 月額売上2700万以下なら翌月無料

## Unityを利用したスマートフォン向けゲームアプリ開発へのアプローチ方法

19:00~

- SummerTimeStudioの開発事例

- 問題点疑問点は即解決
- 話した内容はメモで共有
- コアメンバー少数決めて意思決定を早く

- STFramework
- Android, iOSアプリ内課金共通化
- ローカライズ
- デバッグメニューの共通化
- 独自のフレームワークを作るとUnityがアップデートされたときに対応必要


# 感想

- 講演自体はBlackセッションでも万人向け？の印象
- コアな質問等はUnity Japanのブースまたはワークショップでフォローアップしている感じ
- 公開された資料を見たほうがわかりいいかも
    - [資料](http://japan.unity3d.com/unite/unite2015/schedule)



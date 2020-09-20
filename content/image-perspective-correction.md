Title: 台形補正するツールを作る
Date: 2020-09-20 22:56:44
Modified: 2020-09-20 22:56:44
Category: vue.js typescript
Tags: vue.js typescript
Slug: image-perspective-correction-vue
Summary: 特定の画像から台形補正を行い、補正した画像をダウンロードできるようにした。

## はじめに

特定の画像から台形補正を行い、補正した画像をダウンロードできるようにした。
もともとの目的は、切り出した画像からテキスト検出用のデータセットを作るために、ある写真から矩形のカードや看板など切り出すということがやりたかった。<br>
はじめは、ちまちま GIMP で切り出し＆台形補正していたがもう少し簡単にできるようにしたかったので、ツールを作ったという感じである。


## できたもの

- Perspective Correction
    - [https://mani3.github.io/perspective-correction/](https://mani3.github.io/perspective-correction/)

<img src="{attach}images/image-perspective.jpg" width=720>

※ 使っている画像は、[フリー写真素材ぱくたそ](https://www.pakutaso.com/20110741198post-394.html)の画像です。

画像を読み込んで、切り出したい枠をドラッグできます。<br>
切り出した画像を台形補正して、JPG形式でダウンロードできるようになってます。
Vue.jsのコンポーネントももう少し分けてきれいに作りたい気持ちだったけど、形にはなったのでよしとする。

- リポジトリ
    - https://github.com/mani3/image-perspective-correction

### ツール

- [Vue.js](https://vuejs.org/v2/guide/)
- [Typescript](https://www.typescriptlang.org/)
- [glfx.js](http://evanw.github.io/glfx.js/demo/)


## 参考

ほとんど、こちらの記事を参考につくりました🙇‍♀️

- https://memo.sugyan.com/entry/2018/09/03/212712


title: Setup PyCharm
Date: 2015-12-05 01:16:53
Modified: 2015-12-05 01:16:53
Category: development
Tags: python
Slug: setup-pycharm
Summary: PyCharmのセットアップ

# Setup PyCharm

いつもだいたい忘れるのでメモ

## Install PyCharm

環境：MacOSX 10.10 Yotemise

### Homebrew からインストール

```
$ brew update
$ brew search pycharm
Caskroom/cask/pycharm-ce  Caskroom/cask/pycharm-edu  Caskroom/cask/pycharm
$ brew cask install pycharm
```

`pycharm-ce` はCommunity Editionで、`pycharm`がProfessional Editionらしい

### カラーテーマ

デフォルトでいくつかテーマが存在するが、
いつもTomorrow Nightにお世話になっているので探したらあった。

- [Tomorrow Night](http://color-themes.com/?view=theme&id=563a1a6a80b4acf11273ae64)

File -> Import settings..からダウンロードした Tomorrow Night.jar を開くとカラーテーマを設定できた

### フォント

いつも [Ricty Diminished](https://github.com/yascentur/RictyDiminished) にお世話になっているので設定する

1. Preferences から Editor -> Colors & Fonts -> Font を開く
2. Primay font から Ricty Diminished を選択、Sizeを18にしておく

### Tool Buttons

左端のバーがないと心細いので表示する

- View -> Tool Buttons にチェックを入れる

### virtualenv

いつもターミナルから準備してたけどIDEからやる

1. Preferences を開いて Project: <project name> -> Project Interpreterを開く
2. 歯車のアイコンをクリックして、Create virtualenvを選択する
3. Name: Location: を埋めて作成
4. 仮想環境ができるとインストールされているpackage一覧が表示される
5. 「+」ボタンからパッケージを検索してインストールできるようになる

#### 参考
- [Creating Virtual Enviroment](https://www.jetbrains.com/pycharm/help/creating-virtual-environment.html)


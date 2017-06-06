Jupyter を使ってみる
=====================================

:date: 2017-02-06 23:30:34
:modified: 2017-02-06 23:30:34
:category: development
:tags: jupyter
:slug: hello-jupyter
:summary: Deep Learningを学ぶ前にJupyterをつかってみる


UdacityのDeep Leaningのやつをはじめて，Jupyterというのがおもしろいなと思ってメモしておく

-  ``Jupyter`` : http://jupyter.org/



事前にAnacondaをインストールしておく

-  https://www.continuum.io/downloads

1. 環境をつくる

    .. code-block:: sh

        // 環境名はなんでもいい
        $ conda create --name jupyter python=3

        // 環境に入る
        $ source activate jupyter

2. 必要なパッケージをインストールする

    .. code-block:: sh

        (jupyter)$ conda install numpy matplotlib pandas jupyter notebook 

3. 実行

    .. code-block:: sh

        (jupyter)$ jupyter notebook 

実行すると ``localhost:8888`` でブラウザが起動する。 「File → New Notebook」 で新規にノートが開くのでそこに markdown や pythonのコードを書くことができる。 実行は ``Shift + Enter`` で行える。


4. こんな感じ

    .. image:: {attach}images/hello-jupyter.png
        :alt: magicprefs
        :width: 70%
        :align: center


``.ipynb`` はJSON形式なのでやさしい。
出力はHTMLやmarkdown、reSTなど，reSTで書き出すときは ``pandoc`` のインストールが必要だった．


さわってみて結構便利だったので，python を試行錯誤しながら書くのにはちょうどいいかもしれない。


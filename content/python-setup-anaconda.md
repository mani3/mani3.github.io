Title: Anaconda のセットアップ
Date: 2018-03-28 23:58:14
Modified: 2018-03-28 23:58:14
Category: python
Tags: python dlib 
Slug: python-setup-anaconda
Summary: dlibの環境を用意したかったのでAnaconda のセットアップ


環境: macOS 10.13.3

## Install Anaconda

```bash
$ brew update


// conda で検索したらいくつか出てきた
$ brew cask search conda
==> Partial Matches
anaconda     anaconda2     miniconda    miniconda2


// anaconda を見るとそれぽいのでインストールする
$ brew cask info anaconda
anaconda: 5.1.0
https://www.anaconda.com/what-is-anaconda/
Not installed
From: https://github.com/caskroom/homebrew-cask/blob/master/Casks/anaconda.rb
==> Name
Continuum Analytics Anaconda
==> Artifacts
Anaconda3-5.1.0-MacOSX-x86_64.sh (Installer)
==> Caveats
To use anaconda, you may need to add the /usr/local/anaconda3/bin directory
to your PATH environment variable, eg (for bash shell):

  export PATH=/usr/local/anaconda3/bin:"$PATH"

Cask anaconda installs files under /usr/local. The presence of such
files can cause warnings when running "brew doctor", which is considered
to be a bug in Homebrew-Cask.


// インストール
$ brew cask install anaconda


// .bash_profile などに追記する
$ echo 'export PATH=/usr/local/anaconda3/bin:"$PATH"' >> ~/.bash_profile
$ source ~/.bash_profile


// conda が使えるか確認
$ conda list
```

## dlib 環境準備

```bash
// homebrew からインストールしたせいか最新ではなかったので更新しておく
$ conda update -n base conda


// conda で環境を作成
$ conda create --name dlib-example python=3


// 作成した環境に入る
$ source activate dlib-example


// 共通で使いそうなライブラリを入れておく
(dlib-example) $ conda install numpy matplotlib pandas jupyter notebook


// dlib と OpenCV を pip からインストールする
(dlib-example) $ pip install dlib numpy opencv-python


// import できることを確認する
(dlib-example) ❯ python
Python 3.6.4 |Anaconda, Inc.| (default, Mar 12 2018, 20:05:31)
...
>>> import dlib
>>>
```

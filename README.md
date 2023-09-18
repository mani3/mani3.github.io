```
/// pelican 用の環境
$ pyenv versions
  system
* 3.10.6

/// 必要なものをインストール
$ pip install pelican Markdown typogrify ghp-import pelican_advance_embed_tweet pelican-render-math

// MathJaxのためにPelicanのプラグインを取ってくる
$ git clone --recursive https://github.com/getpelican/pelican-plugins
```

```
/// ローカルでHTMLを確認
$ make clean html && make serve

/// gh-pages ブランチを更新
$ ghp-import output

/// リポジトリに push する
$ git push -f git@github.com:mani3/mani3.github.io.git gh-pages:master
```

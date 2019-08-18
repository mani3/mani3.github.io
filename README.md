

```
/// pelican 用の環境
$ pyenv versions
  system
* 3.6.4

/// 必要なものをインストール
$ pip install pelican Markdown typogrify ghp-import pelican_advance_embed_tweet
```

```
/// ローカルでHTMLを確認
$ make clean html && make serve

/// gh-pages ブランチを更新 
$ ghp-import output

/// リポジトリに push する    
$ git push -f git@github.com:mani3/mani3.github.io.git  gh-pages:master
```

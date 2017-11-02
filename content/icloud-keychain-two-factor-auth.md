title: [iOS] iCloud のキーチェインを利用できなかった
Date: 2017-10-29 22:18:25
Modified: 2017-10-29 22:18:25
Category: ios
Tags: ios
Slug: icloud-keychain-two-factor-auth
Summary: macOS High Sierra で iCloud のキーチェインの有効ができなかった。


macOS High Sierraから、はじめて iCloud キーチェインを使おうとしたけど、iCloud Secrity Code が入力できなくて利用できなかった。

`Forget security code` からリセットしても、Security Code の登録画面はでてこないし意味がわからなかった。

結局、以下を見て、二段階認証を設定したらうまくいった 🎉

- https://support.apple.com/en-us/HT202755

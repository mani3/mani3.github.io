Title: Pocket の代わりに Obsidian を使い始めた。
Date: 2025-06-14 14:32:04
Modified: 2025-06-14 14:32:04
Category: diary
Tags: diary, obsidian
Slug: obsidian-instead-of-pocket
Summary: Pocket 終了に伴い、Obsidian Web Clipper を使って Web 記事を保存・要約・同期する

## はじめに

Web クリップ用途で Pocket を使っていましたが、 [Pocket がサービス終了する](https://support.mozilla.org/ja/kb/Future-of-pocket) ことになったため、代わりに [Obsidian Web Clipper](https://obsidian.md/clipper) を使い始めました。

この記事では、その際の設定や使い方についてまとめておきます。Pocket からの移行については対象外で、 [こちらの記事](https://www.wantedly.com/companies/wantedly/post_articles/978503) が参考になります。

## Obsidian Web Clipper の設定

Obsidian Web Clipper は、Web 記事やメタデータを Markdown 形式で Obsidian の Vault に保存するための [ブラウザ拡張機能](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf) です。保存だけでなく、 `.md` ファイルのダウンロードも可能です。

公式ドキュメントにはさまざまな機能が紹介されていますが、テンプレートとインタープリターを使うことで保存内容をカスタマイズできます。

- https://help.obsidian.md/web-clipper

### テンプレート設定内容

テンプレートは、クリップ時にプロパティや Markdown の内容をカスタマイズするためのものです。

以下のようなプロパティを設定してます。

#### ノート名:

`{{date|date:"YYYY-MM-DD"}}_{{title}}`

#### プロパティ:

| プロパティ | 値 |
| --- | --- |
| title | `{{title}}` |
| source | `{{url}}` |
| author | `{{author\|split:", "\|wikilink\|join}}` |
| published | `{{published}}` |
| created | `{{date}}` |
| description | `{{description}}` |
| tags | `webclip, unread` |
| word | `{{words}}` |
| coverImageUrl | `{{image}}` |

#### ノートの内容:

`{{content}}`

### インタープリター設定内容

インタープリターを使うと、クリップする際に Markdown の内容をさらにカスタマイズできます。  
LLM の外部プロバイダを設定すると、記事の要約やキーワード抽出も可能です。

私の場合、英語の記事をクリップする際に要点を把握するため、インタープリターを設定しています。  
すべての記事を要約すると API の制限に引っかかるため、要約用テンプレートと非要約テンプレートを使い分けています。  
以下は、Gemini API を使って要約するテンプレートの一例です。

- ノートの内容:

```text
{{"以下の記事を日本語で要約してください。出力形式はMarkdownで、見出し2（## 要約）、見出し3（### 主なポイント・### コメント）を使い、本文は2レベルの箇条書きで記述してください。主なポイントでは要点を3～5個程度、簡潔にまとめてください。コメントでは重要な点や興味深い点を1～2文で述べてください。"}}

---

{{content}}
```

## Obsidian の同期

他の端末とクリップ内容を同期するには、Obsidian Sync や iCloud などの同期サービスが必要です。
私は現在、Google Drive を使って同期しています。

Android では、特定フォルダを Obsidian の Vault として設定し、DriveSync を使って Google Drive と同期しています（Google Drive アプリ単体では不可）。

また、Obsidian Web Clipper の設定は JSON 形式でエクスポートできるため、そのファイルも共有・同期して他の端末でも同じ設定を使っています。

## Android 版 Obsidian Web Clipper の設定

Android 版の Chrome では Obsidian Web Clipper 拡張機能が使えません。Obsidian アプリ自体にも Web クリップ機能は見当たりません。

そのため、Android では Firefox ブラウザに Obsidian Web Clipper 拡張をインストールし、Obsidian アプリと連携しています。

## 参考

* [Interpret web pages](https://help.obsidian.md/web-clipper/interpreter)
* [Variables](https://help.obsidian.md/web-clipper/variables)

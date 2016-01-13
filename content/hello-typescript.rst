==========================================
Hello TypeScript
==========================================

:title: Hello TypeScript
:date: 2015-10-21 00:00:14
:modified: 2015-10-21 00:00:14
:category: development
:tags: typescript
:slug: hello-typescript
:summary: TypeScriptのことはじめ


開発環境準備
----------------------------

- `TypeScript <http://www.typescriptlang.org/#Download>`_

.. code-block:: sh

    $ npm -v
    1.4.28
    $ npm install -g typescript


エディタ
----------------------------

- `Visual Studio Code <https://code.visualstudio.com/>`_


Visual Studio Code
----------------------------

Install
""""""""""""""""""""""""""""

Homebrewからインストールできた．


.. code-block:: sh

    $ brew cask update
    $ brew cask install visual-studio-code

User Settings
""""""""""""""""""""""""""""

- Visual Studio Codeを開く

.. code-block:: sh

    $ open ~/Applications/Visual\ Studio\ Code.app

- `⌘,` でユーザ設定が開かれる
- `settings.json` に以下を記述する

.. code-block:: json

    {
      "editor.fontFamily": "Ricty Diminished",
      "editor.fontSize": 16,
      "editor.insertSpaces": true
    }


Hello World
""""""""""""""""""""""""""""

1. 適当な場所に `HelloWorld` ディレクトリを作る
2. Visual Studio Codeから `HelloWorld` ディレクトリを開く
3. `⇧⌘P` を開いて「New Files」とタイプしてファイルを作成する(または`⌘N`)

    .. image:: {attach}images/visual-studio-code-command.png
        :alt: magicprefs
        :width: 70%
        :align: center

4. TypeScriptの [HelloWorld](http://www.typescriptlang.org/Samples#HelloWorld)のコードを貼り付ける

    .. code-block:: typescript

        class Greeter {
            constructor(public greeting: string) {
            }
            greet() {
                return "<h1>" + this.greeting + "</h1>";
            }
        }
        var greeter = new Greeter("Hello, world!");
        document.body.innerHTML = greeter.greet();

5. `⌘N` から `tsconfig.json` を作成する

    .. code-block:: json

        {
          "compilerOptions": {
            "sourceMap": true
          }
        }

6. `⇧⌘P` を開いて「Configure Task Runner」とタイプして `Enter` ． `.vscode` ディレクトリの下に `tasks.json` されて以下のように記述されてる

    .. code-block:: json

        {
          "version": "0.1.0",
          "command": "tsc",
          "isShellCommand": true,
          "showOutput": "silent",
          "args": ["HelloWorld.ts"],
          "problemMatcher": "$tsc"
        }

7. これで `⇧⌘B` するとコンパイルされて `HelloWorld.js` が生成される
8. `⌘N` から `HelloWorld.html` を作成して開くと *Hello, World!* が表示される

    .. code-block:: html

        <!DOCTYPE html>
        <html>
          <head><title> TypeScript Greeter </title></head>
          <body>
            <script src='HelloWorld.js'></script>
          </body>
        </html>

参考
========================

- `Visual Studio Code - TypeScript <https://code.visualstudio.com/docs/languages/typescript>`_


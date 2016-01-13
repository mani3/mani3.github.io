title: Node.js - Environment Setup
Date: 2015-10-19 00:01:28
Modified: 2015-10-19 00:01:28
Category: development
Tags: nodejs
Slug: node-env
Summary: Node.jsの開発環境セットアップ

# Node.js - Environment Setup

## Install nvm

環境：MacOSX 10.10 Yotemise

1. *Homebrew* からインストール

    ```
$ brew install nvm
    ```

2. *.nvm* ディレクトリ作成

    ```
$ mkdir ~/.nvm
    ```

3. ~/.zshrc に追加

    ```
    export NVM_DIR=~/.nvm
    source $(brew --prefix nvm)/nvm.sh 
    ```

## Install Node.js 

```
$ nvm install v4.2.1
$ node -v
v4.2.1
$ npm -v
2.14.7
```

---


*nvm* を使ってバージョン切り替えできるが，
*Python* でいうところの *virtualenv* みたいな感じで使いたいので，
[*nodeenv*](https://github.com/ekalinin/nodeenv) を試しに使ってみる

## Install nodeenv

いつものような感じで，Python の仮想環境を準備する．

- python-env.sh

```
#! /usr/bin/env sh
#
# Setup virtualenv

if [ $# -ne 1 ]; then
  command=`basename $0`
  echo "Usage: ${command} <enviroment name>" 1>&2
  exit 1
fi

ENV_NAME=$1
VIRTUALENV="virtualenv-1.10.1"

# Download ez_setup.py
curl -O https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py

# Download virtualenv
curl -O https://pypi.python.org/packages/source/v/virtualenv/${VIRTUALENV}.tar.gz
tar xvfz ${VIRTUALENV}.tar.gz
cp ${VIRTUALENV}/virtualenv.py virtualenv.py
rm -rf ${VIRTUALENV} ${VIRTUALENV}.tar.gz

# Setup virtualenv
python virtualenv.py ${ENV_NAME}
${ENV_NAME}/bin/python ez_setup.py
${ENV_NAME}/bin/easy_install pip

${ENV_NAME}/bin/pip install  nodeenv

# Cleanup
rm ez_setup.py* virtualenv.py* setuptools*.zip

echo "You can use virtualenv by typing \"source ${ENV_NAME}/bin/activate\"."
echo "Disable virtuallenv \"deactivate\"."
```



```
// バージョン
$ python --version
2.7.9

// Python 仮想環境を準備
$ ./python-env.sh env
$ source env/bin/activate

// Nodeの新しい仮想環境を作る
// 最新バージョンのNode.js がインストールされます
(env)$ nodeenv nodeenv
 * Install node (4.2.1)... done.
(env)$ source nodeenv/bin/active

// node のバージョン
(nodeenv)(env)$ node -v
v4.2.1
(nodeenv)(env)[node-env] npm -v 
2.14.7
```

おもしろいのは *nodeenv* で *requirements.txt* ファイルを作ることができる

```
// 仮想環境内にインストールされる
(nodeenv)(env)$ npm install tsc tsd -g

// requirements.txt を作成する
(nodeenv)(env)$ freeze requirements.txt
(nodeenv)(env)[node-env] cat requirements.txt 
tsc@1.20150623.0
tsd@0.6.5
```

使うときは *nodeenv* で仮想環境を作るときに指定する

```
(nodeenv)(env)$ nodeenv --node=0.12.7 --requirements=requirements.txt nodeenv-0.12
 * Install node (0.12.7)... done.
 * Install node.js packages ... done.
```

でも， *npm* は *packages.json* で管理するべきだと思うので *requirements.txt* は使わないかな．．
これで *TypeScript* 使ってこうかな．



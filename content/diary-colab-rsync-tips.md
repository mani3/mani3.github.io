Title: Google Colab 上で役立つ小ネタ
Date: 2026-06-01 21:55:09
Modified: 2026-06-01 21:55:09
Category: diary
Tags: diary
Slug: colab-tips
Summary: Google Colab 上で実行している際のあったら便利なコマンド

## はじめに

最近、 Google Colab を使って強化学習を試しています。
Colab を使う中でちょっと便利なコマンドを備忘録として残しておきます。

## GPU の使用率の確認

```shell
/content# nvidia-smi dmon -s u -d 1
# gpu     sm    mem    enc    dec    jpg    ofa 
# Idx      %      %      %      %      %      % 
    0     85     70      0      0      0      0 
    0     87     69      0      0      0      0 
    0     87     70      0      0      0      0 
    0     85     70      0      0      0      0 
```

こんな感じで、GPU使用率を表示してくれる。

各列の意味はこんな感じ:

- **sm**: 計算コア(SM)の使用率。いわゆる「GPU 使用率」はこれ。高いほど GPU がしっかり働いている。
- **mem**: メモリの読み書き(帯域)がどれだけ使われているか。 VRAM の使用量ではないことに注意。「メモリにアクセスしている時間の割合」を表す。
- **enc**: 動画エンコード専用ユニット(NVENC)の使用率。機械学習ではまず使わないので、たいてい 0。


## 間違って終了のセルまで実行してしまった場合

学習のセルを実行したあと、以下の「ランタイムを停止するセル」まで実行してしまうことがある。

```python
from google.colab import runtime

runtime.unassign()
```

`runtime.unassign()` を実行するとランタイムが切り離され、`/content` 以下に作ったファイルはすべて消えてしまう。Drive にマウントした領域は無事だけど、ランタイム上で生成しただけの成果物(チェックポイントなど)は道連れになる。

これを防ぐには、ターミナルで成果物フォルダを監視 & 同期しておくと少し救われる。

```shell
# 事前に inotifywait をインストールする
apt install -y inotify-tools

while inotifywait -r -e close_write "/content/artifacts"; do rsync -a "/content/artifacts" "/content/drive/MyDrive/Colab Notebooks/artifacts/"; done
```

やっていることはシンプルで、

- `inotifywait`: ファイルの変更を監視するツール(`inotify-tools` に含まれる)
- `while ...; do ...; done`: `/content/artifacts` 内でファイルの書き込みが終わるたびに、`rsync` で Drive にコピーする、を繰り返す

つまり「ファイルが更新されるたびに自動で Drive へバックアップ」される。ランタイムが落ちても、直前まで同期済みの成果物は Drive に残る。

ただし、完璧ではなく、同期前に落ちた分や書き込み途中のファイルは取りこぼすので、あくまで保険くらいの気持ちで。



## データセットを早くコピーしたい場合

Drive をマウントしたまま学習中に毎回ファイルを読むと、Drive 越しのアクセスは遅くてボトルネックになりがち。先に `/content`（ローカル）へコピーしておくと、その後の読み込みがぐっと速くなる。

ただ、大量のファイルを 1 個ずつコピーすると、Drive は 1 ファイルあたりの待ち時間が大きいぶん時間がかかる。そこで複数の `cp` を並列で走らせ、待ち時間を重ねて短縮する。

```shell
#!/usr/bin/env bash
# データセットを Drive から /content にコピーする（冪等）。
# ファイル/ディレクトリが既に存在する場合はスキップする。
set -euo pipefail

DRIVE_DATASETS="${1:-/content/drive/MyDrive/Colab Notebooks/datasets}"
DEST="${2:-/content}"

copy_files_parallel() {
  local src="$1" dst="$2"
  mkdir -p "$dst"
  local pids=() failed=0
  shopt -s nullglob
  for f in "$src"/*; do
    [ -f "$f" ] || continue
    local name
    name=$(basename "$f")
    if [ -f "$dst/$name" ]; then
      echo "[skip] $dst/$name already exists" >&2
    else
      echo "[copy] $f -> $dst/$name" >&2
      cp "$f" "$dst/$name" &
      pids+=($!)
    fi
  done
  for pid in "${pids[@]}"; do
    wait "$pid" || { echo "[error] cp pid=$pid failed" >&2; failed=1; }
  done
  return $failed
}
copy_files_parallel "$DRIVE_DATASETS/datasets" "$DEST/datasets"
```

- **並列コピー** … `cp ... &` でバックグラウンド実行して、最後に `wait` でまとめて待つ。ファイル数が多いほど効く。
- **冪等（べきとう）** … 「何度実行しても結果が同じ」という意味。コピー先に同名ファイルがあればスキップするので、途中で止めて再実行しても無駄なコピーが走らない。
- **引数で上書き可** … コピー元・先は第 1／第 2 引数で変えられる（省略時はデフォルトのパス）。
- `set -euo pipefail` … エラーや未定義変数があればそこで止まる安全装置。

なお対象はフォルダ直下のファイルだけ。サブフォルダごとまるっとコピーしたいときは `cp -r` や `rsync` に寄せると楽。

Title: PostgreSQL をアップデート後にクエリが急に遅くなったときの調査手順
Date: 2026-01-25 09:28:04
Modified: 2026-01-25 09:28:04
Category: tech
Tags: tech
Slug: tech-postgresql-update-explain-investigation
Summary: データベースのアップデート前後で特定のクエリだけ実行が遅くなった時にどう調べたらいいのかわからなかったので調査手順を備忘録として残しておく。

## はじめに

仕事で PostgreSQL のアップデートを行った時に、古いバージョンで10分以内に終わっていたクエリが、新しいバージョン後に1時間経っても終わらない状況になった。

アップデート前のスナップショットはあるが、古いバージョンの PostgreSQL を再度立ち上げて原因調査するのは大変だし、新しいバージョン側はクエリが終わらないので EXPLAIN (ANALYZE) を取ることもままならなかった。

なので「新しいバージョンのみ」で、どこまで原因を絞れて、どう進めるのが良いかを残しておく。今回の事例については細かくは説明しない。
（※ [EXPLAIN (ANALYZE)](https://www.postgresql.org/docs/current/sql-explain.html) は計測の都合で通常実行より遅くなることがあるので、本番で雑に回すのは注意。）

## 最初やること

クエリの実行が遅い場合、大きく3つくらい考えられる

1. 実行計画作成が遅い
2. クエリの実行が遅い
3. 結果の転送・ BI ツールが遅い

### 1. 実行計画作成が遅い

- EXPLAIN (ANALYZE) は実行するが返ってこないケースはある。
- まずは 実行しない EXPLAIN で判定する
```sql
EXPLAIN (COSTS, VERBOSE, SETTINGS)
<実行したいクエリ>;
```
- すぐ結果が返るなら「プランは作れている」＝ 実行フェーズ以降が怪しい
- 逆に、これ自体が重いなら Planning が怪しい
    - 複雑な条件式、巨大な IN、関数式、型変換の連鎖、やたら多い候補インデックスなど

### 2. クエリの実行が遅い

クエリの実行が遅い場合、ざっくり「待ち」で分岐できる。
- Lock 待ち
- I/O 待ち（ディスク / temp）
- CPU（= 待ちが見えない、ひたすら計算してる）

### 3. 結果の転送・ BI ツールが遅い

DB は返してるのに、 BI ツールの画面に出てこないもの。この場合、結果内容を小さくして同じ条件で試すことで問題を切り分けられる。

- 例: 元クエリをサブクエリ化して LIMIT 1 だけ返す
```sql
SELECT * FROM (<元クエリ>) t LIMIT 1;
```
- これが速いなら「結果表示（転送量 or クライアント側処理）」が疑わしい。



## 実行中の原因調査

「実行が遅い」場合、何から手をつけていけばいいかわからない。実行中に観測できるものをまとめて、原因のあたりをつける手順を考える。

### PostgreSQL の統計情報を見る

- [pg_stat_activity](https://www.postgresql.jp/docs/17/monitoring-stats.html)
    - 現在の実行中の SQL / 状態 / 待ち
- [pg_stat_statements](https://www.postgresql.jp/document/17/html/pgstatstatements.html)
    - 実行した SQL の累積（回数、時間、I/O、temp など）
- [pg_stat_database](https://www.postgresql.jp/docs/17/monitoring-stats.html#MONITORING-PG-STAT-DATABASE-VIEW)
    - DB 全体の統計（temp など）

SQL の実行時間が長い場合に「何が起きているか」を観測したいなら、まず pg_stat_activity を見ると良い。


### 実行計画を確認する

```sql
EXPLAIN (COSTS, VERBOSE, SETTINGS)
<実行したいクエリ>;
```

見るポイント（雑に当たりをつける）：

- Seq Scan になってないか（または Index Scan だけど条件が緩くて 実質ほぼ全件）
- JOIN 順が不自然で、巨大側を先に読んでいないか
- 推定行数（rows）が極端にズレてないか（= 統計不足・統計の質の問題かも）
- CTE が「何度も参照されてる」形になってないか
    - CTE Scan がループで回ってたり、巨大 CTE を何度も Materialize してる雰囲気があると危険

※ SETTINGS を付けておくと「そのプランに効いた設定」が出るので、アップデート前後差分の当たりを付けやすい。


### 実行中に何の待ちが発生しているか

```sql
SELECT
  pid,
  state,
  wait_event_type,
  wait_event,
  now() - query_start AS running_for,
  left(query, 200) AS query_head
FROM pg_stat_activity
WHERE datname = current_database()
  AND state <> 'idle'
ORDER BY query_start;
```

雑な読み方：

- `wait_event_type=Lock` ならロック待ち（ブロッカーを探す）
- `wait_event_type=IO` なら I/O 寄り（temp スピルやディスク読み書き）
    - `wait_event_type=IO` / `wait_event=BuffileRead` が出たり消えたりする場合、 temp を 読み書きしながら処理してる。
- `wait_event_type=NULL` で state = 'active' なら、だいたい CPU で殴ってる（= 計算・結合・フィルタが重い）

### temp スピルの発生の有無（pg_stat_database）

```sql
SELECT
  datname,
  temp_files,
  temp_bytes
FROM pg_stat_database
WHERE datname = current_database();
```

- temp_files / temp_bytes は統計リセット以降の累積なので、数秒おきに 2〜3 回見て増えているか を見る
- 増えていれば temp I/O の可能性が高い

### 一時ファイル（temp）の犯人を特定する（pg_stat_statements）

```sql
SELECT
    d.datname AS database_name,
    r.rolname AS user_name,
    p.queryid,
    p.calls, -- 実行回数
    -- 一時ファイル関連 (ブロック数 * 8KB = サイズ)
    (p.temp_blks_read * 8192) / 1024 / 1024 AS temp_read_mb,
    (p.temp_blks_written * 8192) / 1024 / 1024 AS temp_write_mb,
    -- 平均実行時間
    (p.total_exec_time / p.calls)::numeric(10, 2) AS mean_time_ms,
    -- クエリの一部
    regexp_replace(left(p.query, 200), '[\r\n]+', ' ', 'g') AS query_head
FROM pg_stat_statements p
LEFT JOIN pg_database d ON p.dbid = d.oid
LEFT JOIN pg_roles r ON p.userid = r.oid
ORDER BY temp_blks_written DESC -- 一時ファイルをたくさん書いた順
```

- `pg_stat_statements` を使って、temp をたくさん吐いたクエリを上から見るのが早い。
- temp_blks_read / temp_blks_written は pg_stat_statements の列として存在する
    - https://www.postgresql.org/docs/current/pgstatstatements.html

## 最後に

実際に仕事で起きたケースで行くと、CTE のクエリが Index Scan になっているが row がほぼ全件で、 CTE を繰り返し参照されていたため、実行が終わらないクエリになってしまっていた。同様のケースがあった場合には何かしら使えると思う。

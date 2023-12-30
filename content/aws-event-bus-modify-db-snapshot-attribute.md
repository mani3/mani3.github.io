Title: EventBus で RDS のスナップショットの共有を検知する
Date: 2023-12-30 22:58:20
Modified: 2023-12-30 22:58:20
Category: aws
Tags: aws
Slug: aws-event-bus-modify-db-snapshot-attribute
Summary: AWS EventBridge と CloudTrail を組み合わせて RDS スナップショット共有を監視する方法を紹介します。

## はじめに

Amazon RDS には[イベントを検知する機能](https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/USER_Events.Messages.html)がありますが、スナップショット共有のイベントは検知できないようです。

スナップショット共有は [ModifyDBSnapshotAttribute](https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/APIReference/API_ModifyDBSnapshotAttribute.html)  API が使用されます。 CloudTrail で API コールを検知することができるため、スナップショット共有を検知できます。
また、アカウント間のイベントは EventBridge の [EventBus](https://docs.aws.amazon.com/ja_jp/eventbridge/latest/userguide/eb-event-bus.html) を利用することで別アカウントへイベント送信することができます。

今回は、AWS アカウント間でスナップショット共有したときに自動でスナップショットをリストアする仕組みが欲しかったので、 EventBridge を使ってスナップショット共有を検知する仕組みを作ってみました。

## RDS スナップショット共有の検知

CloudTrail の API コールを検知するための EventBridge のルールを作成します。
イベントルールは、以下のように作成します。

```json
{
  "source": ["aws.rds"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["rds.amazonaws.com"],
    "eventName": ["ModifyDBClusterSnapshotAttribute"],

    "requestParameters": {
      "valuesToAdd": [{ "exists": true }]
    },
    "responseElements": {
      "dBClusterSnapshotIdentifier": [{ "prefix": "sample-cluster" }]
    }
  }
}

```

いくつかの重要なポイントがあります。 CloudTrail で API コールを検知するときには、 `AWS API Call via CloudTrail` の detail-type を指定する必要があります。

`ModifyDBClusterSnapshotAttribute` だけでは、あらゆる変更によってイベントが発火してしまいます。
`requestParameters` に `valuesToAdd` がある場合、共有先のアカウント ID が含まれています。共有を解除する場合は、 `valuesToRemove` が含まれますのでイベントは発火しません。

また、`responseElements` に `dBClusterSnapshotIdentifier` にプレフィックスを指定して特定のスナップショットのみイベントを発火するようにしています。

## EventBus の作成

EventBridge を用いたイベントの送信には、まず EventBus の作成が必要です。
共有先のアカウントで作成するリソースを Terraform で作成すると以下のようになります。

```terraform
resource "aws_cloudwatch_event_bus" "event_bus" {
  name = "rds-snapshot-share-event-bus"
}

data "aws_iam_policy_document" "policy" {
  statement {
    sid    = "OtherAccountAccess"
    effect = "Allow"
    actions = [
      "events:PutEvents",
    ]
    resources = [
      aws_cloudwatch_event_bus.event_bus.arn,
    ]

    principals {
      type = "AWS"
      # 共有元の AWS アカウント ID
      identifiers = ["123456789012"]
    }
  }
}

resource "aws_cloudwatch_event_bus_policy" "event_bus" {
  event_bus_name = aws_cloudwatch_event_bus.event_bus.name
  policy         = data.aws_iam_policy_document.policy.json
}

resource "aws_cloudwatch_event_rule" "event_bus" {
  name           = "rds-snapshot-share"
  event_bus_name = aws_cloudwatch_event_bus.event_bus.name

  event_pattern = jsonencode({
    source      = ["aws.rds"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventSource = ["rds.amazonaws.com"]
      eventName   = ["ModifyDBClusterSnapshotAttribute"]

      requestParameters = {
        valuesToAdd = [{ exists = true }],
      }
      responseElements = {
        dBClusterSnapshotIdentifier = [{ prefix = "sample-cluster" }]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "event_bus" {
  event_bus_name = aws_cloudwatch_event_bus.event_bus.name
  rule           = aws_cloudwatch_event_rule.event_bus.name
  arn            = <共有されたスナップショットのリストア処理>
  role_arn       = aws_iam_role.event_bridge.arn
}

```

## 共有元の EventBridge の作成

共有元のアカウントでイベントを送信するためには、 EventBus の ARN を指定してルールを作成します。

```terraform

resource "aws_cloudwatch_event_rule" "share_snapshot" {
  name        = "rds-modify-db-cluster-snapshot-attribute"

  event_pattern = jsonencode({
    source      = ["aws.rds"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventSource = ["rds.amazonaws.com"]
      eventName   = ["ModifyDBClusterSnapshotAttribute"]
      requestParameters = {
        valuesToAdd = [{ exists = true }],
      }
      responseElements = {
        dBClusterSnapshotIdentifier = [{ prefix = "sample-cluster" }]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "share_snapshot" {
  rule     = aws_cloudwatch_event_rule.share_snapshot.name
  arn      = <共有先の EventBus の ARN>
  role_arn = aws_iam_role.event_bridge.arn
}
```

## さいごに

AWS の EventBridge と CloudTrail を組み合わせることで、データベースのスナップショット共有を効率的に監視することが可能です。
この機能を活用することで、スナップショットの共有を自動的に検知し、即時にリストアするシステムを構築できます。

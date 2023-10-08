Title: AWS SES ログを S3 に保存する
Date: 2023-10-08 22:54:45
Modified: 2023-10-08 22:54:45
Category: aws
Tags: aws
Slug: aws-ses-logging
Summary: AWS SES のログを S3 に保存する方法を Terraform で構築したのでメモ。

## はじめに

AWS SES のログを S3 に保存する方法を Terraform で構築したのでメモ。

## Terraform による構築

### SES の設定

SES にドメインの登録を行うのと送信アドレスを登録する。
ログを残す場合、 `aws_ses_configuration_set` を設定することでいくつかログの送信先が設定できる。

- [aws_ses_configuration_set](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ses_configuration_set)
- [aws_ses_event_destination](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ses_event_destination)

今回は、Firehose を使って S3 に保存するようにした。
ただ、AWS コンソール上だと configuration_set のデフォルト設定を行うことができるが、Terraform ではできない様子。
仕方ないので、 terraform apply を行ったあとに、コンソール上で設定を行う必要がある。

```terraform
resource "aws_ses_domain_identity" "ses_domain" {
  domain   = var.ses_domain
  provider = aws.east
}

resource "aws_ses_domain_dkim" "ses_domain_dkim" {
  domain   = aws_ses_domain_identity.ses_domain.domain
  provider = aws.east
}

resource "aws_ses_email_identity" "ses_email" {
  email    = var.ses_email
  provider = aws.east
}

resource "aws_ses_configuration_set" "configuration_set" {
  name     = "${var.stack}-${var.env}-configuration-set"
  provider = aws.east
}

resource "aws_ses_event_destination" "firehose" {
  name                   = "event-destination-firehose"
  configuration_set_name = aws_ses_configuration_set.configuration_set.name
  enabled                = true
  matching_types         = ["bounce", "complaint", "delivery", "send", "reject", "open", "click"]

  kinesis_destination {
    stream_arn = aws_kinesis_firehose_delivery_stream.extended_s3_stream.arn
    role_arn   = aws_iam_role.ses_role.arn
  }
  provider = aws.east
}
```

### Provider の設定

SES を `us-east-1` で作成したので、 `us-east-1` に対しては `aws.east` という alias をつけている。

```terraform
provider "aws" {
  alias  = "east"
  region = "us-east-1"

  default_tags {
    tags = {
      env       = var.env,
      stack     = var.stack,
      terraform = true,
    }
  }
}
```

### S3 の設定

```terraform
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.stack}-${var.env}-email-logs"
}
```

### CloudWatch Logs の設定

```terraform
resource "aws_cloudwatch_log_group" "ses" {
  name              = "/aws/ses/${var.stack}-${var.env}"
  retention_in_days = 30
  provider          = aws.east
}
```

### Firehose の設定

- [aws_kinesis_firehose_delivery_stream](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kinesis_firehose_delivery_stream)

```terraform
resource "aws_kinesis_firehose_delivery_stream" "extended_s3_stream" {
  name        = "${var.stack}-${var.env}-kinesis-firehose-extended-s3-stream"
  destination = "extended_s3"
  provider    = aws.east

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.bucket.arn

    buffering_size = 64

    cloudwatch_logging_options {
      enabled         = "true"
      log_group_name  = aws_cloudwatch_log_group.ses.name
      log_stream_name = "extended_s3"
    }

    prefix              = "data/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/"
    error_output_prefix = "errors/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/!{firehose:error-output-type}/"
  }
}

```

### IAM の設定

SES から Firehose にログを送るためには、SES から Firehose にアクセスできる IAM ロールが必要になる。
また、Firehose から S3 にログを保存するためには、Firehose から S3 にアクセスできる IAM ロールが必要。

```terraform
# SES

resource "aws_iam_role" "ses_role" {
  name               = "${var.stack}-${var.env}-ses-role"
  assume_role_policy = data.aws_iam_policy_document.ses_assume_policy_document.json
}

resource "aws_iam_role_policy" "ses_policy" {
  role   = aws_iam_role.ses_role.name
  policy = data.aws_iam_policy_document.ses_policy_document.json
}

data "aws_iam_policy_document" "ses_assume_policy_document" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ses.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "ses_policy_document" {
  statement {
    actions = [
      "firehose:PutRecordBatch",
    ]
    resources = ["*"]
  }
}

# Firehose

resource "aws_iam_role" "firehose_role" {
  name               = "${var.stack}-${var.env}-firehose-role"
  assume_role_policy = data.aws_iam_policy_document.firehose_assume_policy_document.json
}

resource "aws_iam_role_policy" "firehose_policy" {
  role   = aws_iam_role.firehose_role.name
  policy = data.aws_iam_policy_document.firehose_policy_document.json
}

data "aws_iam_policy_document" "firehose_assume_policy_document" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["firehose.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "firehose_policy_document" {
  statement {
    actions = [
      "s3:AbortMultipartUpload",
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads",
      "s3:PutObject",
    ]
    resources = ["*"]
  }

  statement {
    actions = [
      "cloudwatch:*",
    ]
    resources = ["*"]
  }
}

```

## さいごに

configuration set の設定は、 terraform apply を行ったあとに、コンソール上で設定を行う必要があるので以下の手順で設定する。

- [https://docs.aws.amazon.com/ja_jp/ses/latest/dg/managing-configuration-sets.html](https://docs.aws.amazon.com/ja_jp/ses/latest/dg/managing-configuration-sets.html)

delivery の場合、以下のようなログが S3 に保存される。（適当にマスクしてます）

```json
{
  "eventType": "Delivery",
  "mail": {
    "timestamp": "2023-10-08T00:26:46.312Z",
    "source": "noreply@example.com",
    "sourceArn": "arn:aws:ses:us-east-1:981185984049:identity/example.com",
    "sendingAccountId": "012345678901",
    "messageId": "0100018b0cadeaa8-7003157d-b5b6-4495-bd5b-31e9097a005f-000000",
    "destination": ["success@simulator.amazonses.com"],
    "headersTruncated": false,
    "headers": [
      { "name": "MIME-Version", "value": "1.0" },
      {
        "name": "Content-Type",
        "value": "multipart/mixed; boundary=\"delimiter\""
      },
      { "name": "From", "value": "noreply@example.com" }
    ],
    "commonHeaders": {
      "from": ["noreply@example.com"],
      "messageId": "0100018b0cadeaa8-7003157d-b5b6-4495-bd5b-31e9097a005f-000000"
    },
    "tags": {
      "ses:operation": ["SendRawEmail"],
      "ses:configuration-set": ["sample-dev-configuration-set"],
      "ses:source-ip": ["xxx.xxx.xxx.xxx"],
      "ses:from-domain": ["example.com"],
      "ses:caller-identity": ["xxx"],
      "ses:outgoing-ip": ["xxx.xxx.xxx.xxx"]
    }
  },
  "delivery": {
    "timestamp": "2023-10-08T00:26:46.710Z",
    "processingTimeMillis": 398,
    "recipients": ["success@simulator.amazonses.com"],
    "smtpResponse": "250 2.6.0 Message received",
    "reportingMTA": "xxx.smtp-out.amazonses.com"
  }
}
```

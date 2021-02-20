Title: Apple Connect API 使ってアプリをアップロードする
Date: 2021-02-21 00:33:28
Modified: 2021-02-21 00:33:28
Category: ios
Tags: ios
Slug: ios-apple-connect-api
Summary: Github Action 上で iOS アプリをビルドして、Apple Connect API 経由でアップロードする


## Apple Connect API

1. Apple Connect の User and Roles から Keys を開く
2. 「+」から名前と Developer を選択して Generate
3. 以下の3つを確認する
    - Issuer ID
    - KEY ID
    - .p8 ファイル



## Fastlane

Fastlane から 使う場合は、 app_store_connect_api_key メソッドを使う

- app_store_connect_api_key
    - [https://docs.fastlane.tools/actions/app_store_connect_api_key/](https://docs.fastlane.tools/actions/app_store_connect_api_key/)


```ruby
default_platform(:ios)

platform :ios do
  desc "Builds the app for AppStore release"
  lane :build_release do |options|

    # Apple Connect API
    api_key = app_store_connect_api_key(
      key_id: ENV['APPLE_STORE_CONNECT_KEY_ID'],
      issuer_id: ENV['APPLE_STORE_CONNECT_ISSUER_ID'],
      key_content: ENV['APPLE_STORE_CONNECT_KEY_CONTENT'],
    )

    team_id = CredentialsManager::AppfileConfig.try_fetch_value(:team_id)
    app_identifier = CredentialsManager::AppfileConfig.try_fetch_value(:app_identifier)
    
    # ...

    # Generate build number
    increment_build_number(
      build_number: latest_testflight_build_number(api_key: api_key) + 1
    )

    # Build app ...

    # Upload to Testflight
    pilot(
      api_key: api_key,
      skip_submission: true,
      skip_waiting_for_build_processing: true,
      ipa: "./builds/xxx.ipa"
    )
  end
end
```

ビルド番号をインクリメントするときは、 `latest_testflight_build_number` の引数に `api_key` を指定する

```ruby
# Generate build number
increment_build_number(
  build_number: latest_testflight_build_number(api_key: api_key) + 1
)
```

TestFlight へアップロードするときも、 `api_key` の引数をつける。

```ruby
# Upload to TestFlight
pilot(
  api_key: api_key,
  skip_submission: true,
  skip_waiting_for_build_processing: true,
  ipa: "./builds/xxx.ipa"
)
```




## Github Actions

- リポジトリから Settings -> Secrets を開く
- 「New repository secret」からそれぞれ設定する
    - `APPLE_STORE_CONNECT_KEY_ID`=<KEY ID\>
    - `APPLE_STORE_CONNECT_ISSUER_ID`=<Issuer ID\>
    - `APPLE_STORE_CONNECT_KEY_CONTENT`=<.p8ファイルの中身>


Github Actions の workflows の一例、fastlane のビルドと環境変数を記述する。

```yaml
name: Build and Deploy to App Store Connect

on:
  push:
    branches: [ master ]

jobs:
  build:
    runs-on: macos-latest

    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - uses: actions/checkout@v2

    - name: Select Xcode
      run: sudo xcode-select -switch /Applications/Xcode_12.4.app

    # ...

    # Build and upload to app store connect
    - name: Run Fastlane - Deploy to AppStore Connect
      run: fastlane build_release
      env:
        APPLE_KEY_BASE64: ${{ secrets.APPLE_KEY_BASE64 }}
        APPLE_KEY_PASSWORD: ${{ secrets.APPLE_KEY_PASSWORD }}
        APPLE_STORE_CONNECT_KEY_ID: ${{ secrets.APPLE_STORE_CONNECT_KEY_ID }}
        APPLE_STORE_CONNECT_ISSUER_ID: ${{ secrets.APPLE_STORE_CONNECT_ISSUER_ID }}
        APPLE_STORE_CONNECT_KEY_CONTENT: ${{ secrets.APPLE_STORE_CONNECT_KEY_CONTENT }}
        PROVISIONING_PROFILE_BASE64: ${{ secrets.PROVISIONING_PROFILE_BASE64 }}
        PROVISIONING_PROFILE_WATCHKIT_BASE64: ${{ secrets.PROVISIONING_PROFILE_WATCHKIT_BASE64 }}
        PROVISIONING_PROFILE_WATCHKIT_EXTENSION_BASE64: ${{ secrets.PROVISIONING_PROFILE_WATCHKIT_EXTENSION_BASE64 }}
```


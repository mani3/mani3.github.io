title: [Xcode] Xcode 9.1 でコマンドからビルドしたときでたエラーの対応方法
Date: 2017-11-05 00:29:57
Modified: 2017-11-05 00:29:57
Category: ios
Tags: ios
Slug: xcode91-cocoapods-xcodebuild-error
Summary: Xcode 9.1 + Cocoapods でコマンドからビルドしたときのエラーを対応

- Xcode 9.1
- Cocoapods 1.3.1

Xcode 9.1 でコマンドからビルドしたら以下のようなエラーがでた。
Xcode 9.1 GUI からビルドする分には問題なかった...😭

```sh
Code Signing Error: GoogleToolboxForMac-Defines-Logger-NSData+zlib does not support provisioning profiles. GoogleToolboxForMac-Defines-Logger-NSData+zlib does not support provisioning profiles, but provisioning profile NO_SIGNING/ has been manually specified. Set the provisioning profile value to "Automatic" in the build settings editor.
```

ぐぐったらすぐ出てきた。 一応これで解決した。。

- https://discuss.circleci.com/t/xcode-9-build-failures-due-to-code-signing-errors-in-pods/16713/2

```ruby
  post_install do |installer|
    installer.pods_project.build_configurations.each do |config|
      config.build_settings['PROVISIONING_PROFILE_SPECIFIER'] = ''
    end
  end
```

title: Xcode 8.3 で Documentation Issue がでたときの対応
Date: 2017-10-12 22:18:22
Modified: 2017-10-12 22:18:22
Category: ios
Tags: ios
Slug: xcode83-documentation-issue-warning
Summary: Xcode 8.3 のときに CocoaPods のライブラリの Documentation Issue が出たのでそのときの対応方法

## Documentation Issue

Xcode 8.3.3 でビルドするようになって、 CocoaPodsで入れているライブラリの Documentation Issue の Warning がでるようになった。


AWSCore だとこういうのがでてた。

```
Documentation Issue
Parameter 'kits' not found in the function declaration
```


- https://github.com/realm/realm-cocoa/issues/4853

Realm 入れてるとたくさんでるみたいだった。

とりあえず、以下を `Podfile` 入れたらWarningが消えた。

```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['CLANG_WARN_DOCUMENTATION_COMMENTS'] = 'NO'
      end
  end
end
```

あとは手動で `Pods.xcodeproj` の 方の `CLANG_WARN_DOCUMENTATION_COMMENTS` を NO にするか。


Title: [Xcode] Xcode 9 から xcodebuild で ipa ファイルにするときメモ 
Date: 2017-11-16 20:40:27
Modified: 2017-11-16 20:40:27
Category: ios
Tags: ios
Slug: xcode91-xcodebuild-exportoptionplist
Summary: xcodebuild で ipa ファイルにするときの exportOptionsPlist にオプションが増えた

[Xcode Release Notes](https://developer.apple.com/library/content/releasenotes/DeveloperTools/RN-Xcode/Chapters/Introduction.html#//apple_ref/doc/uid/TP40001051-CH1-SW876)

- signingStyle
- signingCertificate
- provisioningProfiles

`xcodebuild` のオプションの `-exportOptionsPlist` に指定する plist ファイルに追加できるキーが増えていた。実際に `xcodebuild -h` で詳細が書いてある。

```sh
    provisioningProfiles : Dictionary

        For manual signing only. Specify the provisioning profile to use for each executable in your app. Keys in this dictionary are the bundle identifiers of executables; values are the provisioning profile name or UUID to use.

    signingCertificate : String

        For manual signing only. Provide a certificate name, SHA-1 hash, or automatic selector to use for signing. Automatic selectors allow Xcode to pick the newest installed certificate of a particular type. The available automatic selectors are "Mac App Distribution", "iOS Distribution", "iOS Developer", "Developer ID Application", and "Mac Developer". Defaults to an automatic certificate selector matching the current distribution method.

    signingStyle : String

        The signing style to use when re-signing the app for distribution. Options are manual or automatic. Apps that were automatically signed when archived can be signed manually or automatically during distribution, and default to automatic. Apps that were manually signed when archived must be manually signed during distribtion, so the value of signingStyle is ignored.
```

`stripSwiftSymbols` とかも Xcode 9 から増えてる気がする。。
説明を読んで以下のような plist ファイル (exportOptions.plist) を用意したら `exportArchive` できました🤗

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">;
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>signingStyle</key>
    <string>manual</string>
    <key>signingCertificate</key>
    <string>iPhone Distribution: xxxxx</string>
    <key>provisioningProfiles</key>
    <dict>
        <key>io.github.mani3.xxxxx</key>
        <string>e3584093-4ad1-4176-b736-xxxxxxxxxx</string>
    </dict>
</dict>
</plist>
``` 

あとはビルドしたあとに以下のような感じでいつも通りパッケージングすることができた。

```sh
$ xcodebuild -exportArchive -archivePath XXXXX.xcarchive -exportPath archive -exportOptionsPlist exportOptions.plist
```

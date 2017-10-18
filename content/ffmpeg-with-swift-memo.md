title: FFmpeg を Swift から使ってみる
Date: 2017-10-14 20:48:44
Modified: 2017-10-14 20:48:44
Category: ios
Tags: ios
Slug: ffmpeg-with-swift-memo
Summary: FFmpeg を使って動画のメタデータを Swift から読み込む 

## 動画のメタデータの表示

`-Bridging-Header.h` に import する

```
#ifndef FFmpegMetadata_Bridging_Header_h
#define FFmpegMetadata_Bridging_Header_h

#import <libavcodec/avcodec.h>
#import <libavformat/avformat.h>
#import <libswscale/swscale.h>

#endif
```

メタデータを標準出力する

```swift
func metadata(filename: String) {
    var formatContext: UnsafeMutablePointer<AVFormatContext>?
    
    av_register_all()
    
    if avformat_open_input(&formatContext, filename, nil, nil) != 0 {
        print("Could not open file:", filename)
        return
    }
    
    var tag: UnsafeMutablePointer<AVDictionaryEntry>! = av_dict_get(formatContext!.pointee.metadata, "", nil, AV_DICT_IGNORE_SUFFIX)
    while tag != nil {
        let key = String(cString: tag.pointee.key)
        let value = String(cString: tag.pointee.value)
        print(key, "=", value)
        tag = av_dict_get(formatContext!.pointee.metadata, "", tag, AV_DICT_IGNORE_SUFFIX)
    }
    
    let ret = avformat_find_stream_info(formatContext, nil)
    print("ret=\(ret)")
    
    avformat_close_input(&formatContext)
}

metadata(filename: "path/to/big_buck_bunny_720p_h264.mov")
```

## 実行

`big_buck_bunny_720p_h264.mov` の動画のメタデータを表示する

```sh
major_brand = qt  
minor_version = 537199360
compatible_brands = qt  
creation_time = 2008-05-27T18:36:22.000000Z
com.apple.quicktime.player.movie.audio.gain = 1.000000
com.apple.quicktime.player.movie.audio.treble = 0.000000
com.apple.quicktime.player.movie.audio.bass = 0.000000
com.apple.quicktime.player.movie.audio.balance = 0.000000
com.apple.quicktime.player.movie.audio.pitchshift = 0.000000
com.apple.quicktime.player.movie.audio.mute = 
com.apple.quicktime.player.movie.visual.brightness = 0.000000
com.apple.quicktime.player.movie.visual.color = 1.000000
com.apple.quicktime.player.movie.visual.tint = 0.000000
com.apple.quicktime.player.movie.visual.contrast = 1.000000
com.apple.quicktime.player.version = 7.4.1 (14)
com.apple.quicktime.version = 7.4.1 (14) 0x7418000 (Mac OS X, 10.5.2, 9C31)
ret=0
```

title: [mbed] mbed のオフライン環境をメモ2
Date: 2017-10-27 21:33:55
Modified: 2017-10-27 21:33:55
Category: development
Tags: mbed
Slug: mbed-local-environment-memo2
Summary: mbed のローカル環境を準備したときのメモ2

オフラインの環境できたと思ったけど、 [BLE_API](https://os.mbed.com/teams/Bluetooth-Low-Energy/code/BLE_API) や [nRF51822](https://os.mbed.com/teams/Nordic-Semiconductor/code/nRF51822) を include したらビルドできなかった。

## mbed.bld に以下を記載しておく

```sh
https://mbed.org/users/mbed_official/code/mbed/builds/4eea097334d6
```

## 必要なものを追加

```sh
// BLE_API を追加
(mbed) $ mbed add https://os.mbed.com/teams/Bluetooth-Low-Energy/code/BLE_API/

// nRF51822 を追加
(mbed) $ mbed add https://os.mbed.com/teams/Nordic-Semiconductor/code/nRF51822/

// mbed (4eea097334d6) を追加
(mbed) $ mbed deploy
```

これでビルドできるようになったけど、 `Warning` が多かったり、 `mbed detect` できなかったりもう少し試行錯誤が必要そうだ 🤕


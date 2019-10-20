Title: UbuntuでGPU環境をセットアップ
Date: 2019-10-15 02:46:57
Modified: 2019-10-15 02:46:57
Category: deep-learning
Tags: deep-learning
Slug: setup-ubuntu-gpu-environment
Summary: なかなかスタンダードな方法はないのかな

## はじめに

先日 RTX 2080 Ti を購入したのだけど、MNISTくらいのタスクは実行できるのだけど大きいタスクをやらせると画面にノイズが入って勝手に再起動してしまう現象が起きて苦労した。
結局、初期不良ということで交換対応してもらえた。
そのときにNVIDIAドライバを入れ直したり環境を作ったり壊したりしていて、良さそうなGPU環境のセットアップを決めた。
もう、CUDAのインストールも面倒なのでDockerベースでやることにした。

- https://github.com/NVIDIA/nvidia-docker

上記のリポジトリにnvidiaのコンテナイメージが提供されている。
今後学習もコンテナでやることにしたので、準備をつらつら書いてみる

## 準備

- Ubuntu 18.04

## NVIDIA ドライバのインストール

[NVIDIA/nvidia-docker](https://github.com/NVIDIA/nvidia-docker)にもあるが、NVIDIAドライバのインストールは最低限必要になっている。

Ubuntu環境で `ubuntu-drivers devices` を実行すると推奨ドライバがわかる。

```sh
$ ubuntu-drivers devices
== /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
modalias : pci:v000010DEd00001E07sv000010DEsd00001E07bc03sc00i00
vendor   : NVIDIA Corporation
driver   : nvidia-driver-430 - distro non-free recommended
driver   : xserver-xorg-video-nouveau - distro free builtin
```

とりあえず、自動でインストールして再起動する

```sh
$ sudo ubuntu-drivers autoinstall
$ sudo reboot now
```

再起動後にデバイスが認識しているか `nvidia-smi` を実行する。一応大丈夫そう。

```sh
$ nvidia-smi
Sat Oct 13 00:24:59 2019
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 430.26       Driver Version: 430.26       CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce RTX 208...  Off  | 00000000:01:00.0  On |                  N/A |
| 35%   40C    P8    24W / 260W |     99MiB / 11016MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+


+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0      1078      G   /usr/lib/xorg/Xorg                            39MiB |
|    0      1124      G   /usr/bin/gnome-shell                          58MiB |
+——————————————————————————————————————+
```

## Docker インストール

ほとんど、公式のインストール方法のまま。現時点の最新は19.03。

- https://docs.docker.com/install/linux/docker-ce/ubuntu/

```sh
$ sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88
$ sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
$ sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io
$ sudo usermod -aG docker <user>
$ sudo reboot now
$ docker version
Client: Docker Engine - Community
 Version:           19.03.3
 API version:       1.40
 Go version:        go1.12.10
 ...

Server: Docker Engine - Community
 Engine:
  Version:          19.03.3
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.10
 ...
```

## NVIDIA のコンテナツールのインストール

これは [NVIDIA/nvidia-docker](https://github.com/NVIDIA/nvidia-docker) のまま。

```sh
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
$ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
$ sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
$ sudo systemctl restart docker
$ sudo reboot now
$ docker run --gpus all --rm nvidia/cuda nvidia-smi
Unable to find image 'nvidia/cuda:latest' locally
latest: Pulling from nvidia/cuda
35c102085707: Pull complete
...
Status: Downloaded newer image for nvidia/cuda:latest
Fri Oct 14 15:42:40 2019
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 430.26       Driver Version: 430.26       CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce RTX 208...  Off  | 00000000:01:00.0 Off |                  N/A |
| 35%   33C    P8    22W / 260W |     26MiB / 11016MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+


+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
```

## Dockerfile

最終的な学習用のコンテナイメージはこんな感じで、これからはTF2.0を使っていこうと思う。
`jupyterlab` を使えるようにしている。また `jupyterlab` から Tensorboard が開けるように nodejs 12.xをインストールするようにしてる。


```docker
FROM tensorflow/tensorflow:2.0.0-gpu-py3

RUN apt-get update && apt-get install -y --no-install-recommends \
libsm6 \
libxext6 \
libxrender-dev

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/pip install -U pip
RUN /usr/local/bin/pip --no-cache-dir install \
wheel \
Pillow \
matplotlib \
numpy \
pandas \
scipy \
sklearn \
tqdm \
argparse \
boto3 \
mtcnn \
Cython \
contextlib2 \
lxml \
jupyter \
jupyterlab \
easydict

RUN /usr/local/bin/pip --no-cache-dir install \
kaggle \
opencv-python

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get install -y nodejs
RUN jupyter labextension install jupyterlab_tensorboard
```

### 使い方

```sh
// イメージを作る
$ docker build -t tf2 -f Dockerfile .

// jupyterlab を起動させる
$ docker run -p 8888:8888 -v `pwd`:/docker --gpus all -it --rm tf2 jupyter lab --ip=0.0.0.0 --allow-root
```



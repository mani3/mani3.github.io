Title: macOS の gcc環境準備
Date: 2020-11-03 13:18:54
Modified: 2020-11-03 13:18:54
Category: gcc
Tags: gcc
Slug: gcc-in-macos
Summary: macOS で gcc 環境準備

## はじめに

いろいろなところに書いてあるけど、macOS で gcc を使うと Xcode の clang が使われるので、gcc を使えるようにしたい。

Apery をmacでビルドしたときに以下のエラーがでたのでその対応方法です。

```shell
❯ git clone https://github.com/HiraokaTakuya/apery.git
❯ cd apery/src
❯ make all

...

g++ -std=c++11 -fno-exceptions -fno-rtti -Wextra -Ofast -MMD -MP -fopenmp  -o ../obj/main.o -c main.cpp
clang: error: unsupported option '-fopenmp'
make: *** [../obj/main.o] Error 1
```

## 準備

- macOS 10.15.7 


```shell
// clang が使われる
❯ gcc -v
Configured with: --prefix=/Applications/Xcode.12.0.app/Contents/Developer/usr --with-gxx-include-dir=/Applications/Xcode.12.0.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/4.2.1
Apple clang version 12.0.0 (clang-1200.0.32.2)
Target: x86_64-apple-darwin19.6.0
Thread model: posix
InstalledDir: /Applications/Xcode.12.0.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin

// gcc をインストール
❯ brew install gcc

// gcc インストール後もかわらない
❯ gcc -v
Configured with: --prefix=/Applications/Xcode.12.0.app/Contents/Developer/usr --with-gxx-include-dir=/Applications/Xcode.12.0.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/4.2.1
Apple clang version 12.0.0 (clang-1200.0.32.2)
Target: x86_64-apple-darwin19.6.0
Thread model: posix
InstalledDir: /Applications/Xcode.12.0.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin


// Homebrew からインストールした gcc
❯ ls /usr/local/bin/gcc*
/usr/local/bin/gcc-10        /usr/local/bin/gcc-ar-10     /usr/local/bin/gcc-nm-10     /usr/local/bin/gcc-ranlib-10

// シンボリックリンク作成
❯ ln -s /usr/local/bin/gcc-10 /usr/local/bin/gcc
❯ ln -s /usr/local/bin/g++-10 /usr/local/bin/g++

// 別のターミナルを開いて実行
❯ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/local/Cellar/gcc/10.2.0/libexec/gcc/x86_64-apple-darwin19/10.2.0/lto-wrapper
Target: x86_64-apple-darwin19
Configured with: ../configure --build=x86_64-apple-darwin19 --prefix=/usr/local/Cellar/gcc/10.2.0 --libdir=/usr/local/Cellar/gcc/10.2.0/lib/gcc/10 --disable-nls --enable-checking=release --enable-languages=c,c++,objc,obj-c++,fortran --program-suffix=-10 --with-gmp=/usr/local/opt/gmp --with-mpfr=/usr/local/opt/mpfr --with-mpc=/usr/local/opt/libmpc --with-isl=/usr/local/opt/isl --with-system-zlib --with-pkgversion='Homebrew GCC 10.2.0' --with-bugurl=https://github.com/Homebrew/homebrew-core/issues --disable-multilib --with-native-system-header-dir=/usr/include --with-sysroot=/Library/Developer/CommandLineTools/SDKs/MacOSX10.15.sdk SED=/usr/bin/sed
Thread model: posix
Supported LTO compression algorithms: zlib
gcc version 10.2.0 (Homebrew GCC 10.2.0)
```


## Apery をビルドする

```shell
❯ make clean bmi2
```

これでビルドはできるので、以下を参考に将棋ソフトなどに利用することができる。

- 参考
    - [http://shogidokoro.starfree.jp/mac/compile.html](http://shogidokoro.starfree.jp/mac/compile.html)
    - [http://ringocatnote.com/entry/mac-elmo#Mac](http://ringocatnote.com/entry/mac-elmo#Mac)

## ライブラリとしての利用

Apery を Static Library として利用するために書いておきます。

```shell
❯ cd ..
❯ mkdir -p shared/include

❯ cp src/*.hpp shared/include
❯ ar rcs shared/libapery.a obj/benchmark.o obj/bitboard.o obj/book.o obj/common.o obj/evalList.o obj/evaluate.o obj/generateMoves.o obj/hand.o obj/init.o obj/move.o obj/movePicker.o obj/mt64bit.o obj/pieceScore.o obj/position.o obj/search.o obj/search.o obj/square.o obj/thread.o obj/timeManager.o obj/tt.o obj/usi.o
```

一応、これで shared というディレクトリを参照してやれば静的ライブラリとして利用できる。
Apery の実装などを参考に、ランダムな手を指すプログラムを書いてみる。

```cpp
#include <iostream>
#include <common.hpp>
#include <bitboard.hpp>
#include <init.hpp>
#include <position.hpp>
#include <usi.hpp>
#include <thread.hpp>
#include <tt.hpp>
#include <search.hpp>

#include <move.hpp>
#include <generateMoves.hpp>


int main(int argc, const char * argv[]) {
  int position_num = 0;
  std::mt19937 mt(std::chrono::system_clock::now().time_since_epoch().count());

  initTable();
  Position::initZobrist();

  auto s = std::unique_ptr<Searcher>(new Searcher);
  s->init();

  auto th = std::unique_ptr<Thread>(new Thread(s->thisptr));
  auto p = std::unique_ptr<Position>(new Position(DefaultStartPositionSFEN, th.get(), s->thisptr));

  while (position_num < MaxPly) {
    std::cout << p->toSFEN() << std::endl;

    StateInfo state[MaxPly+7];
    StateInfo* st = state;

    MoveList<Legal> ml(*p.get());
    if (ml.size()) {
      std::uniform_int_distribution<int> moveDist(0, ml.size() - 1);
      p->doMove((ml.begin() + moveDist(mt))->move, *st++);
    } else {
      break;
    }
    
    std::string sfen = p->toSFEN();
    std::istringstream ss(sfen);
    setPosition(*p.get(), ss);
    position_num++;
  }
  return 0;
}
```

これをどこか main.cpp として保存してビルドして実行すると適当な局面が生成されます。

```shell
❯ g++-10 main.cpp shared/libapery.a -lpthread -flto -std=c++11 -fno-exceptions -fno-rtti -Wextra -Ofast -MMD -MP -fopenmp -DNDEBUG -DHAVE_SSE4 -DHAVE_SSE42 -DHAVE_BMI2 -msse4.2 -mbmi2 -DHAVE_AVX2 -mavx2 -o a.out -Lshared -Ishared/include && ./a.out
sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1
sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1BR6/LNSGKGSNL w - 1
sfen lnsgkgsnl/1r5b1/pppp1pppp/4p4/9/9/PPPPPPPPP/1BR6/LNSGKGSNL b - 1
...
sfen 1n4+N2/l2k5/2p1gP3/1sGpPg1pP/2PN2p2/1PsP2P1p/rpR1Sg1PL/LB6s/1+B2K1+nL1 w 3Pp 1
sfen 1n4+N2/l2k5/2p1gP3/1sGpPg1pP/2PN2p2/1PsP2P1p/rpR1Sg1PL/LB4+n1s/1+B2K2L1 b 3Pp 1
sfen 1n4+N2/l2k5/2p1gP3/1sGpPg1pP/2PN2p2/1PsP2P1p/rpR1Sg1PL/LB4+n1s/1+B1K3L1 w 3Pp 1
```

とりあえず、Apery の実装などがすこし理解できたので、独自の将棋ソフトを作ってみたい気持ち。

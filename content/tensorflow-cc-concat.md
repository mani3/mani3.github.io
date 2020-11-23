Title: TensorFlow C++ を使って入力の整形
Date: 2020-11-23 00:10:48
Modified: 2020-11-23 00:10:48
Category: tensorflow
Tags: tensorflow
Slug: tensorflow-cc-concat
Summary: tensorflow::ops::Concat の実装例とか


## はじめに

TensorFlow C++ API をつかって、推論などの方法を試してますが結構難しいです😭<br>
実施に、推論するときには Session に対して、`tensorflow::Tensor` を入力に使いますが、たいていバッチに変換します。
`std::vector` や float 配列をバッチとして `tensorflow::Tensor` に変換するときに、Concat が使えそうなのですが ops なので Session での実行が伴います。
なので、バッチ入力する場合、 `tensorflow::Tensor` に値をアサインしていくほうがベターなのかなと思います。

そんなこんなで、Concat と 直接 Tensor に値を入れる方法の実装例をメモとして書いておきます。


## tensorflow::ops::Concat

Concat オペレーションを試しに使います。

- [https://www.tensorflow.org/api_docs/cc/class/tensorflow/ops/concat](https://www.tensorflow.org/api_docs/cc/class/tensorflow/ops/concat)

## 実装例

### コード

```cpp
#include <iostream>

#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/cc/ops/standard_ops.h>
#include <tensorflow/cc/client/client_session.h>

using namespace std;
using namespace tensorflow;

const int INPUT_SIZE = 9 * 9 * 1;

tensorflow::Tensor ConcatInputs(const std::vector<std::vector<float>> inputs) {
  Tensor tensor(tensorflow::DT_FLOAT, tensorflow::TensorShape({int(inputs.size()), 9, 9, 1}));
  
  auto dst = tensor.flat<float>().data();
  for (auto v: inputs) {
    std::copy_n(v.begin(), v.size(), dst);
    dst += v.size();
  }
  return tensor;
}

tensorflow::Tensor CreateTensor(float value) {
  Tensor input(tensorflow::DT_FLOAT, tensorflow::TensorShape({1, 9, 9, 1}));
  std::vector<float> values(9 * 9 * 1, value);
  std::copy_n(values.begin(), values.size(), input.flat<float>().data());
  return input;
}

void PrintTensor(const tensorflow::Tensor tensor) {
  auto size = tensor.flat<float>().size();
  auto p = tensor.flat<float>().data();

  std::vector<float> inputs(p, p + size);
  for (int i = 0; i < inputs.size(); i++) {
    if (i % (9 * 9 * 1) == 0) {
      std::cout << std::endl;
    }
    std::cout << inputs[i] << " ";
  }
  std::cout << std::endl;
}

int main(int argc, char **argv) {
  Scope root = Scope::NewRootScope();

  std::vector<std::vector<float>> values { 
    std::vector<float>(9 * 9 * 1, 1.f), 
    std::vector<float>(9 * 9 * 1, 2.f), 
    std::vector<float>(9 * 9 * 1, 3.f),
  };
  
  std::vector<Tensor> input_tensors {
    CreateTensor(1.f), 
    CreateTensor(2.f),
    CreateTensor(3.f),
  };

  // tensorflow::ops::Concat
  {
    std::vector<Tensor> concat_inputs;
    auto input = ops::Concat(root.WithOpName("Concat"), InputList({input_tensors[0], input_tensors[1], input_tensors[2]}), 0);
    
    ClientSession session(root);
    auto status = session.Run({input}, &concat_inputs);
    TF_CHECK_OK(status);

    PrintTensor(concat_inputs[0]);
  }

  std::cout << "==========================" << std::endl;

  // tensorflow::Tensor
  {
    Tensor inputs = ConcatInputs(values);
    PrintTensor(inputs);
  }
  return 0;
}
```

### 実行結果

実装の確認ということで、当たり前ではあるけど同じ結果になります。


```

1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
==========================

1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```

Title: Deep Learning メモメモ
Date: 2019-08-30 18:47:56
Modified: 2019-08-30 18:47:56
Category: deep-learning
Tags: deep-learning
Slug: deep-learning-study
Summary: ざっくり用語周り



ニューラルネットワーク

パーセプトロン

最適化手法

最急降下法

勾配下法

確率的勾配降下法

学習率

逆誤差伝播法

活性化関数

損失関数

バッチ学習

ミニバッチ学習

過学習

正則化

畳み込み

プーリング

ソフトマックス関数


$$ y_{k}=\frac{\exp \left(a_{k}\right)}{\Sigma_{i=1}^{K}\left(\exp \left(a_{i}\right)\right)} $$


ノーフリーランチ定理(no free lunch theorem)
汎用的な機械学習アルゴリズムはないということかな。なのでタスクごとに機械学習アルゴリズムを設計しないといけない。




Affine 

```python
class Affine:
  def __init__(self, W, b):
    self.W = W
    self.b = b
    self.x = None
    self.dW, self.db = None, None
  
  def forward(self, x):
    self.x = x
    out = np.dot(self.x, self.W) + self.b
    return out

  def backward(self, dout):
    dx = np.dot(dout, sefl.W.T)
    self.dW = np.dot(self.x.T, dout)
    self.db = np.sum(dout, axis=0)
    return dx
```

im2col

```python
def im2col(inputs, filter_h, filter_w, stride, pad, constant_values=0):
  N, C, H, W = inputs.shape
  out_h = (H + 2 * pad - filter_h) // stride + 1
  out_w = (W + 2 * pad - filter_w) // stride + 1

  img = np.pad(inputs, [(0, 0), (0, 0), (pad, pad), (pad, pad)], 'constant', constant_values=constant_values)

  col = np.zeros((N, C, filter_h, filter_w, out_h, out_w))

  for y in range(filter_h):
    y_max = y + stride * out_h
    for x in range(filter_w):
      x_max = x + stride * out_w
      col[:, :, y, x, :, :] = img[:, :, y:y_max:stride, x:x_max:stride]

  col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N * out_h * out_w, -1)
  return col
```

col2im

```python
def col2im(col, input_shape, filter_h, filter_w, stride, pad, is_backward=False):
  N, C, H, W = input_shape
  out_h = (H + 2 * pad - filter_h) // stride + 1
  out_w = (W + 2 * pad - filter_w) // stride + 1

  col = col.reshape(N, out_h, out_w, C, filter_h, filter_w).transpose(0, 3, 4, 5, 1, 2)
  img = np.zeros((N, C, H + 2 * pad + stride - 1, W + 2 * pad + stride - 1))

  for y in range(filter_h):
    y_max = y + stride * out_w
    for x in range(filter_w):
      x_max = x + stride * out_w
      if is_backward:
        img[:, :, y:y_max:stride, x:x_max:stride] += col[:, :, y, x, :, :]
      else:
        img[:, :, y:y_max:stride, x:x_max:stride] = col[:, :, y, x, :, :]
  return img[:, :, pad:H + pad, pad:W + pad]
```



KLダイバージェンス


$$ D_{K L}(p \| q)=-\sum p(x) \ln \frac{q(x)}{p(x)} $$


確率分布同士の距離を測る

情報エントロピー

クロスエントロピー誤差

$$ L=\frac{1}{N} \sum_{n}^{N}\left(-\sum_{k}^{K} t_{n k} \log y_{n k}\right)=-\frac{1}{N} \sum_{n}^{N} \sum_{k}^{K} t_{n k} \log y_{n k} $$

ワンショット学習


GAN

$$ \min _{G} \max _{D} V(D, G)=\quad \mathbb{E}_{x \sim p_{\text {data }}}[\log D(x)] \quad+\quad \mathbb{E}_{z-p_{z}}[\log (1-D(G(z)))] $$

<!-- 
ベルマン方程式

$$  $$ -->
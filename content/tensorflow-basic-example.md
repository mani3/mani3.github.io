Title: Tensorflow のメモ
Date: 2018-04-26 22:12:29
Modified: 2018-04-26 22:12:29
Category: python
Tags: python tensorflow
Slug: tensorflow-basic-example
Summary: Tensorflow のサンプル

Tensorflow で行列操作とか、計算する関数とかよくわからなくなるときがあるのでメモ

### tf.gather

```python
row_indices = [1]
row = tf.gather(tf.constant([[1, 2],[3, 4]]), row_indices, axis=1)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(tf.Session().run(row)) 

# [[2]
#  [4]]
```

### tf.where

```python
a = np.array([[1, 2],[3, 4]])
x = tf.placeholder(tf.int32, shape=(2, 2), name='x')

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    b = sess.run(tf.where(x > 2, tf.subtract(x, 1), tf.fill([2, 2], 0)), feed_dict={x: a})
    print(b)

# [[0 0]
#  [2 3]]
```

### tf.argmax

```python
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    a = tf.constant([[0.5, 0.5],[0.1, 0.9]])
    b = tf.constant([[0, 1],[0, 1]])
    result = sess.run([tf.argmax(a, 1), tf.argmax(b, 1)])
    print(result)

# [array([0, 1]), array([1, 1])]
```

### tf.reshape

```python
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    a = tf.constant([0.5, 0.5, 0.1, 0.9])
    result = sess.run(tf.reshape(a, [-1, 1]))
    print(result)

# [[0.5]
#  [0.5]
#  [0.1]
#  [0.9]]


with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())
    a = tf.constant([0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3])
    result = sess.run(tf.reshape(a, [-1, 3, 9]))
    print(result)

# [[[0.5 0.5 0.5 0.4 0.4 0.4 0.3 0.3 0.3]
#   [0.5 0.5 0.5 0.4 0.4 0.4 0.3 0.3 0.3]
#   [0.5 0.5 0.5 0.4 0.4 0.4 0.3 0.3 0.3]]]
```


### IOU ぽいの

```python

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    a = tf.constant([[0.5, 0.5],[0.1, 0.9]])
    b = tf.constant([[0, 1],[0, 1]])
    y1 = tf.cast(tf.greater(tf.gather(a, indices=[1], axis=1), 0.5), tf.bool)
    y2 = tf.cast(tf.gather(b, indices=[1], axis=1), tf.bool)
    intersection = tf.reduce_sum(tf.cast(tf.logical_and(y1, y2), tf.int32))
    union = tf.reduce_sum(tf.cast(tf.logical_or(y1, y2), tf.int32))
        
    result = sess.run([y1, y2, intersection, union, tf.divide(intersection, union)])
    print(result)

# [array([[False],
#        [ True]]), array([[ True],
#        [ True]]), 1, 2, 0.5]
```



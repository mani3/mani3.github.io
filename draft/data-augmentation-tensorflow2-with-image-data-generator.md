





Image Data Generator と tf.data を組み合わせて使う方法


```python

### tf.data

#### Data argumentation

- random crop
- occlusion
- transition
- rotate
- brightness

def preprocess(x):
#   print(x.shape, x)
  return x / 255.

def random_erasing(image, p=0.5, s=(0.02, 0.2), r=(0.3, 2)):
  if np.random.rand() > p:
    return image
  mask_value = np.random.randint(0, 256)
  h, w, _ = image.shape
  mask_area = np.random.randint(h * w * s[0], h * w * s[1])
  mask_aspect_ratio = np.random.rand() * r[1] + r[0]
  mask_height = int(np.sqrt(mask_area / mask_aspect_ratio))
  mask_height = min(mask_height, h - 1)
  mask_width = int(mask_aspect_ratio * mask_height)
  mask_width = min(mask_width, w - 1)
  top = np.random.randint(0, h - mask_height)
  left = np.random.randint(0, w - mask_width)
  bottom = top + mask_height
  right = left + mask_width
  image[top:bottom, left:right, :].fill(mask_value)
  return image

logger = tf.get_logger()

class Dataset(object):
  def __init__(self, fer2013_csv, epochs, batch_size, seed=1234, image_size=48):
    self.epochs = epochs
    self.batch_size = batch_size
    self.seed = seed
    self.image_size = image_size
    
    print('読み込むぞ')
    df = pd.read_csv(fer2013_csv)
    print('読み込んだ')
    self.df_train = df[df['Usage'] == 'Training'].reset_index(drop=True)
    self.df_valid = df[df['Usage'] == 'PrivateTest'].reset_index(drop=True)
    self.max_steps = int(epochs * (len(self.df_train) / batch_size))
    self.cpu_count = multiprocessing.cpu_count()
    self.steps_par_epoch = len(self.df_train) // batch_size
    
    logger.info('total_count: {}'.format(len(df)))
    logger.info('train_count: {}, valid_count: {}'.format(len(self.df_train), len(self.df_valid)))
    logger.info('max_steps: {}, steps_par_epoch: {}'.format(self.max_steps, self.steps_par_epoch))
    logger.info('cpu_count: {}'.format(self.cpu_count))
    logger.info('image_size: {}'.format(self.image_size))

  def random_erasing(self, image, label):
    # image = tf.compat.v1.py_func(random_erasing, [image], (tf.float32))
#     image = tf.py_function(random_erasing, [image], (tf.float32))
    tf.print(type(image), label)
    return image, label
  
  def mixup(self, image, label):
    tf.print('mixup', type(image), label)
    return image, label
  
  def parse_pixels(self, x, w, h):
    x = x.split(' ')
    x = np.array(x, dtype=np.uint8).reshape(h, w, 1)
    return x
    
  def train_input_fn(self):
    image_size = self.image_size
    batch_size = self.batch_size
    x = self.df_train['pixels'].tolist()[:100]
    x = np.array([self.parse_pixels(i, image_size, image_size) for i in x])
    y = self.df_train['emotion'].tolist()[:100]
    
    param = {
      'preprocessing_function': preprocess,
      'rotation_range': 40,
      'width_shift_range': 0.2,
      'height_shift_range': 0.2,
      'shear_range': 5,
      'zoom_range': [0.6, 1.2],
      'brightness_range': [0.5, 1.5],
      'fill_mode': 'constant',
      'cval': 0,
      'horizontal_flip': True,
    }
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(**param)
    # generator = datagen.fit(x, y, seed=self.seed)
    generator = datagen.flow(x, y, seed=self.seed, batch_size=batch_size)
    
    
    dataset = tf.data.Dataset.from_generator(lambda: generator, (tf.float32, tf.float32))
    dataset = dataset.map(self.random_erasing) # decided batch_size from datagen 
    dataset = dataset.map(self.mixup)
#     dataset = dataset.shuffle(10000, seed=self.seed).repeat(self.epochs)
    
    for next_element in dataset.take(1):
      image = next_element[0].numpy()
      output = next_element[1].numpy()
      print('出力サイズの確認', image.shape, type(image), output.shape)
      plt.imshow(image[0, :, :, 0])
      plt.show()

    return dataset  
  
  def valid_input_fn(self):
    pass
  
  
dataset = Dataset(fer_2013_csv, 1, 4)
dataset.train_input_fn()
```





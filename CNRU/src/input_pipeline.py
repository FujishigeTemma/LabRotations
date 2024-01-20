import tensorflow as tf
import tensorflow_datasets as tfds
from jax import numpy as jnp


def build_train_set(batch_size: int, ds_builder):
    """Builds train dataset."""
    train_ds = ds_builder.as_dataset(split=tfds.split_for_jax_process(tfds.Split.TRAIN))  # type: ignore
    train_ds = train_ds.map(preprocess_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    train_ds = train_ds.cache()
    train_ds = train_ds.repeat()
    train_ds = train_ds.shuffle(50000)
    train_ds = train_ds.batch(batch_size)
    train_ds = train_ds.prefetch(tf.data.experimental.AUTOTUNE)
    train_ds = train_ds.as_numpy_iterator()
    return (jnp.array(v) for v in train_ds)


def build_test_set(batch_size: int, ds_builder):
    """Builds train dataset."""
    test_ds = ds_builder.as_dataset(split=tfds.Split.TEST)  # type: ignore
    test_ds = test_ds.map(preprocess_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    test_ds = test_ds.batch(batch_size)
    test_ds = test_ds.as_numpy_iterator()
    return (jnp.array(v) for v in test_ds)


def preprocess_image(data):
    """Resize and normalize images."""
    if "image" in data:
        image = tf.image.resize(data["image"], [128, 128])
    elif "video" in data:
        video = data["video"]
        video = tf.slice(video, [0, 0, 0, 0], [-1, -1, video.shape[2] // 2, -1])
        video = tf.map_fn(lambda frame: tf.image.resize(frame, [128, 128]), video, dtype=tf.float32)
        image = video[tf.random.uniform(shape=[], minval=0, maxval=tf.shape(video)[0], dtype=tf.int32)]
    image = tf.cast(image, tf.float32) / 255.0  # type: ignore
    return image

import numpy as np

from src.preprocessing.transform import resize_slice


def test_resize_slice():
    image = np.random.rand(320, 320).astype(np.float32)

    resized = resize_slice(image, (224, 224))

    assert resized.shape == (224, 224)
    assert resized.dtype == np.float32

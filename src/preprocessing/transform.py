import numpy as np
from PIL import Image


def resize_slice(
    image: np.ndarray,
    size: tuple[int, int] = (224, 224),
) -> np.ndarray:
    """
    Resize a single MRI slice.

    Parameters
    ----------
    image : np.ndarray
        2D normalized MRI slice.
    size : tuple[int, int]
        Target size as (width, height).

    Returns
    -------
    np.ndarray
        Resized 2D slice as float32.
    """

    if image.ndim != 2:
        raise ValueError(
            "Expected a 2D MRI slice."
        )

    resized = Image.fromarray(image.astype(np.float32))

    resized = resized.resize(
        size,
        Image.Resampling.BILINEAR,
    )

    return np.asarray(
        resized,
        dtype=np.float32,
    )

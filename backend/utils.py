from io import BytesIO

import cv2
import numpy as np


def convert_np_array_to_bytes(image: np.ndarray) -> BytesIO:
    is_success, result = cv2.imencode(".jpg", image)
    result = BytesIO(result)
    result.seek(0)
    return result

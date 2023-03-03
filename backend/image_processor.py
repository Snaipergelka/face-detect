import cv2
import numpy as np

from backend.schemas import ColorType


class ImageProcessor:

    def __init__(self):
        pass

    @staticmethod
    def convert_color_to_rgb(color):
        if color == "red":
            return 0, 0, 255
        elif color == "green":
            return 0, 255, 0
        elif color == "blue":
            return 255, 0, 0

    @staticmethod
    def add_face_rectangles_to_image(image_np: np.ndarray,
                                     face_coordinates: list,
                                     color: ColorType,
                                     thickness: int = 3) -> np.ndarray:

        color = ImageProcessor.convert_color_to_rgb(color)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        for (top, left, width, height) in face_coordinates:
            cv2.rectangle(img, (left, top), (left + width, top + height),
                          color, thickness)
        return img

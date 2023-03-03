from enum import Enum

from pydantic import BaseModel


class ColorType(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"


class ImageIdResponse(BaseModel):
    id: int

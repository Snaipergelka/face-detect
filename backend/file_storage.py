import uuid

from fastapi import UploadFile
import numpy as np
import s3fs


class S3FileStorage:

    def __init__(self, key, secret, url):
        self.fs = s3fs.S3FileSystem(key=key,
                                    secret=secret,
                                    client_kwargs={'endpoint_url': url})

    def save_image_in_s3(self, image: UploadFile) -> str:
        image.filename = '.'.join([str(uuid.uuid4()), image.filename.split('.')[-1]])

        with self.fs.open(f'images/{image.filename}', 'wb') as file:
            image.file.seek(0)
            file.write(data=image.file.read())

        return f"s3://images/{image.filename}"

    def get_image_from_s3(self, path) -> np.ndarray:
        return np.fromstring(self.fs.open(path).read(), np.uint8)

    def delete_image_from_s3(self, path: str):
        self.fs.delete(path)

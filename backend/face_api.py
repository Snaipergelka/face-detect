import aiohttp
from aiohttp import FormData, ClientSession
from fastapi import UploadFile


class FaceAPI:

    def __init__(self, api_key, api_secret, url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.url = url
        self.session = ClientSession()

    async def detect_faces(self, image: UploadFile):
        data = self.form_request_data_for_face_api(image)
        async with self.session.post(self.url, data=data, verify_ssl=False) as response:
            content = await response.json()
        return content

    def form_request_data_for_face_api(self, image: UploadFile) -> FormData:
        data = aiohttp.FormData()
        data.add_field("api_key", self.api_key)
        data.add_field("api_secret", self.api_secret)
        data.add_field('image_file',
                       image.file.read(),
                       filename=image.filename,
                       content_type=image.content_type)
        return data

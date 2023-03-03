import pytest
from starlette import status

from backend.errors import ImageNotFoundError


class TestsBase:
    request_id: int = None

    @pytest.mark.asyncio
    async def test_post_image(self, client):
        fpath = "./test_images/image_with_faces.jpeg"

        response = await client.post(
            "/image",
            files={"image": ("test.jpg", open(fpath, "rb"))}
        )
        TestsBase.request_id = response.json()['id']
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_image(self, client):
        response = await client.get(f'/image/{TestsBase.request_id}?color=red&thickness=3')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_image(self, client):
        fpath = "./test_images/image_with_faces.jpeg"
        response = await client.put(
            f"/image/{TestsBase.request_id}",
            files={"image": ("test.jpg", open(fpath, "rb"))}
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_delete_image(self, client):
        response = await client.delete(f"/image/{TestsBase.request_id}")
        assert response.status_code == status.HTTP_200_OK

        try:
            response = await client.get(f'/image/{TestsBase.request_id}?color=red&thickness=3')
        except ImageNotFoundError as ex:
            assert True
            return
        assert False

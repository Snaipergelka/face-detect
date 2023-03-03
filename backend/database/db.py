from sqlalchemy import update, select

from backend.database import models
from backend.database.models import Image
from backend.errors import ImageNotFoundError


class Database:

    def __init__(self, session_maker):
        print("Created DB!")
        self.session_maker = session_maker

    async def create_image(self, image_path: str, faces_response: dict) -> Image:
        async with self.session_maker() as session:
            instance = models.Image(**{"image": image_path}, **faces_response)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            await session.close()
            return instance

    async def get_image_or_404(self, id: int) -> Image:
        async with self.session_maker() as session:
            image_instance = await session.execute(select(Image).where(Image.id == id))
            image_instance = image_instance.scalars().first()
            if image_instance:
                return image_instance
            raise ImageNotFoundError({"status_code": 404,
                                      "body": "Image not found"})

    async def update_image(self, image_instance: Image, update_info: dict):

        u = update(Image)
        u = u.values(update_info)
        u = u.where(Image.id == image_instance.id)

        async with self.session_maker() as session:
            await session.execute(u)
            await session.commit()
            await session.close()

    async def delete_image(self, image_instance: Image):
        async with self.session_maker() as session:
            await session.delete(image_instance)
            await session.commit()
            await session.close()

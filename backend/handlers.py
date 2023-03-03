from dependency_injector.wiring import inject, Provide
from fastapi import UploadFile, Depends, APIRouter
from starlette.responses import StreamingResponse

from backend.database.db import Database
from backend.face_api import FaceAPI
from backend.image_processor import ImageProcessor
from backend.schemas import ColorType, ImageIdResponse
from backend.utils import convert_np_array_to_bytes
from backend.file_storage import S3FileStorage
from backend.containers import Container


router = APIRouter()


@router.post("/image")
@inject
async def post_image(image: UploadFile,
                     file_storage: S3FileStorage = Depends(Provide[Container.s3_file_storage]),
                     face_api: FaceAPI = Depends(Provide[Container.face_api]),
                     db: Database = Depends(Provide[Container.database])):

    content = await face_api.detect_faces(image)
    image_path = file_storage.save_image_in_s3(image)
    image_instance = await db.create_image(image_path=image_path, faces_response=content)

    return ImageIdResponse(id=image_instance.id)


@router.get("/image/{id}")
@inject
async def get_image(id: int,
                    color: ColorType,
                    thickness: int = 3,
                    file_storage: S3FileStorage = Depends(Provide[Container.s3_file_storage]),
                    db: Database = Depends(Provide[Container.database])):

    instance = await db.get_image_or_404(id)
    face_coordinates = [face_rectangle['face_rectangle'].values() for face_rectangle in instance.faces]
    image_path = instance.image

    image = file_storage.get_image_from_s3(image_path)
    image = ImageProcessor.add_face_rectangles_to_image(
        image_np=image,
        color=color,
        face_coordinates=face_coordinates,
        thickness=thickness)

    result = convert_np_array_to_bytes(image)

    return StreamingResponse(result, media_type="image/jpeg")


@router.put("/image/{id}")
@inject
async def update_image_in_db(id: int,
                             image: UploadFile,
                             file_storage: S3FileStorage = Depends(Provide[Container.s3_file_storage]),
                             face_api: FaceAPI = Depends(Provide[Container.face_api]),
                             db: Database = Depends(Provide[Container.database])):

    content = await face_api.detect_faces(image)

    image_instance = await db.get_image_or_404(id=id)
    file_storage.delete_image_from_s3(image_instance.image)
    image_path = file_storage.save_image_in_s3(image)

    content.update({"image": image_path})
    await db.update_image(image_instance=image_instance, update_info=content)

    return ImageIdResponse(id=image_instance.id)


@router.delete("/image/{id}")
@inject
async def delete_image(id: int,
                       file_storage: S3FileStorage = Depends(Provide[Container.s3_file_storage]),
                       db: Database = Depends(Provide[Container.database])):
    image_instance = await db.get_image_or_404(id=id)
    file_storage.delete_image_from_s3(image_instance.image)
    await db.delete_image(image_instance=image_instance)
    return

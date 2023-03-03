import asyncio

from dependency_injector import containers, providers

from backend.config import get_settings
from backend.file_storage import S3FileStorage
from backend.database.db import Database
from backend.face_api import FaceAPI
from backend.database.connection.session import get_session, SessionManager


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".handlers"])

    # used to store images
    s3_file_storage = providers.Singleton(S3FileStorage, **get_settings().s3_settings)

    # object to make requests to Face++ API
    face_api = providers.Singleton(FaceAPI, **get_settings().face_api_settings)

    # used to store image analysis results
    session_maker = providers.Singleton(get_session, get_settings().database_uri)
    database = providers.Singleton(Database, session_maker)

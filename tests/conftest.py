import os
from types import SimpleNamespace
from uuid import uuid4

from alembic.command import upgrade
from alembic.config import Config
from asyncio import new_event_loop, set_event_loop
from httpx import AsyncClient
from mock import Mock
import pytest
import pytest_asyncio
from sqlalchemy_utils import create_database, database_exists, drop_database

import backend.face_api
from backend.application import create_app
import tests.utils as test_utils


def database_uri_sync(database) -> str:
    """
    Get uri for connection with database.
    """
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    loop = new_event_loop()
    set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture()
def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """
    tmp_name = ".".join([uuid4().hex, "pytest"])
    # нужно, чтобы в остальных функциях использовать тестовую бд
    os.environ["POSTGRES_DATABASE"] = tmp_name
    tmp_url = database_uri_sync(tmp_name)
    print(tmp_url)

    if not database_exists(tmp_url):
        create_database(tmp_url)
    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(
        config=".", name="alembic", pg_url=database_uri_sync(os.getenv("POSTGRES_DATABASE")),
        raiseerr=False, x=None
    )
    return test_utils.make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, "head")


async def get_mock_value():
    return {
        'request_id': '1677843747,ca237cfc-2110-4f16-85b2-055feb22ecb0', 'time_used': 149, 'faces': [
            {'face_token': '64e3536092de6aee60576e20f7b90cad',
             'face_rectangle': {'top': 29, 'left': 43, 'width': 69, 'height': 69}},
            {'face_token': 'f662b2fb12688709bf05721c2dd5093b',
             'face_rectangle': {'top': 137, 'left': 566, 'width': 57, 'height': 57}},
            {'face_token': 'd215a024bbf05ecdfe1c10715ef029cb',
             'face_rectangle': {'top': 148, 'left': 383, 'width': 56, 'height': 56}},
            {'face_token': 'a507f3268e0d0e305fa682125a9da2a8',
             'face_rectangle': {'top': 137, 'left': 249, 'width': 50, 'height': 50}},
            {'face_token': '2a114bb4b995d84a61a6f720309495fe',
             'face_rectangle': {'top': 110, 'left': 500, 'width': 35, 'height': 35}}],
        'image_id': 'u7uGrn1lRvKGdKRIDNeFEg==', 'face_num': 5}


@pytest_asyncio.fixture
async def client(migrated_postgres) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = create_app()
    backend.face_api.FaceAPI.detect_faces = Mock(return_value=get_mock_value())
    yield AsyncClient(app=app, base_url="http://tests")

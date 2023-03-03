from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self, database_uri: str) -> None:
        self.database_uri = database_uri
        self.engine = create_async_engine(self.database_uri, echo=True, future=True)
        self.refresh()

    def __new__(cls, database_uri: str):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(self.database_uri, echo=True, future=True)


def get_session(database_uri: str):
    session_maker = SessionManager(database_uri).get_session_maker()
    return session_maker


__all__ = [
    "get_session",
]

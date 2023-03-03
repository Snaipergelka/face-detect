from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Image(Base):
    __tablename__ = "face_app_images"

    id = Column("Image id", Integer, primary_key=True)
    image = Column("Path to an image", String)
    request_id = Column("Face++ request id", String)
    faces = Column("List of found faces", ARRAY(JSON))
    face_num = Column("Number of faces", Integer)
    image_id = Column("Face++ image id", String)
    time_used = Column("Time used by Face++", Integer)

    def __str__(self):
        return self.image_id

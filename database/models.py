from sqlalchemy import Column, Integer, String
from .database import Base


class ShortURL(Base):

    __tablename__ = "short url record"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True)
    short_url = Column(String, unique=True)

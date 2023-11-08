"""Модели."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class ShortUrl(Base):
    """Модель юзера."""

    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    long_url = Column(String, nullable=False)
    hash = Column(String, nullable=False)

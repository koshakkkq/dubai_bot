import asyncio

import datetime

import sqlalchemy
from sqlalchemy import ForeignKey, func, select, Column, Integer, String

from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy.orm import DeclarativeBase, Mapped
from .base import Base

class Shop(Base):
	__tablename__ = 'shop'

	id = Column(Integer, primary_key=True, index=True)
	shop_name = Column(String, nullable=True)
	shop_location = Column(String, nullable=True)
	shop_phone = Column(String, nullable=True)



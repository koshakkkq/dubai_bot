import asyncio

import datetime

import sqlalchemy
from sqlalchemy import ForeignKey, func, select, Column, Integer, String, BigInteger

from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy.orm import DeclarativeBase, Mapped
from .base import Base

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, index=True)
	telegram_id = Column(BigInteger, nullable=False)
	language = Column(String(100), nullable=True)

class ShopMembers(Base):
	__tablename__ = 'shop_members'

	id = Column(Integer, primary_key=True, index=True)
	shop_id = Column(Integer, ForeignKey('shop.id'))
	user_id = Column(Integer, ForeignKey('user.id'))


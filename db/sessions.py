from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_session
from sqlalchemy.orm import sessionmaker

from loader import engine


@asynccontextmanager
async def get_session() -> AsyncSession:
	try:
		async_session = async_session_generator()
		async with async_session() as session:
			yield session
	except:
		await session.rollback()
		print('rollback')
		raise
	finally:
		await session.close()


def async_session_generator():
	return sessionmaker(
    	engine, class_=AsyncSession
	)
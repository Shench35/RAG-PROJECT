from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.services.config import Config

engine = create_async_engine(
    Config.DATABASE_URL, 
    echo=False,  # Disable SQL query logging for production performance
    pool_pre_ping=True,  # Check connections before using them
    pool_size=10,  # Connection pool size
    max_overflow=20  # Max overflow connections
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session

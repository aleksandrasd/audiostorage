import asyncio
import app.audio.domain.entity.audio_file
import app.user.domain.entity.user
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import config
from core.db.session import Base
from minio_storage import minio_client

# Import all models to ensure they are registered with Base


async def create_tables():
    # Replace 'sqlite+aiosqlite:///example.db' with your actual async database URL
    # For PostgreSQL, you might use something like 'postgresql+asyncpg://user:password@localhost/dbname'
    engine = create_async_engine(config.WRITER_DB_URL, echo=True)

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    # Create a sessionmaker
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    sql_file_path = "db.sql"  # Path to your SQL file
    with open(sql_file_path, "r") as file:
        sql_commands = file.read()
        
    await engine.dispose()
    
    try:
      minio_client.make_bucket(config.BUCKET_NAME)
    except Exception as e:
      print(f"While creating bucket an exception occurred: {e}")


if __name__ == "__main__":
    try:
      asyncio.run(create_tables())
    except Exception as e:
      print(f"Exception occurred: {e}")
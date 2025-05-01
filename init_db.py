import asyncio
import app.audio.domain.entity.audio_file
import app.user.domain.entity.user
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import config
from core.db.session import Base
from minio_storage import minio_client


async def create_tables():
    with open("db.sql", "r") as file:
        sql_commands = file.read()
    engine = create_async_engine(config.WRITER_DB_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(sql_commands))  
        
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
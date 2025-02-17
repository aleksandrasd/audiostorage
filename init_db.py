# create_tables.py
from sqlalchemy import create_engine

from core.config import config
from core.db.session import Base

# Import all models to ensure they are registered with Base


# Replace 'sqlite:///example.db' with your actual database URL
engine = create_engine(config.SYN_WRITER_DB_URL)

# Create all tables
Base.metadata.create_all(engine)

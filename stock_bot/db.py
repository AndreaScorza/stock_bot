from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from stock_bot.config import Config

# Create the SQLite engine
engine = create_engine(Config.DB_URL, echo=False)

# Create a sessionmaker for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Initialize the database (call this function when setting up)
def init_db():
    Base.metadata.create_all(bind=engine)

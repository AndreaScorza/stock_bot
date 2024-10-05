from sqlalchemy import Column, Integer, String, Float
from stock_bot.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    username = Column(String, index=True)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(String)
    filing_date = Column(String)
    reporting_name = Column(String)
    activity = Column(String)
    security = Column(String)
    shares = Column(Integer)
    price = Column(Float)
    total = Column(Float)

    # Used for debugging prints
    def __repr__(self):
        return f"<Transaction(date={self.transaction_date}, security={self.security}, activity={self.activity})>"


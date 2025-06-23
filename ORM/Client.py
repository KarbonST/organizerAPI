from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id       = Column(Integer, primary_key=True, index=True)
    inn      = Column(String(10), unique=True, nullable=False)
    fullname = Column(String,    nullable=False)
    company  = Column(String,    nullable=False)
    phone    = Column(String,    nullable=False)
    worker_fullname = Column(String, nullable=False)
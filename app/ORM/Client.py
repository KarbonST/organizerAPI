from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    worker_fullname = Column(String, nullable=False)
    inn = Column(String(10), unique=True, nullable=False)
    company_name = Column(String, nullable=False)
    is_client = Column(String, nullable=False)
    working_sphere = Column(String, nullable=False)
    contact_fullname = Column(String,    nullable=False)
    phone = Column(String,    nullable=False)
    client_request = Column(String, nullable=False)

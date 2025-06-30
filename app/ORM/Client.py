from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.ORM.base import Base

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

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="clients")
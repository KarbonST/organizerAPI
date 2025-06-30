from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.ORM.base import Base

class Event(Base):
    __tablename__ = "events"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=True, nullable=False)

    clients = relationship("Client", back_populates="event", cascade="all, delete-orphan")

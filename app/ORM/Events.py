from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.ORM.base import Base

class Events(Base):
    __tablename__ = "events"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=True, nullable=False)
    event_number = Column(Integer, nullable=False, index=True)

    clients = relationship("Clients", back_populates="event", cascade="all, delete-orphan",
                           passive_deletes=True)

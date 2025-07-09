from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel 

class Event(BaseModel):
    __tablename__ = "events"

    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    organizer_id = Column(ForeignKey("users.id"), nullable=False)

    organizer = relationship("User", back_populates="events")
    feedbacks = relationship("Feedback", back_populates="event", cascade="all, delete-orphan")
    files = relationship("File", back_populates="event", cascade="all, delete-orphan")
    rsvps = relationship("RSVP", back_populates="event", cascade="all, delete-orphan")

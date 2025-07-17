from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel

class Event(BaseModel):
    __tablename__ = "events"

    image_url = Column(String(512), nullable=False)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    organizer_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    organizer = relationship("User", back_populates="events")
    feedbacks = relationship("Feedback", back_populates="event", cascade="all, delete-orphan")
    files = relationship("File", back_populates="event", cascade="all, delete-orphan")
    rsvps = relationship("RSVP", back_populates="event", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")


    def __repr__(self):
        return (
            f"<Event(title={self.title}, location={self.location}, "
            f"start_time={self.start_time}, end_time={self.end_time})>"
        )

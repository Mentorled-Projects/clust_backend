from sqlalchemy import Column, String, Enum
import enum
from sqlalchemy.orm import relationship


from api.v1.models.base_class import BaseModel 

class UserRole(str, enum.Enum):
    organizer = "organizer"
    attendee = "attendee"

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)


    events = relationship("Event", back_populates="organizer")
    rsvps = relationship("RSVP", back_populates="user")
    groups = relationship("Group", back_populates="organizer")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    uploaded_files = relationship("File", back_populates="uploader", cascade="all, delete-orphan")

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID

from api.v1.models.base_class import BaseModel 
from sqlalchemy.orm import relationship

class Feedback(BaseModel):
    __tablename__ = "feedback"

    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    event = relationship("Event", back_populates="feedbacks")
    user = relationship("User", back_populates="feedbacks")

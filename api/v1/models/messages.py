from sqlalchemy import Column, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel, Base




class Message(BaseModel):
    __tablename__ = "messages"
    content = Column(Text, nullable=False)
    sender_id = Column(ForeignKey("users.id"), nullable=False)
    group_id = Column(ForeignKey("groups.id"), nullable=False)

    sender = relationship("User", back_populates="messages_sent")
    group = relationship("Group", back_populates="messages")

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel 

class Group(BaseModel):
    __tablename__ = "groups"

    name = Column(String, nullable=False)
    description = Column(Text)
    organizer_id = Column(ForeignKey("users.id"), nullable=False)

    organizer = relationship("User", back_populates="groups")

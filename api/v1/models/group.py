from sqlalchemy import Column, String, Text, ForeignKey, Table, Boolean, Index
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel, Base

group_members = Table(
    "group_members",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

class Group(BaseModel):
    __tablename__ = "groups"

    image_url = Column(String(512), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    organizer_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    location = Column(String(255), nullable=False)
    is_private = Column(Boolean, default=False)

    organizer = relationship("User", back_populates="groups")
    members = relationship("User", secondary=group_members, back_populates="member_groups")
    messages = relationship("Message", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Group(name={self.name}, is_private={self.is_private}, location={self.location})>"

from sqlalchemy import Column, String, Text, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel, Base


group_members = Table(
    "group_members",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id")),
)
class Group(BaseModel):
    __tablename__ = "groups"

    name = Column(String, nullable=False)
    description = Column(Text)
    organizer_id = Column(ForeignKey("users.id"), nullable=False)
    is_private = Column(Boolean, default=False)

    organizer = relationship("User", back_populates="groups")
    members = relationship("User", secondary=group_members, back_populates="member_groups")
    messages = relationship("Message", back_populates="group", cascade="all, delete-orphan")
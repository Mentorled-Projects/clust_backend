from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel, Base

user_categories = Table(
    "user_categories",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(100), nullable=False, unique=True)
    users = relationship("User", secondary=user_categories, back_populates="categories")

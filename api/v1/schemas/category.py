from pydantic import BaseModel
from uuid import UUID

class CategoryBase(BaseModel):
    name: str

class CategoryOut(CategoryBase):
    id: UUID

    class Config:
        orm_mode = True

class CategoryAssign(BaseModel):
    category_ids: list[UUID]
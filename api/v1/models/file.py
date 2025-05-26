from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from api.v1.models.base_class import BaseModel 
from sqlalchemy.orm import relationship

class File(BaseModel):
    __tablename__ = "files"

    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_url = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    event = relationship("Event", back_populates="files")
    uploader = relationship("User", back_populates="uploaded_files")

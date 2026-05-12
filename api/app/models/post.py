from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.postgres import Base


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "api_social_media"}

    id = Column(BigInteger, primary_key=True)
    content = Column(Text, nullable=False)
    id_user = Column(BigInteger, ForeignKey("api_social_media.users.id"), nullable=False)
    guid = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
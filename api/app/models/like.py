from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.db.postgres import Base


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("id_post", "id_user", name="uq_like_post_user"),
        {"schema": "api_social_media"}
    )

    id = Column(BigInteger, primary_key=True)
    id_post = Column(BigInteger, ForeignKey("api_social_media.posts.id"), nullable=False)
    id_user = Column(BigInteger, ForeignKey("api_social_media.users.id"), nullable=False)
    guid = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


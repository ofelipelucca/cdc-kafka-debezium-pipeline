from sqlalchemy import Column, BigInteger, String

from app.db.postgres import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "api_social_media"}

    id = Column(BigInteger, primary_key=True)
    nome = Column(String(800), nullable=False)
    email = Column(String(254), nullable=False)
    guid = Column(String(36), unique=True, nullable=False)

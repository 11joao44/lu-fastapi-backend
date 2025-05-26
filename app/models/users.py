from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, text
from app.core.database import Base, relationship

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    is_admin = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    orders = relationship("OrderModel", back_populates="user")
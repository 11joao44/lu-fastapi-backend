from sqlalchemy import Column, Integer, String, Text, Numeric, Date, DateTime, func, text
from app.core.database import Base

class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    barcode = Column(String(50), unique=True)
    section = Column(String(100), index=True)
    stock = Column(Integer, nullable=False, server_default=text("0"))
    expiration_date = Column(Date)
    image_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

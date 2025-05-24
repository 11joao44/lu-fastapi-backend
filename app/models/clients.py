from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base, relationship

class ClientModel(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    address = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    orders = relationship("OrderModel", back_populates='client')
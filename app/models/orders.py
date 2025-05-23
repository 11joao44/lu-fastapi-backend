from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, DateTime, func
from app.core.database import Base, relationship

class Orders(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    status = Column(String(20), index=True, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    clients = relationship("Clients", back_populates=__tablename__)
    users = relationship("Users", back_populates=__tablename__ )
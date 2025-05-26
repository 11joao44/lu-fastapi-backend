from sqlalchemy import Column, Integer, ForeignKey, Numeric, UniqueConstraint, DateTime, func, text
from app.core.database import Base, relationship

class OrderProductsModel(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, server_default=text("1"))
    price_at_moment = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('order_id', 'product_id', name='uq_order_product'),
    )

    order = relationship("OrderModel", back_populates="order_products")
    product = relationship("ProductModel")

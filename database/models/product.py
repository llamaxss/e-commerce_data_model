from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import func, DateTime
from datetime import datetime

from ..base import Base


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)
    base_price: Mapped[float] = mapped_column(nullable=False)
    stock_quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(product_id={self.product_id}, category={self.category}, base_price={self.base_price}, stock_quantity={self.stock_quantity}, created_at={self.created_at}, updated_at={self.updated_at})>"

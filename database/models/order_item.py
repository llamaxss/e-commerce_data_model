from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime

from ..base import Base


class OrderItem(Base):
    __tablename__ = "order_item"

    order_id: Mapped[str] = mapped_column(
        ForeignKey("order.order_id"), primary_key=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("product.product_id"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)
    discount_applied: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self) -> str:
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}, unit_price={self.unit_price}, total_price={self.total_price}, discount_applied={self.discount_applied}, created_at={self.created_at}, updated_at={self.updated_at})>"

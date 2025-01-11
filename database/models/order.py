from sqlalchemy import ForeignKey, func, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime

from ..base import Base


class Order(Base):
    __tablename__ = "order"

    order_id: Mapped[str] = mapped_column(primary_key=True)
    customer_id: Mapped[str] = mapped_column(
        ForeignKey("customer.customer_id"), nullable=False
    )
    order_date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self) -> str:
        return f"<Order(order_id={self.order_id}, customer_id={self.customer_id}, order_date={self.order_date}, status={self.status}, total_amount={self.total_amount}, created_at={self.created_at}, updated_at={self.updated_at})>"

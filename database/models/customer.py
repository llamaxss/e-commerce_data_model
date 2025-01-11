from sqlalchemy import func, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime

from ..base import Base


class Customer(Base):
    __tablename__ = "customer"

    customer_id: Mapped[str] = mapped_column(primary_key=True)
    join_date: Mapped[datetime] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"<Customer(customer_id={self.customer_id}, join_date={self.join_date}, phone_number={self.phone_number}, email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})>"
